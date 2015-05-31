$(document).ready(function(){

    var $full = $("#page-browser-full");
    var $image = $full.find(".image");
    var $zoom = $image.find(".zoom");
    var $img = $zoom.find("img");

    $panzoom = $zoom.panzoom({
       // contain: "invert",
    });

    $zoom.on('mousewheel.focal', function (e) {
        e.preventDefault();
        var delta = e.delta || e.originalEvent.wheelDelta;
        var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
        $panzoom.panzoom('zoom', zoomOut, {
            increment: 0.1,
            animate: false,
            focal: e
        });
    });

    $panzoom.on('panzoomend', function (e, panzoom, matrix, changed) {
        if (!changed) {
            $full.hide();
        }
        return false;
    });

    $("#page-browser .page a").click(function (event) {
        $img[0].src = $img.data("src");
        $full.show();
        return false;
    });


});