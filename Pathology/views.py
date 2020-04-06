import datetime
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from Pathology.GetValueFromPowerAI import *
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Pathology.forms import *
import os
import mimetypes
import glob
import pdfkit


def create_pdf(request, patient_name):
    path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path)
    path_folder = os.getcwd() + os.sep + "Pathology" + os.sep + "pdf_output" + os.sep + "*.pdf"
    for pdf in glob.glob(path_folder):
        print("[+] Removed previous PDF.")
        os.remove(pdf)

    url_ = request.scheme + "://" + request.get_host() + "/report/"
    save_file = os.getcwd() + os.sep + "Pathology" + os.sep + "pdf_output" + os.sep + str(patient_name) + "_report.pdf"
    pdfkit.from_url(url_, save_file, configuration=config)
    fl_path = os.getcwd() + os.sep + "Pathology" + os.sep + "pdf_output" + os.sep + str(patient_name) + "_report.pdf"
    filename = str(patient_name) + "_report.pdf"
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def home(request):
    return render(request, 'Home.html')


def about_us(request):
    return render(request, 'About_Us.html')


def contact_us(request):
    return render(request, 'Contact_Us.html')


def test_in_pathology(request):
    test_list = []
    patient_name = ''
    global len_value
    global value
    if request.method == 'POST':
        value = request.POST.getlist('test')
        len_value = len(value)
        return HttpResponseRedirect('/image_upload/')

    else:
        tests = Test_Pathology.objects.all()
        for test in tests:
            test_list.append(test)
        patients = Patient_Details.objects.all()
        length = len(patients) - 1
        patient_name = patients[length]

    return render(request, 'test_in_pathology.html', {'tests': test_list, 'patient_name': patient_name})


def image_upload_wr(request, test_name):
    print('test_name', test_name)
    test_list = []
    if request.method == 'POST':
        form = Image_Input_Forms(request.POST, request.FILES)
        check_box = request.POST.get("heatmap_bool", None)
        print("[INFO] Checkbox ", check_box)
        if form.is_valid():
            if check_box is None:
                form.save()
                image = Image_Input.objects.filter(id=len(Image_Input.objects.all()))
                test_url = Test_Pathology.objects.filter(some_test=test_name)
                filename = os.getcwd() + os.sep + 'media' + os.sep + str(image[0])
                destination = os.getcwd() + os.sep + "Pathology" + os.sep + "static" + os.sep + "uploadImage" + os.sep + "upload.jpg"
                from shutil import copy
                copy(filename, destination)
                output = detect_image_label(filename, test_url[0].api_url)
                print("[INFO] conf", round(output[2], 2))
                request.session['test_name'] = test_name
                request.session['result'] = output[1]
                request.session['confidence'] = round(output[2], 2)
                AI_Usecase_Occurences.objects.create(time=datetime.now(), Image_Output_1=output[1], confidence=round(output[2], 2), heatmap=None)
                return HttpResponseRedirect('/report_wr_h/')
            else:
                form.save()
                image = Image_Input.objects.filter(id=len(Image_Input.objects.all()))
                test_url = Test_Pathology.objects.filter(some_test=test_name)
                filename = os.getcwd() + os.sep + 'media' + os.sep + str(image[0])
                destination = os.getcwd() + os.sep + "Pathology" + os.sep + "static" + os.sep + "uploadImage" + os.sep + "upload.jpg"
                from shutil import copy
                copy(filename, destination)
                output = detect_image_label(filename, test_url[0].api_url)
                print("[INFO] conf", round(output[2], 2))
                import urllib.request
                name = os.getcwd() + os.sep + "Pathology" + os.sep + "static" + os.sep + "heatmap" + os.sep + "heatmap.png"
                urllib.request.urlretrieve(output[3], name)

                request.session['test_name'] = test_name
                request.session['result'] = output[1]
                request.session['confidence'] = round(output[2], 2)

                AI_Usecase_Occurences.objects.create(time=datetime.now(), Image_Output_1=output[1], confidence=round(output[2], 2), heatmap=name)

            return HttpResponseRedirect('/report_wr/')
    else:
        tests = Test_Pathology.objects.all()
        for test in tests:
            test_list.append(test)
        form = Image_Input_Forms()
        context = {
            'form': form,
            'test_name': test_name,
        }

    return render(request, 'image_upload_wr.html', context)


