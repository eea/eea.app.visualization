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

  sections.tabs("div.chart-panes > div", {
    onClick: function(evt, index){
      var tab = this.getTabs()[index];
      var css = jQuery(tab).attr('class');
      if(css.indexOf('tab-daviz') !== -1){
        jQuery('.daviz-facets').show();
      }else{
        jQuery('.daviz-facets').hide();
      }
    }
  });
});
