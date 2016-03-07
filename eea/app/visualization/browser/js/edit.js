if(window.DavizEdit === undefined){
  var DavizEdit = {'version': '4.0'};
}

/** Events
*/
DavizEdit.Events = DavizEdit.Events || {};
DavizEdit.Events.facet = {
  changed: 'daviz-facet-changed',
  deleted: 'daviz-facet-deleted',
  refresh: 'daviz-facets-refresh',
  refreshed: 'daviz-facets-refreshed'
};

DavizEdit.Events.views = {
  refresh: 'daviz-views-refresh',
  refreshed: 'daviz-views-refreshed',
  clicked: 'daviz-view-clicked'
};

DavizEdit.Events.table = {
  change: 'daviz-table-change',
  changed: 'daviz-table-changed'
};

/** Status
*/
DavizEdit.Status = {
  initialize: function(){
    this.area = jQuery('.daviz-settings');
    this.area.append(jQuery('<div>').addClass('daviz-cleanup'));
    this.lock = jQuery('<div>').addClass('daviz-status-lock');
    this.message = jQuery('<div>').addClass('daviz-ajax-loader');
    this.lock.prepend(this.message);
    this.area.prepend(this.lock);
    this.lock.slideUp();
  },

  start: function(msg){
    this.message.html(msg);
    this.lock.slideDown();
  },

  stop: function(msg){
    this.message.html(msg);
    this.lock.delay(1500).slideUp();
  }
};


/** Confirm dialog
*/
DavizEdit.Confirm = {
  initialize: function(){
    var self = this;
    self.event = null;
    self.kwargs = {};

    self.area = jQuery('<div>').addClass('daviz-confirm').attr('title', 'Confirm');
    jQuery('daviz-views-edit').after(self.area);
    self.area.dialog({
      bgiframe: true,
      autoOpen: false,
      modal: true,
      dialogClass: 'daviz-confirm-overlay',
      open: function(evt, ui){
        var buttons = jQuery(this).parent().find("button[title!='close']");
        buttons.attr('class', 'btn');
        jQuery(buttons[0]).addClass('btn-danger');
        jQuery(buttons[1]).addClass('btn-inverse');
      },
      buttons:  {
        Yes: function(){
          if(self.event !== null){
            jQuery(document).trigger(self.event, self.kwargs);
          }
          jQuery(this).dialog('close');
        },
        No: function(){
          jQuery(this).dialog('close');
        }
      }
    });
  },

  confirm: function(msg, event, kwargs){
    var self = this;
    self.area.html(msg);
    self.event = event;
    self.kwargs = kwargs;
    self.area.dialog('open');
  }
};


