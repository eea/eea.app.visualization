var DavizTableStyler = function(table, database){
  jQuery(table).addClass('listing');
};

var DavizTableRowStyler = function(item, database, tr) {
  if (tr.rowIndex % 2) {
    jQuery(tr).addClass('odd');
  } else {
    jQuery(tr).addClass('even');
  }
};

jQuery(document).ready(function(){
  var sections = jQuery("ul.chart-tabs");
  if(!sections.length){
    return;
  }

  var tabs = sections.tabs("div.chart-panes > div.daviz-tab-view", {
    history: true,
    onClick: function(evt, index){
      var api = this;
      var tab = this.getTabs()[index];
      jQuery(document).trigger('eea-daviz-tab-click', {
        index: index,
        tab: tab,
        api: api
      });
    }
  });

  var api = jQuery("ul.chart-tabs").data('tabs');
  jQuery(window).bind('hashchange', function(evt){
    jQuery.each(api.getTabs(), function(idx, tab){
      if(jQuery(tab).attr('href') == window.location.hash.split('_filters=')[0]){
        api.click(idx);
        return false;
      }
    });
  });

  jQuery("ul.chart-tabs a").click(function(){
    window.location.hash = jQuery(this).attr('href');
    return false;
  });

  jQuery(".daviz-tab-view-noscript").removeClass("daviz-tab-view-noscript");

});
