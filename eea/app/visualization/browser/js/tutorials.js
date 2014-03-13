//TODO: move tags in youtube video descriptions
var video_tags = {
    "My first DaViz | DaViz tutorial" : ["create"],
    "Create DaViz - data via copy and paste | DaViz tutorial" : "create",
    "Create DaViz - data via CSV/TSV upload | DaViz tutorial" : "create",
    "Create DaViz - data from URL (external site) | DaViz tutorial" : "create",
    "Create DaViz - data from another DaViz | DaViz tutorial" : "create",
    "Create DaViz - data from SPARQL query (Linked Data) | DaViz tutorial" : "create",
    "Basic DaViz editing | DaViz tutorial" : "edit chart",
    "Add visualization - Bar chart | DaViz tutorial" : "edit chart, bar",
    "Add visualization - Column chart | DaViz tutorial" : "edit chart, column",
    "Basic chart customization | DaViz tutorial" : "edit chart, bar",
    "Add visualization - Pie chart | DaViz tutorial" : "edit chart, pie",
    "Add visualization - Line chart | DaViz tutorial" : "edit chart, line",
    "Add visualization - Map chart | DaViz tutorial" : "edit chart, map",
    "Rearrange charts | DaViz Tutorial" : "edit chart",
    "Add Visualisation - Chart with intervals | DaViz tutorial" : "edit chart, intervals",
    "Introduction to Exhibit visualizations | DaViz tutorial" : "exhibit",
    "Map view - Exhibit visualization | DaViz tutorial" : "exhibit, map",
    "Tabular view - Exhibit visualization | DaViz tutorial" : "exhibit, tabular",
    "Timeline view - Exhibit visualization | DaViz tutorial" : "exhibit, timeline",
    "Tile view - Exhibit visualization | DaViz tutorial" : "exhibit, tile",
    "Lens - Exhibit visualization | DaViz tutorial" : "exhibit, lens",
    "Facets - Exhibit visualization | DaViz tutorial" : "exhibit, facets",
    "Hide/Show table columns - Using the table configurator | DaViz tutorial" : "edit chart, table, hide/show",
    "Table formatters - Using the table configurator | DaViz tutorial" : "edit chart, table, formatters",
    "Unpivot table - Using the table configurator | DaViz tutorial" : "edit chart, table, unpivot",
    "Pivot table - Using the table configurator | DaViz tutorial" : "edit chart, table, pivot",
    "Filter - Using the table configurator | DaViz tutorial" : "edit chart, table, rowfilters",
    "Scatterplots matrix - Using the table configurator | DaViz tutorial" : "edit chart, table, scatterplots, matrices",
    "Other matrices - Using the table configurator | DaViz tutorial" : "edit chart, table, others, matrices",
    "Adding Filters, sorting and chart notes - Interactive charts | DaViz tutorial" : "edit chart, filters, notes, sort",
    "Creating dashboards - Combine multiple charts in a dashboard | DaViz tutorial" : "edit dashboard",
    "Embed charts or dashboards in other sites - Embedding in webpages | DaViz tutorial" : "view, embed, chart, dashboard",
    "Keep chart's filter settings when embedding - Embedding in webpages | DaViz tutorial" : "view, embed, chart, dashboard, filters",
    "Embed a static image - Embedding in webpages | DaViz tutorial" : "view, embed, chart",
    "Customize CSS when embedding - Embedding in webpages | DaViz tutorial" : "view, embed, csscustomization",
    "Embed and use DaViz in EEA indicators | DaViz tutorial" : "view, embed, chart, dashboard, indicators"
};

function updateTagCloud(tags){
    tag_data = jQuery(".daviz-tutorials-tagcloud").data("tags");
    for (i = 0; i < tags.length; i++) {
        var tag = tags[i].trim();
        if (tag !== "") {
            if (tag_data[tag] === undefined) {
                tag_data[tag] = 0;
            }
            tag_data[tag] ++;
        }
    }
    jQuery(".daviz-tutorials-tagcloud").data("tags", tag_data);
    var sorted_tags = [];
    jQuery.each(tag_data, function(key, value){
        sorted_tags.push({tag:key, count:value});
    });
    sorted_tags.sort(function (a,b){
        if (a.count > b.count) {
            return -1;
        }
        else if (a.count < b.count) {
            return 1;
        }
        else {
            return 0;
        }
    });
    jQuery(".daviz-tutorials-tagcloud")
        .empty();
    for (i=0; i<sorted_tags.length; i++){
        jQuery("<a>")
            .css("text-decoration", "none")
            .attr("tag", sorted_tags[i].tag)
            .attr("href", "daviz-tutorials.html#" + sorted_tags[i].tag)
            .text(sorted_tags[i].tag + "(" + sorted_tags[i].count+ ") ")
            .appendTo(".daviz-tutorials-tagcloud");
    }
}