def analyze(request):
    test_list = []
    if request.method == 'POST':
        tests = request.POST.getlist('test')
        p_name = request.POST.get('patient_name')
        print("[INFO] tests, patient_name ", tests, p_name)
        request.session['p_name'] = p_name
        url_test = "/image_upload_wr/" + tests[0]
        return HttpResponseRedirect(str(url_test))

    else:
        tests = Test_Pathology.objects.all()
        for test in tests:
            test_list.append(test)
        context = {
            'tests': test_list,
        }
        return render(request, 'test_wr.html', context)


def report_view(request):
    test_list = []
    location = Location.objects.all()
    loc_length = len(location) - 1
    l1 = location[loc_length]

    results = AI_Usecase_Occurences.objects.all().values_list('Image_Output_1', flat=True)
    conf = AI_Usecase_Occurences.objects.all().values_list('confidence', flat=True)
    heatmap = AI_Usecase_Occurences.objects.all().values_list('heatmap', flat=True)
    results_list = list(results)
    conf_list = list(conf)
    heat_list = list(heatmap)

    value
    newlist = results_list[-len_value:]
    confList = conf_list[-len_value:]
    heatList = heat_list[-len_value:]
    upload_image = os.getcwd() + os.sep + "Pathology" + os.sep + "static" + os.sep + "uploadImage" + os.sep + "upload.jpg"

    tests = Test_Pathology.objects.all()
    for test in tests:
        test_list.append(test)
    patients = Patient_Details.objects.all()
    length = len(patients) - 1
    patient_name = patients[length]

    confListNew = []
    for i in confList:
        temp = i[:5]
        confListNew.append(temp)

    context = {
        'heatList': heatList,
        'confList': confListNew,
        'newlist': newlist,
        'value': value,
        'patient_name': patient_name,
        'Location': l1,
        'upload_image': upload_image,
    }
    return render(request, 'report.html', context=context)


def report_wr(request):
    context = {
        'test_name': request.session['test_name'],
        'result': request.session['result'],
        'confidence': request.session['confidence'],
        'patient_name': request.session['p_name'],
    }
    return render(request, "report_wr.html", context)


def report_wr_h(request):
    context = {
        'test_name': request.session['test_name'],
        'result': request.session['result'],
        'confidence': request.session['confidence'],
        'patient_name': request.session['p_name'],
    }
    return render(request, "report_wr_h.html", context)


def image_upload_view(request):
    test_list = []
    if request.method == 'POST':
        form = Image_Input_Forms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            global url
            for val in value:
                test = Test_Pathology.objects.get(some_test='{0}'.format(val))
                url = test.api_url
                length = len(Image_Input.objects.all())
                image = Image_Input.objects.filter(id=length)
                for img in image:
                    img = str(img)
                    sli = slice(16, -1)
                    img = img[sli] + "g"
                    import os
                cwd = os.getcwd() + os.sep + 'media' + os.sep + 'Patient_reports' + os.sep
                filename = cwd + img
                destination = os.getcwd() + os.sep + "Pathology" + os.sep + "static" + os.sep + "uploadImage" + os.sep + "upload.jpg"
                from shutil import copy
                copy(filename, destination)
                output = detect_image_label(filename, url)
                conf = str(output[2])

                import urllib.request
                urllib.request.urlretrieve(output[3],
                                           os.getcwd() + os.sep + "Pathology" + os.sep + "static" + os.sep + "heatmap" + os.sep + "heatmap.png")

                AI_Usecase_Occurences.objects.create(time=datetime.now(), Image_Output_1=output[1], confidence=conf,
                                                     heatmap="/home/kernel/shazan/11dec2019/Lab_Working_1/Pathology/static/heatmap/heatmap.png")
            return redirect('/report/')
    else:
        tests = Test_Pathology.objects.all()
        for test in tests:
            test_list.append(test)
        patients = Patient_Details.objects.all()
        length = len(patients) - 1
        patient_name = patients[length]
        form = Image_Input_Forms()

    return render(request, 'Image_Upload.html', {'form': form, 'patient_name': patient_name})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def patient_details_view(request):
    if request.method == 'POST':
        form = Patient_Details_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/test/')
    else:
        form = Patient_Details_Form()

    return render(request, 'patient_details.html', {'form': form})


def final_reports_view(request):
    return render(request, 'final_report_view.js')


def location_view(request):
    if request.method == 'POST':
        form = Location_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/report/')
    else:
        form = Location_Form()

    return render(request, 'location.html', {'form': form})


def test_view(request):
    if request.method == 'POST':
        form = Test_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/test/')
    else:
        form = Test_Form()
    return render(request, 'test.html', {'form': form})
