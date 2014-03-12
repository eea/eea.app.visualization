jQuery(document).ready(function(){
    var playlists = ["PLVPSQz7ahsByeq8nVKC7TT9apArEXBrV0", "PLVPSQz7ahsBxbe8pwzFWLQuvDSP9JFn8I"];
    jQuery("<iframe>")
        .attr("width", 580)
        .attr("height", 315)
        .attr("frameborder", 0)
        .attr("allowfullscreen", true)
        .attr("src", "")
        .appendTo("#daviz-tutorials")

    jQuery("<div>")
        .addClass("daviz-tutorials-main-playlist")
        .css("height", jQuery("#daviz-tutorials iframe").attr("height"))
        .appendTo("#daviz-tutorials")

    for (var i = 0; i < playlists.length; i++){
        jQuery.getJSON("http://gdata.youtube.com/feeds/api/playlists/" + playlists[i] + "?v=2&alt=jsonc&orderby=position", function(data){
            var div = jQuery("<div>")
                .addClass("daviz-tutorials-playlist")
                .attr("playlistid", data.data.id)
                .appendTo("#daviz-tutorials .daviz-tutorials-main-playlist")
            jQuery("<h2>")
                .text(data.data.title)
                .attr("href","https://www.youtube.com/playlist?list=" + data.data.id)
                .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "']")
            jQuery("<div style='clear:both'></div>")
                .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "']")
            jQuery("<div>")
                .addClass("daviz-tutorials-videos")
                .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "']");
            for (var j = 0; j < data.data.items.length; j++){
                var img = jQuery("<img>")
                    .attr("src", data.data.items[j].video.thumbnail.sqDefault)
                jQuery("<div>")
                    .text(data.data.items[j].video.title)
                    .attr("videoid", data.data.items[i].video.id)
                    .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "'] .daviz-tutorials-videos")
                    .prepend(img)
                    .click(function(){
                        jQuery("#daviz-tutorials iframe")
                            .attr("src", "http://www.youtube.com/embed/"+jQuery(this).attr("videoid")+"?autoplay=1")
                        jQuery(".nowplaying")
                            .removeClass("nowplaying")
                        jQuery(this)
                            .addClass("nowplaying")
                        });
                jQuery("<div style='clear:both'></div>")
                    .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "'] .daviz-tutorials-videos")
                if (jQuery("#daviz-tutorials iframe").attr("src") === ""){
                    jQuery(".daviz-tutorials-playlist[playlistid='" + data.data.id + "'] div[videoid='" + data.data.items[j].video.id + "']")
                        .addClass("nowplaying");
                    jQuery("#daviz-tutorials iframe")
                        .attr("src", "http://www.youtube.com/embed/"+data.data.items[j].video.id)
                }
            }
            jQuery("<div style='clear:both'></div>")
                .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "'] .daviz-tutorials-videos")
        });
    }
});