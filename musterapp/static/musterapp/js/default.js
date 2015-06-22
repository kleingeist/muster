// Get the Django csrftoken
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

// Apply the csrftoken to every POST method
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function(){
    /**
     * Base sidebar, login
     */
    $("#nav-left .bottom .login").click(function(){
        $("#login-modal").modal("show");
    });


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

            var $img = $this.find("img");
            console.log($img);
            console.log($img.attr("src"));
            $img.data("img-src", $img.attr("src"));
            $img.attr("src", $img.data("svg-src"));

        }, function(e) {
            var $this = $(this);
            var pattern_id = $this.data("pattern-id");
            var $rect = $("#pattern-" + pattern_id);
            var $classes = $this.data("svg-classes");

            $rect.attr("class", $classes);

            var $img = $this.find("img:first");
            $img.attr("src", $img.data("img-src"));
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


    /**
     * Favorites
     */
    $(".favorit").click(function(e){
        var $this = $(this);
        var target_id = $this.data("id");
        // TODO: get from html attribute
        var target_model = "musterapp.Pattern";
        var faved = $this.hasClass("faved");

        $this.prop('disabled', true);
        $.ajax({
            url: $this.data('href'),
            type: 'POST',
            data: {
                target_model: target_model,
                target_object_id: target_id
            },
            success: function (response) {
                if (response.status == 'added') {
                    $this.removeClass("unfaved");
                    $this.addClass("faved");
                }
                else {
                    $this.removeClass("faved");
                    $this.addClass("unfaved");
                }
                $this.prop('disabled', false);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                // TODO show error message
                $this.prop("disabled", false);
            }
        });
    });

});