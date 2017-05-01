$("document").ready(function(){
    var active_window = undefined;

    /* Search tags */
    $("#id_search").submit(function( event ) {
        event.preventDefault();
        if($(".search").val()) {
            $.get("/search/", {
                q: $( ".search" ).val()
            }, function(data) {
                var result = data["images"];
                $(".gallery > li").each(function(index) {
                    if(!result[index])
                        $(this).hide();
                    else {
                        $(this).show();
                        var img = $("img", this);
                        var title = $("#id_image_title", this);
                        img.attr("src", result[index]["media"]["m"] + "?timestamp=" + new Date().getTime());
                        title.text(result["title"]);
                    }
                });
            });
        }
    });

    /* Like/favorite photos */
    $(".heart.fa").click(function(event) {
        event.preventDefault();
        var element = $(this)
        $(this).attr("class", "heart fa fa-heart");
        var url = $(".like", this).attr("href");
        $.ajax({
            url: url,
            type: "GET",
            async: false,
            headers: {
              "Content-Type": "application/x-www-form-urlencoded"
            },
            data: {},
            success: function(data) {
                if(data["redirect_url"]) {
                    $(element).attr("class", "heart fa fa-heart-o")
                    if(active_window) {
                        active_window.close();
                    }
                    var win = window.open(data["redirect_url"], "_blank");
                    active_window = win;
                    win.focus();
                }
            }
        });
    });
});
