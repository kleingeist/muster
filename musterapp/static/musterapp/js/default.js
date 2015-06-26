// Get the Django csrftoken
var csrftoken = Cookies.get('csrftoken');

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
     * Base sidebar, login and fold/unfold
     */
    $("#nav-left .bottom .login").click(function(){
        $("#login-form").modal("show");
    });

    $("#nav-left p.fold-button").click(function(){
        var $content = $("#gravatar").parent().parent();
        $content.siblings().each(function() {
            $(this).toggleClass('hidden');
        });

        $("#fold-button").toggleClass('down');

        if (Cookies.get('folded') == 'true') {
            Cookies.remove('folded');
        } else {
            Cookies.set('folded', 'true');
        }
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


    /**
     * Search
     */
    $("#search-form .filter").on("change", function(e) {
       $("#search-form").submit();
    });



    /**
     * Tag Adding
     */
    $(".tags-editable").each(function() {
        var $container = $(this);
        var $form = $container.find(".tag-add-form").first();

        var $button = $form.find(".tag-add-button").first();
        var $input = $form.find(".tag-add-input").first();

        function show() {
            $button.prop('disabled', true);
            $input.show().focus();
        }

        function hide() {
            $input.hide().val("");
            $button.prop('disabled', false);
        }

        function abort() {
            hide();
        }

        function submit(value) {
            $.ajax({
                url: $form.data("action"),
                type: 'POST',
                data: {
                    tag: value,
                },
                success: function(response) {
                    console.log(response);

                    if (response.created) {
                        $container.find(".tags").append(" " + response.html);
                    }
                    hide();
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(thrownError);
                    hide();
                }
            });
        }


        $button.click(function() {
           show();
        });

        $input
            .on("focusout", function(e) {
                abort();
            })
            .on("keydown", function(event) {
                if (event.which == 13) {
                    event.preventDefault();
                    submit($input.val());
                }
                if (event.which == 27) {
                    event.preventDefault();
                    abort();
                }
            })
            .autoGrowInput({
                comfortZone: 20
            })
            .autocomplete({
                lookup: tag_list_all,
                triggerSelectOnValidInput: false,
                tabDisabled: true,
                onSelect: function (value) {
                    console.log(value);
                }
            })
        ;
    });
});