/** Facets
*/
DavizEdit.Facets = {
  initialize: function(){
    var self = this;
    self.facets = {};
    self.area = jQuery('.daviz-facets-edit').addClass('daviz-facets-edit-ajax');

    // Events
    jQuery(document).unbind('.DavizEditFacets');
    jQuery(document).bind(DavizEdit.Events.facet.deleted + '.DavizEditFacets', function(evt, data){
      self.handle_delete(data);
    });

    jQuery(document).bind(DavizEdit.Events.facet.refresh + '.DavizEditFacets', function(evt, data){
      self.handle_refresh(data);
    });

    jQuery(document).bind(DavizEdit.Events.views.clicked + '.DavizEditFacets', function(evt, data){
      self.handle_tab(data);
    });

    jQuery(document).trigger(DavizEdit.Events.facet.refresh + '.DavizEditFacets', {init: true});
  },

  handle_refresh: function(data){
    var self = this;
    if(data.init){
      self.setup();
    }else{
      var action = data.action;
      var i = action.indexOf('@@');
      action = action.slice(0, i) + '@@daviz-edit.facets.html';
      DavizEdit.Status.start('Refreshing ...');
      jQuery.get(action, {}, function(data){
        self.area.html(data);
        self.setup();
        DavizEdit.Status.stop("Done");
        jQuery(document).trigger(DavizEdit.Events.facet.refreshed);
      });
    }
  },

  setup: function(){
    var self = this;
    // Add box
    jQuery('.daviz-facet-add', self.area).each(function(){
      var facet = jQuery(this);
      var add = new DavizEdit.FacetAdd(facet);
    });

    // Facets
    jQuery('.daviz-facet-edit', self.area).each(function(){
      var facet = jQuery(this);
      self.facets[facet.attr('id')] = new DavizEdit.Facet(facet);
    });

    // Sortable
    jQuery('.daviz-facets-edit-ajax').sortable({
      items: '.daviz-facet-edit',
      placeholder: 'ui-state-highlight',
      forcePlaceholderSize: true,
      opacity: 0.7,
      delay: 300,
      cursor: 'crosshair',
      tolerance: 'pointer',
      update: function(event, ui){
        self.sort(ui.item.parent());
      }
    });
  },

  sort: function(context){
    facets = jQuery('.facet-title', context);
    var order = jQuery.map(facets, function(value){
      return jQuery(value).text();
    });

    var action = jQuery('form', context).attr('action');
    var index = action.indexOf('@@');
    action = action.slice(0, index) + '@@daviz-edit.save';

    query = {'daviz.facets.save': 'ajax', order: order};
    DavizEdit.Status.start('Saving ...');
    jQuery.ajax({
      traditional: true,
      type: 'post',
      url: action,
      data: query,
      success: function(data){
        DavizEdit.Status.stop(data);
      }
    });
  },

  handle_delete: function(kwargs){
    var self = this;
    var facet = kwargs.facet;
    var name = facet.attr('id');

    var action = jQuery('form', facet).attr('action');
    var i = action.indexOf('@@');
    action = action.slice(0, i) + '@@daviz-edit.save';
    var query = {'daviz.facet.delete': 'ajax', name: name};

    facet.slideUp(function(){
      DavizEdit.Status.start('Saving ...');
      jQuery.ajax({
        traditional: true,
        type: 'post',
        url: action,
        data: query,
        success:  function(data){
          DavizEdit.Status.stop(data);
          var currentTab = 0;
          var tabs = jQuery('.daviz-views-edit ul');
          var tab = null;
          if(tabs.length){
            tabs = tabs.data('tabs');
            currentTab = tabs.getIndex();
            tab = tabs.getCurrentTab();
          }

          jQuery(document).trigger(DavizEdit.Events.views.refresh, {
            init: false,
            action: jQuery('form', facet).attr('action'),
            currentTab: currentTab,
            tab: tab
          });

          facet.remove();
          delete self.facets[name];
        }
      });
    });
  },

  handle_tab: function(kwargs){
    var self = this;
    var href = jQuery(kwargs.tab).attr('href');

    if(!href){
      return self.area.hide();
    }

    if(href === '#daviz-properties-tab'){
      return self.area.hide();
    }

    if(href.indexOf('#daviz-') !== 0){
      return self.area.hide();
    }

    if(jQuery(href + ' .daviz-view-form-disabled').length){
      return self.area.hide();
    }

    return self.area.show();
  }
};

/** Add facets box
*/
DavizEdit.FacetAdd = function(facet){
  this.initialize(facet);
};

DavizEdit.FacetAdd.prototype = {
  initialize: function(facet){
    var self = this;
    self.facet = facet;
    self.form = jQuery('form', facet);
    self.action = self.form.attr('action');
    self.button = jQuery("input[type='submit']", this.form).hide();

    self.form.submit(function(evt){
      evt.preventDefault();
      return false;
    });

    self.form.dialog({
      bgiframe: true,
      autoOpen: false,
      modal: true,
      dialogClass: 'daviz-facet-add-overlay',
      buttons:  {
        Add: function(){
          self.submit();
          jQuery(this).dialog('close');
        },
        Cancel: function(){
          jQuery(this).dialog('close');
        }
      }
    });

   var plus = jQuery("<span>")
      .attr('title', 'Add new facet')
//      .text('+')
      .addClass('eea-icon').addClass('eea-icon-plus').addClass('ui-corner-all');

    self.facet.prepend(plus);

    plus.click(function(){
      self.form.dialog('open');
    });
  },

  submit: function(){
    var self = this;
    var name = self.button.attr('name');
    var query = name + '=ajax&';
    query += self.form.serialize();

    DavizEdit.Status.start('Adding ...');
    jQuery.ajax({
      traditional: true,
      type: 'post',
      url: self.action,
      data: query,
      success: function(data){
        DavizEdit.Status.stop(data);
        jQuery(document).trigger(DavizEdit.Events.facet.refresh, {
          init: false, action: self.action});
      }
    });
  }
};


/** Facet
*/
DavizEdit.Facet = function(facet){
  this.initialize(facet);
};

