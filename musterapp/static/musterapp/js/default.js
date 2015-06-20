$(document).ready(function(){

    /**
     * Page Browser
     */
    $("#page-browser rect").click(function(e){
        var $content = $("#" + e.target.id + "-content");
        $content.modal("show");
    });


    $(".modal-centered").on("show.bs.modal", function() {
        $(this).css('display', 'flex');
    });

    $(".pattern-sb").hover(
        function(e) {
            var $this = $(this);
            var pattern_id = $this.data("pattern-id");
            var $rect = $("#pattern-" + pattern_id);
            var $classes = $rect.attr("class");
            $this.data("svg-classes", $classes);

            $rect.attr("class", $classes + " highlight");
        }, function(e) {
            var $this = $(this);
            var pattern_id = $this.data("pattern-id");
            var $rect = $("#pattern-" + pattern_id);
            var $classes = $this.data("svg-classes");

            $rect.attr("class", $classes);
        }
    );

    /**
     * Sidebar Left
     */
    $("#sidebar-left .volume-cat .name").click(function() {
        $(this).next().toggleClass('hidden');
    });

    $("#sidebar-left .volume-list .volume a").hover(
        function () {
            $(this).addClass("hover");
        },
        function () {
            $(this).removeClass("hover");
        });


});