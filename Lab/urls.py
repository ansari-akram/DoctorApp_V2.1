from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from Pathology import views

urlpatterns = [
     path('admin/', admin.site.urls),
     path('', views.home, name='home'),
     path('register/', views.register, name='register'),
     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
     path('patient/', views.patient_details_view, name='patient'),
     path('image_upload/', views.image_upload_view, name='image_upload'),
     path('image_upload/<test_name>', views.image_upload_view, name='test_name'),
     path('report/', views.report_view, name='report'),
     path('location/', views.location_view, name='location'),
     path('test/', views.test_in_pathology, name='test'),
     path('final_report/', views.final_reports_view, name='final_report'),
     path('add_test/', views.test_view, name='add_test'),
     path('about_us/', views.about_us, name='about_us'),
     path('contact_us/', views.contact_us, name='contact_us'),
     path('create_pdf/<patient_name>', views.create_pdf, name="create_pdf"),
     path('analyze/', views.analyze, name="analyze"),
     path('image_upload_wr/<test_name>', views.image_upload_wr, name="image_upload_wr"),
     path('report_wr/', views.report_wr, name="report_wr"),
     path('report_wr_h/', views.report_wr_h, name="report_wr"),
]