DavizEdit.Facet.prototype = {
  initialize: function(facet){
    var self = this;
    this.facet = facet;
    this.form = jQuery('form', facet);
    this.action = this.form.attr('action');
    this.button = jQuery("input[type='submit']", this.form);
    this.button.hide();

    var show = jQuery("div.field:has([id$='.show'])", this.form).hide();
    this.show = jQuery("[id$='.show']", show);
    this.visible = this.show.attr('checked');

    var title = jQuery('h1', this.form);
    title.attr('title', 'Click and drag to change widget position');

    var html = title.html();
    var newhtml = jQuery('<div>').addClass('facet-title').html(html);
    title.html(newhtml);

    this.hide_icon(title);
    this.delete_icon(title);

    this.form.submit(function(){
      return false;
    });

    // Events
    jQuery(document).unbind('.' + self.facet.attr('id'));
    jQuery(document).bind(DavizEdit.Events.facet.changed + '.' + self.facet.attr('id'), function(evt, data){
      self.submit(data);
    });

    jQuery(':input', this.form).change(function(){
      var form = jQuery(this).parents('form');
      var label = jQuery("input[name*='.label']", form);
      var key = label.attr('name').replace('.label', '');
      var value = label.val();

      jQuery(document).trigger(DavizEdit.Events.facet.changed, {
        key: key,
        value: value,
        trigger: jQuery(this)
      });
      return false;
    });
  },

  hide_icon: function(title){
    var self = this;

    var msg = 'Hide facet';
    var css = 'eea-icon-eye';
    if(!self.visible){
      msg = 'Show facet';
      css = 'eea-icon-eye-slash';
      title.addClass('hidden');
    }
    var icon = jQuery('<div>')
      .attr('title', msg)
      .addClass('eea-icon daviz-menuicon')
      .addClass(css);

    icon.click(function(){
      if(self.visible){
        self.visible = false;
        icon.removeClass('eea-icon-eye')
          .addClass('eea-icon-eye-slash')
          .attr('title', 'Show facet');
          title.addClass('hidden');
      }else{
        self.visible = true;
        icon.removeClass('eea-icon-eye-slash')
          .addClass('eea-icon-eye')
          .attr('title', 'Hide facet');
          title.removeClass('hidden');
      }
      self.show.click();
      self.submit();
    });
    title.prepend(icon);
  },

  delete_icon: function(title){
    var self = this;
    var icon = jQuery('<div>')
      .attr('title', 'Delete facet')
      .addClass('eea-icon daviz-menuicon')
      .addClass('eea-icon-trash-o');

    icon.click(function(){
      var msg = "Are you sure you want to delete facet: <strong>" + self.facet.attr('id') + "</strong>. ";
      msg += "You should consider hiding it, instead of deleting it, otherwise ";
      msg += "you'll have to manually update Views properties if this facet id is used by any of them.";
      DavizEdit.Confirm.confirm(msg, DavizEdit.Events.facet.deleted, {facet: self.facet});
    });

    title.prepend(icon);
  },

  submit: function(options){
    var self = this;

    if(options){
      var label = jQuery("input[name='" + options.key + ".label']", this.form);
      if(!label.length){
        return;
      }
      label.val(options.value);
    }

    var name = this.button.attr('name');
    var query = name + '=ajax&';
    query += this.form.serialize();

    DavizEdit.Status.start('Saving ...');
    jQuery.ajax({
      traditional: true,
      type: 'post',
      url: self.action,
      data: query,
      success: function(data){
        DavizEdit.Status.stop(data);
        if(options && options.trigger && options.trigger.attr('name').indexOf('.type') !== -1){
          var action = self.form.attr('action');
          jQuery(document).trigger(DavizEdit.Events.facet.refresh, {
            init: false, action: action
          });
        }
      }
    });
  }
};

