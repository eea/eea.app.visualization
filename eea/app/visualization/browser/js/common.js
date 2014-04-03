if(window.EEA === undefined){
  var EEA = {'version': 'eea.app.visualization'};
}

if(EEA.Daviz === undefined){
  EEA.Daviz = {'version': 'eea.app.visualization'};
}

EEA.Daviz.ColumnMenu = function(options){

  var settings = {
    columnType: '',
    annotations: false,
    rename: true
  };

  if(options){
    jQuery.extend(settings, options);
  }

  var menu = {};
  var items = [];

  if(settings.columnType === 'annotations'){
    items = [
      {
        title: "Delete",
        command: "delete",
        tooltip: "Delete annotations"
      },
      {
      title: "Column type:",
      tooltip: "Select column-type",
      iconCssClass: "slick-header-menusection",
      disabled: true
      },
      {
        title: 'Annotations',
        command: 'annotations',
        tooltip: "Convert this column to boolean",
        iconCssClass: "slick-header-menusectionitem",
        disabled: true,
        iconImage: "++resource++slickgrid-images/tick.png"
      }
    ];
  }else{
    items = [
      {
        title: "Column type:",
        tooltip: "Select column-type",
        iconCssClass: "slick-header-menusection",
        disabled: true
      },
      {
        title: 'Boolean',
        command: 'boolean',
        tooltip: "Convert this column to boolean",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "boolean"),
        iconImage: (settings.columnType === "boolean") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: 'Date',
        command: 'date',
        tooltip: "Convert this column to date",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "date"),
        iconImage: (settings.columnType === "date") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: 'Latitude',
        command: 'latitude',
        tooltip: "Convert this column to latitude",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "latitude"),
        iconImage: (settings.columnType === "latitude") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: 'Longitude',
        command: 'longitude',
        tooltip: "Convert this column to longitude",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "longitude"),
        iconImage: (settings.columnType === "longitude") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: 'LatLong',
        command: 'latlong',
        tooltip: "Convert this column to latlong",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "latlong"),
        iconImage: (settings.columnType === "latlong") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: 'List',
        command: 'list',
        tooltip: "Convert this column to list",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "list"),
        iconImage: (settings.columnType === "list") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: "Number",
        command: "number",
        tooltip: "Convert this column to number",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "number"),
        iconImage: (settings.columnType === "number") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: 'Text',
        command: "text",
        tooltip: "Convert this column to text",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "text"),
        iconImage: (settings.columnType === "text") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: 'URL',
        command: "url",
        tooltip: "Convert this column to URL",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "url"),
        iconImage: (settings.columnType === "url") ? "++resource++slickgrid-images/tick.png" : ""
      },
      {
        title: 'Year',
        command: "year",
        tooltip: "Convert this column to year",
        iconCssClass: "slick-header-menusectionitem",
        disabled: (settings.columnType === "year"),
        iconImage: (settings.columnType === "year") ? "++resource++slickgrid-images/tick.png" : ""
      }
    ];
  }

  if(settings.rename){
    items.splice(0, 0, {
      title: "Rename",
      command: "rename",
      tooltip: "Give this column a friendly name"
    });
  }

  if(settings.annotations){
    items.splice(1, 0, {
      title: "Annotations",
      command: "annotations",
      tooltip: "Extract annotations for this column"
    });
  }

  menu.items = items;
  return menu;
};

EEA.Daviz.Status = {
  initialize: function(){
    this.area = jQuery('body');
    this.area.append(jQuery('<div>').addClass('daviz-cleanup'));
    this.lock = jQuery('<div>').addClass('daviz-status-lock');
    this.message = jQuery('<div>').addClass('daviz-ajax-loader');
    this.lock.prepend(this.message);
    this.area.prepend(this.lock);
    this.lock.slideUp();
  },

  start: function(msg){
    if(!this.message){
      this.initialize();
    }
    this.message.html(msg);
    this.lock.slideDown();
  },

  stop: function(msg){
    if(!this.message){
      this.initialize();
    }
    this.message.html(msg);
    this.lock.delay(1500).slideUp();
  }
};
