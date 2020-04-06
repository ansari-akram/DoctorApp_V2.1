var doc = new jsPDF('p', 'pt', 'letter');
var specialElementHandlers = {
    '#editor': function (element, renderer){
        return true;
    }
}

$('#cmd').click(function()
{
    var w = document.getElementById("content_id").offsetWidth;
    var h = document.getElementById("content_id").offsetHeight;
    html2canvas(document.getElementById("content_id"), {
    dpi: 300, scale: 3,
    onrendered: function (canvas) {

        var img = canvas.toDataURL("image/jpg", 1);
        var doc = new jsPDF('L', 'px', [w, h]);
        doc.addImage(img, 'JPG', 0, 0, w, h);
        var name = document.getElementById("pname").value
        doc.save(name + '_report.pdf');
        }
    });
});