/** Views
*/
DavizEdit.Views = {
  initialize: function(){
    var self = this;

    jQuery(document).unbind('.DavizEditViews');
    jQuery(document).bind(DavizEdit.Events.views.refresh + '.DavizEditViews', function(evt, data){
      self.update_views(data);
    });
    jQuery(document).trigger(DavizEdit.Events.views.refresh, {
      init: true,
      action: jQuery('.daviz-views-edit form').attr('action'),
      currentTab: 0,
      tab: null
    });
  },

  update_views: function(form){
    var self = this;
    self.views = {};
    self.area = jQuery('.daviz-views-edit').addClass('daviz-views-edit-ajax');
    var action = form.action;
    var i = action.indexOf('@@');
    action = action.slice(0, i) + '@@daviz-edit.views.html';

    if(!form.init){
      DavizEdit.Status.start('Refreshing ...');
      jQuery.get(action, {}, function(data){
        self.area.html(data);
        self.update_tabs(action);
        jQuery(document).trigger(DavizEdit.Events.views.refreshed, form);
        DavizEdit.Status.stop("Done");
      });
    }else{
      self.update_tabs(action);
    }
  },

  update_tabs: function(action){
    var self = this;
    jQuery('.daviz-view-edit', self.area).each(function(){
      var view = jQuery(this);
      self.views[view.attr('id')] = new DavizEdit.View(view);
    });
    jQuery('fieldset', self.area).addClass('daviz-edit-fieldset');
    jQuery('form.daviz-view-form h1', self.area).hide();

    // Make tabs
    var ul = jQuery('ul.formTabs', self.area);
    ul.tabs('div.panes > div', {
      onClick: function(evt, index){
        var api = this;
        var tab = this.getTabs()[index];
        jQuery(document).trigger(DavizEdit.Events.views.clicked, {
          index: index,
          tab: tab,
          api: api
        });
      }
    });

    // Make tabs sortable
    jQuery('li', ul)
      .attr('title', 'Click and drag to change tabs order');
    ul.sortable({
      items: 'li.formTab',
      placeholder: 'formTab ui-state-highlight',
      cursor: 'crosshair',
      tolerance: 'pointer',
      delay: 300,
      update: function(event, ui){
        var order = jQuery('li', ul);
        self.sort(order, action);
      }
    });

    jQuery(document).bind(DavizEdit.Events.views.refreshed + '.DavizEditViews', function(evt, data){
      var index = data.currentTab || 0;
      var tab = data.tab;
      var tabs = jQuery('ul', self.area).data('tabs');
      if(tab){
        jQuery.each(tabs.getTabs(), function(i, item){
          if(jQuery(tab).attr('href') == jQuery(item).attr('href')){
            tabs.click(i);
            return false;
          }
        });
      }else{
        tabs.click(index);
      }
    });
  },

  sort: function(order, action){
    var self = this;
    var i = action.indexOf('@@');
    action = action.slice(0, i) + '@@daviz-edit.save';

    order = jQuery.map(order, function(item){
      return jQuery(item).attr('data-name');
    });

    var query = {
      'daviz.views.save': 'ajax',
      order: order
    };

    DavizEdit.Status.start('Saving ...');
    jQuery.ajax({
      traditional: true,
      type: 'post',
      url: action,
      data: query,
      success: function(data){
       DavizEdit.Status.stop(data);
      }
    });
  }
};

/** View settings
*/
DavizEdit.View = function(view){
  this.initialize(view);
};