jQuery(document).ready(function(){
    jQuery(window).bind('hashchange', function(evt){
        var hash = window.location.hash;
        if (hash === "") {
            hash = "#all tutorials";
        }
        hash = hash.substr(1);
        jQuery(".daviz-tutorials-tagcloud a")
            .removeClass("selected");
        jQuery(".daviz-tutorials-tagcloud a[tag='" + hash + "']")
            .addClass("selected");
        jQuery(".daviz-tutorials-videoitem")
            .addClass("hidden-item")
            .removeClass("nowplaying");
        jQuery("#daviz-tutorials iframe")
            .attr("src", "");
        jQuery.each(jQuery(".daviz-tutorials-videoitem"), function(idx, item){
            item = jQuery(item);
            if (jQuery.inArray(hash, item.data("tags")) !== -1) {
                if (jQuery("#daviz-tutorials iframe").attr("src") === ""){
                    item.addClass("nowplaying");
                    jQuery("#daviz-tutorials iframe")
                        .attr("src", "http://www.youtube.com/embed/"+item.attr("videoid"));
                }
                item.removeClass("hidden-item");
            }
        });
    });

    jQuery(window).trigger('hashchange');
    var playlists = ["PLVPSQz7ahsByeq8nVKC7TT9apArEXBrV0", "PLVPSQz7ahsBxbe8pwzFWLQuvDSP9JFn8I"];
    jQuery("<iframe>")
        .attr("width", 580)
        .attr("height", 315)
        .attr("frameborder", 0)
        .attr("allowfullscreen", true)
        .attr("src", "")
        .appendTo("#daviz-tutorials");

    jQuery("<div>")
        .addClass("daviz-tutorials-search")
        .css("height", jQuery("#daviz-tutorials iframe").attr("height"))
        .appendTo("#daviz-tutorials");

    jQuery("<div>")
        .addClass("daviz-tutorials-tagcloud")
        .data("tags", {})
        .css("height", 100)
        .appendTo(".daviz-tutorials-search");

    jQuery("<div>")
        .addClass("daviz-tutorials-main-playlist")
        .css("height", jQuery("#daviz-tutorials iframe").attr("height") - 100)
        .appendTo(".daviz-tutorials-search");

    jQuery.each(playlists, function(playlist_idx, playlist){
        jQuery.getJSON("http://gdata.youtube.com/feeds/api/playlists/" + playlist + "?v=2&alt=jsonc&orderby=position", function(data){
            var div = jQuery("<div>")
                .addClass("daviz-tutorials-playlist")
                .attr("playlistid", data.data.id)
                .appendTo("#daviz-tutorials .daviz-tutorials-main-playlist");
            jQuery("<div>")
                .addClass("daviz-tutorials-videos")
                .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "']");
            jQuery.each(data.data.items, function(item_idx, item){
                var description = [item.video.description, video_tags[item.video.title]].join(",");
                var tmp_tags = description.split(",");
                tmp_tags.push("all tutorials");
                var tags = [];
                for (i = 0; i < tmp_tags.length; i++) {
                    var tag = tmp_tags[i].trim();
                    if (tag !== "") {
                        tags.push(tag);
                    }
                }
                updateTagCloud(tags);
                var img = jQuery("<img>")
                    .attr("src", item.video.thumbnail.sqDefault);
                var item_obj = jQuery("<div>")
                    .addClass("daviz-tutorials-videoitem")
                    .addClass("hidden-item")
                    .data("tags", tags)
                    .attr("videoid", item.video.id)
                    .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "'] .daviz-tutorials-videos")
                    .click(function(){
                        jQuery("#daviz-tutorials iframe")
                            .attr("src", "http://www.youtube.com/embed/"+jQuery(this).attr("videoid")+"?autoplay=1");
                        jQuery(".nowplaying")
                            .removeClass("nowplaying");
                        jQuery(this)
                            .addClass("nowplaying");
                    })
                    .prepend(img);
                jQuery("<div>")
                    .text(item.video.title)
                    .appendTo(item_obj);
            });
            jQuery(window).trigger('hashchange');
        });
    });
});