DavizEdit.View.prototype = {
  initialize: function(view){
    var self = this;
    self.view = view;
    self.form = jQuery('form.daviz-view-form', self.view);
    if(!self.form.length){
      self.form = jQuery('form.daviz-view-form-disabled', self.view);
    }

    //
    // Data settings tab
    //

    // Table
    self.jsondata = jQuery("div.field:has(label[for='daviz.properties.json'])", self.form);
    if(self.jsondata.length){
      var jsondata = new DavizEdit.JsonGrid(self.jsondata);
    }

    // Additional sources
    self.table = jQuery("div:has(label[for='daviz.properties.sources']) table", self.form);
    if(self.table.length){
      self.table.addClass('daviz-sources-table');
      var table = new DavizEdit.SourceTable(self.table);
    }

    // Annotations
    if(self.form.attr('data-annotations')){
      self.form.data('annotations', JSON.parse(self.form.attr('data-annotations')));
      self.form.removeAttr('data-annotations');
    }

    self.form.submit(function(evt){
      evt.preventDefault();
      return false;
    });

    self.buttons = jQuery(".actionButtons input[type='submit']", self.form);
    self.buttons.click(function(evt, args){
      var button = jQuery(this);
      self.submit(button);
    });

    self.buttons.each(function(){
      if(jQuery(this).attr('name') == 'daviz.view.enable'){
        return;
      }
      jQuery(this).addClass('btn').addClass('btn-large');
      if(jQuery(this).attr('name').indexOf('.disable') !== -1){
        jQuery(this).addClass('btn-danger');
      }
      if(jQuery(this).attr('name').indexOf('.save') !== -1){
        jQuery(this).addClass('btn-success');
      }
    });

    self.inputs = jQuery(':input', self.form).change(function(evt){
      jQuery('fieldset', self.form).addClass('changed');
    });

    self.style();
  },

  style: function(){
    // Add links to URLs
    var self = this;
    var help = jQuery('.formHelp', this.view);
    help.each(function(){
      var here = jQuery(this);
      var text = self.replaceURL(here.text());
      here.html(text);
    });
  },

  replaceURL: function(inputText) {
    var replacePattern = /(\b(https?|ftp):\/\/[\-A-Z0-9+&@#\/%?=~_|!:,.;]*[\-A-Z0-9+&@#\/%=~_|])/gim;
    return inputText.replace(replacePattern, '<a href="$1" target="_blank">here</a>');
  },

  submit: function(button){
    var self = this;
    if(!button.hasClass('btn-danger')){
      return self.onSubmit(button);
    }

    jQuery('<div>')
      .html(['',
        '<span>',
          'This will ',
          '<strong>erase</strong> ',
          'all configuration settings for this visualization.',
        '</span><span>',
          'Are you sure that you want to',
          '<strong>disable</strong>',
          'it? ',
        '</span>'
        ].join('\n'))
      .dialog({
        title: 'Disable visualization',
        modal: true,
        dialogClass: 'daviz-confirm-overlay',
        open: function(evt, ui){
          var buttons = jQuery(this).parent().find("button[title!='close']");
          buttons.attr('class', 'btn');
          jQuery(buttons[0]).addClass('btn-danger');
          jQuery(buttons[1]).addClass('btn-inverse');
        },
        buttons: {
          Yes: function(){
            self.onSubmit(button);
            jQuery(this).dialog('close');
          },
          No: function(){
            jQuery(this).dialog('close');
          }
        }
      });
  },

  onSubmit: function(button){
    var self = this;
    var action = self.form.attr('action');
    var query = {};
    var array = self.form.serializeArray();

    jQuery.each(array, function(){
      if(query[this.name]){
        query[this.name].push(this.value);
      }else{
        query[this.name] = [this.value];
      }
    });

    var name = button.attr('name');
    query[name] = 'ajax';

    DavizEdit.Status.start('Saving ...');
    jQuery.ajax({
      traditional: true,
      type: 'post',
      url: action,
      data: query,
      success: function(data){
        jQuery('fieldset', self.form).removeClass('changed');
        button.removeClass('submitting');
        DavizEdit.Status.stop(data);
        if((name === 'daviz.properties.actions.save') || (name.indexOf('.enable') !== -1) || (name.indexOf('.disable') !== -1)){
          var currentTab = 0;
          var tabs = jQuery('.daviz-views-edit ul');
          var tab = null;
          if(tabs.length){
            tabs = tabs.data('tabs');
            currentTab = tabs.getIndex();
            tab = tabs.getCurrentTab();
          }

          jQuery(document).trigger(DavizEdit.Events.views.refresh, {
            init: false,
            action: action,
            currentTab: currentTab,
            tab: tab
          });
        }
      }
    });
  }
};

DavizEdit.Annotations = function(context, options){
  var self = this;
  self.context = context;
  self.settings = {};

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

DavizEdit.Annotations.prototype = {
  initialize: function(){
    var self = this;

    var annotations = [];
    self.all = self.context.closest('.daviz-view-form').data('annotations') || [];

    if(self.settings.column.indexOf('__annotations__') !== -1){
      self.settings.column = self.settings.column.replace('__annotations__', '');
    }

    self.target = self.settings.table.properties[self.settings.column];

    if(!self.settings.table.properties[self.settings.column + '__annotations__']){
      var order = 0;
      var properties = {};
      jQuery.each(self.settings.table.properties, function(key, val){
        val.order = order;
        order += 1;
        properties[key] = val;
        if(key == self.settings.column){
          properties[self.settings.column + '__annotations__'] = {
            valueType: 'text',
            columnType: 'annotations',
            column: self.settings.column,
            label: self.target.label + ':annotations',
            order: order,
            annotations: jQuery.extend([], self.all)
          };
          order += 1;
        }
      });
      self.settings.table.properties = properties;
    }

    self.annotations = self.settings.table.properties[self.settings.column + '__annotations__'];

    self.grid = null;

    jQuery(document).bind('keydown.DavizAnnotations', function(e){
      if (e.keyCode != jQuery.ui.keyCode.DELETE){
        return;
      }

      if(!self.grid){
        return;
      }

      self.remove();
    });

    self.reload();
  },

  reload: function(){
    var self = this;
    jQuery('.daviz-annotations-box', self.context).remove();
    self.box = jQuery('<div>')
      .addClass('daviz-annotations-box')
      .appendTo(self.context)
      .dialog({
        bgiframe: true,
        title: 'Annotations for ' + self.target.label,
        modal: true,
        dialogClass: 'daviz-confirm-overlay',
        minHeight: 480,
        minWidth: 600,
        closeOnEscape: false,
        open: function(evt, ui){
          var buttons = jQuery(this).parent().find("button[title!='close']");
          buttons.attr('class', 'btn');
          jQuery(buttons[0]).addClass('btn-inverse');
          jQuery(buttons[1]).addClass('btn-success');
        },
        close: function(evt, ui){
          jQuery(document).unbind('.DavizAnnotations');
          if(self.grid){
            self.grid.destroy();
            self.box.remove();
          }
        },
        buttons: {
          Cancel: function(){
            jQuery(this).dialog('close');
          },
          Save: function(){
            self.save();
            jQuery(this).dialog('close');
          }
        }
      });

    self.template();
  },

  template: function(){
    var self = this;
    jQuery([
    '<div class="field">',
      '<label>',
        '<span class="formHelp">Define specific annotations for data values (e.g. :=not available, (p)=provisional, (b)=break in series, etc)</span>',
      '</label>',
      '<div class="daviz-slick-table daviz-annotations-table" style="width: 550px; height: 400px"></div>',
    '</div>'
    ].join('\n')).appendTo(self.box);
    self.body();
  },

  body: function(){
    var self = this;

    var columns = [
      {
        id: 'name',
        name: 'Id',
        field: 'name',
        toolTip: 'e.g. (p), n/a, :, (b)',
        sortable: false,
        selectable: true,
        resizable: true,
        focusable: true,
        editor: Slick.Editors.Text
      }, {
        id: 'title',
        name: 'Friendly Name',
        field: 'title',
        toolTip: 'e.g. Provisional, Not available',
        sortable: false,
        selectable: true,
        resizable: true,
        focusable: true,
        editor: Slick.Editors.Text
      }];

    var options = {
      enableColumnReorder: false,
      editable: true,
      enableAddRow: true,
      forceFitColumns: true,
      enableCellNavigation: true,
      autoEdit: true
    };

    self.grid = new Slick.Grid('.daviz-annotations-table', self.annotations.annotations, columns, options);
    self.grid.setSelectionModel(new Slick.CellSelectionModel());

    self.grid.onAddNewRow.subscribe(function (e, args) {
      var item = args.item;
      self.grid.invalidateRow(self.annotations.annotations.length);
      self.annotations.annotations.push(item);
      self.grid.updateRowCount();
      self.grid.render();
    });

    self.grid.onCellChange.subscribe(function(e, args){
      var item = args.item;
      var index = args.row;
      if( !(item.name || item.title) ){
        self.annotations.annotations.splice(index, 1);
        self.grid.invalidate();
      }
    });
  },

  remove: function(){
    var self = this;
    var rows = self.grid.getSelectedRows();
    if(!rows.length){
      return;
    }

    var index = rows[0];
    var length = rows.length;
    self.annotations.annotations.splice(index, length);
    self.grid.invalidate();
  },

  save: function(){
    var self = this;
    self.context.closest('.daviz-view-form').data('annotations', self.annotations.annotations);
    jQuery(document).trigger(DavizEdit.Events.table.changed, self.settings.table);
  }
};

DavizEdit.JsonGrid = function(context){
  this.initialize(context);
};

DavizEdit.JsonGrid.prototype = {
  initialize: function(context){
    var self = this;
    self.context = context;
    self.context.addClass('daviz-jsongrid');

    self.grid = null;

    self.textarea = jQuery('textarea', self.context)
      .css({width: '99%', margin: '0px'})
      .slideUp()
      .change(function(){
        self.reload();
      });

    self.table = JSON.parse(self.textarea.val());
    jQuery("label[for='daviz.properties.json']", self.context).hide();

    self.relatedItems = {};
    var action = self.context.parents('form').attr('action');
    var i = action.indexOf('@@');
    action = action.slice(0, i) + '@@daviz.json';
    DavizEdit.Status.start('Loading data table...');
    jQuery.getJSON(action, {}, function(data){
        self.relatedItems = data;
        self.reload();
        DavizEdit.Status.stop('Loading data table... Done');
      });

    // Events
    jQuery(document).unbind('.DavizJsonGrid');
    jQuery(document).bind(DavizEdit.Events.facet.changed + '.DavizJsonGrid', function(evt, data){
      self.save_header(data);
    });

    jQuery(document).bind(DavizEdit.Events.table.changed + '.DavizJsonGrid', function(evt, data){
      self.table = data;
      self.textarea.val(JSON.stringify(self.table, null, "  ")).change();
    });
  },

  reload: function(){
    var self = this;
    if(self.grid){
      self.grid.destroy();
      jQuery(".daviz-data-table", self.context).remove();
    }

    self.gridview = jQuery('<div>')
      .addClass('daviz-slick-table')
      .addClass('daviz-data-table')
      .width(self.context.parents('.daviz-settings').width() - 40)
      .height(300);

    self.textarea.after(self.gridview);

    self.table = JSON.parse(self.textarea.val());
    var colNames = Object.keys(self.table.properties || {});
    var cols = [];
    var i;
    for (i = 0; i < colNames.length; i++){
        var newCol = {
            name: colNames[i],
            order: self.table.properties[colNames[i]].order
        };
        cols.push(newCol);
    }
    cols = cols.sort(function(a,b){return a.order-b.order;});

    colNames = [];
    for (i = 0; i < cols.length; i++){
        colNames.push(cols[i].name);
    }

    var columns = [
      {
        id: "selector",
        name: "",
        field: "num",
        cssClass: "slickgrid-index-column",
        width: 30,
        resizable: false,
        header: {
          buttons: [
            {
              image: "++resource++slickgrid-images/pencil.png",
              command: "editJSON",
              tooltip: "Inspect and edit generate JSON"
            }
          ]
        }
      }
    ];

    jQuery.each(colNames, function(index, key){
      var colType = self.table.properties[key].columnType || self.table.properties[key].valueType;
      var label = self.table.properties[key].label || key;

      var column = {
        id: key,
        name: label,
        field: key,
        toolTip: colType,
        sortable: false,
        selectable: true,
        resizable: true,
        focusable: true,
        header: {
          menu: EEA.Daviz.ColumnMenu({
            columnType: colType,
            annotations: true
          })
        }
      };

      columns.push(column);
    });

    var options = {
      enableColumnReorder: false,
      enableCellNavigation: true,
      forceFitColumns: true,
      editable: false
    };

    var items = jQuery.map(self.relatedItems.items, function(item, index){
      item.num = index;
      return item;
    });

    self.grid = new Slick.Grid('.daviz-data-table', items, columns, options);

    // Plugins

    // Menu
    var headerMenuPlugin = new Slick.Plugins.HeaderMenu({
      buttonImage: "++resource++slickgrid-images/down.gif"
    });

    headerMenuPlugin.onCommand.subscribe(function(e, args) {
      self.handle_menu_action(args);
    });

    // Buttons
    var headerButtonsPlugin = new Slick.Plugins.HeaderButtons();
    headerButtonsPlugin.onCommand.subscribe(function(e, args) {
      self.edit_body(args);
    });

    self.grid.registerPlugin(headerMenuPlugin);
    self.grid.registerPlugin(headerButtonsPlugin);
    self.grid.setSelectionModel(new Slick.CellSelectionModel());

    // Header right-click
    self.grid.onHeaderContextMenu.subscribe(function(e, args){
      e.preventDefault();
      jQuery('.slick-header-menubutton', e.srcElement).click();
    });

    // Fixes
    self.gridview.height('auto');
    self.gridview.width(self.gridview.width() + 2);
  },

  handle_menu_action: function(args){
    var self = this;
    var command = args.command;
    if(command === "rename"){
      return self.edit_header(args.column);
    }

    if(command === 'annotations'){
      return self.edit_annotations(args.column);
    }

    if(command === 'delete'){
      return self.delete_column(args.column);
    }

    return self.convert_column(command, args.column);
  },

  delete_column: function(column){
    var self = this;
    delete self.table.properties[column.id];
    jQuery(document).trigger(DavizEdit.Events.table.changed, self.table);
  },

  convert_column: function(to, column){
    var self = this;
    self.table.properties[column.field].columnType = to;
    jQuery(document).trigger(DavizEdit.Events.table.changed, self.table);
  },

  edit_body: function(args){
    var self = this;
    if(self.textarea.is(':visible')){
      self.textarea.slideUp();
    }else{
      self.textarea.slideDown();
    }
  },

  edit_header: function(column){
    var self = this;
    var text = column.name;
    var popup = jQuery("<div title='Rename column: " + column.name + "' />")
      .append(
        jQuery("<div>")
            .addClass("warning portalMessage warningMessage")
            .html("<b>Warning: </b>Changing the name of the columns may break existing charts if unpivot was used.")
      )
      .append(
        jQuery('<input>').attr('type', 'text').val(text).width('80%')
      ).dialog({
        bgiframe: true,
        modal: true,
        dialogClass: 'daviz-confirm-overlay',
        width: 400,
        open: function(evt, ui){
          var buttons = jQuery(this).parent().find("button[title!='close']");
          buttons.attr('class', 'btn');
          jQuery(buttons[0]).addClass('btn-inverse');
          jQuery(buttons[1]).addClass('btn-success');
        },
        buttons: {
          Cancel: function(){
            jQuery(this).dialog('close');
          },
          Rename: function(){
            var value = jQuery('input', popup).val();
            self.table.properties[column.id].label = value;
            jQuery("[name='" + column.id + ".label']").val(value);
            self.grid.updateColumnHeader(column.id, value);
            jQuery(document).trigger(DavizEdit.Events.table.changed, self.table);
            jQuery(this).dialog('close');
          }
        }
    });
  },

  edit_annotations: function(column){
    var self = this;
    var settings = {
      table: jQuery.extend({}, self.table),
      column: column.id
    };
    var annotations = new DavizEdit.Annotations(self.context, settings);
    return annotations;
  },

  save_header: function(options){
    var self = this;
    var column = self.table.properties[options.key];
    if(!column){
      return;
    }
    column.label = options.value;
    self.textarea.val(JSON.stringify(self.table, null, "  "));
    self.grid.updateColumnHeader(options.key, options.value);
  }
};

DavizEdit.SourceTable = function(table){
  this.initialize(table);
};

DavizEdit.SourceTable.prototype = {
  initialize: function(table){
    var self = this;
    self.table = table;
    self.count = jQuery("input[name='daviz.properties.sources.count']", table.parent());

    self.button_add = jQuery("input[name='daviz.properties.sources.add']", table);
    self.button_add.click(function(){
      self.add(jQuery(this));
      return false;
    });

    self.button_remove = jQuery("input[name='daviz.properties.sources.remove']", table);
    if (!self.button_remove.length){
      self.button_remove = jQuery('<input>').attr('type', 'submit')
        .attr('name', 'daviz.properties.sources.remove')
        .val("Remove selected items");
      self.button_add.parent('td').prepend(self.button_remove);
    }

    self.button_remove.click(function(){
      self.remove(jQuery(this));
      return false;
    });

  },

  add: function(button){
    var self = this;
    button.removeClass('submitting');
    var count = parseInt(self.count.val(), 10);

    var check = jQuery('<input />').attr('type', 'checkbox')
      .addClass('editcheck')
      .attr('name', 'daviz.properties.sources.remove_' + count);
    var text = jQuery('<input />').attr('type', 'text').attr("value", "")
      .addClass('textType')
      .attr('name', 'daviz.properties.sources.' + count + '.');

    var td = jQuery('<td>').append(check).append(text);
    var row = jQuery('<tr>').append(td);

    self.table.prepend(row);

    count += 1;
    self.count.val(count);
  },

  remove: function(button){
    var self = this;
    button.removeClass('submitting');

    var checked = jQuery("input[type='checkbox']:checked", self.table);
    checked.each(function(){
      jQuery(this).parent().parent('tr').remove();
    });

    var count = parseInt(self.count.val(), 10);
    count -= checked.length;
    self.count.val(count);
  }
};


jQuery(document).ready(function(){
  DavizEdit.Status.initialize();
  DavizEdit.Confirm.initialize();
  DavizEdit.Facets.initialize();
  DavizEdit.Views.initialize();
});

