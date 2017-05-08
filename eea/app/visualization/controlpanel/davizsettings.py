""" Daviz Settings ZMI and Plone Control Panel Views
"""
# pylint: disable = W0622
from datetime import datetime
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from eea.app.visualization.controlpanel.interfaces import IDavizSection
from eea.app.visualization.controlpanel.interfaces import IDavizSettings
from zope.formlib.form import EditForm, FormFields, setUpWidgets, action
from zope.component import getUtilitiesFor
from zope.component import queryUtility
from zope.interface import implements
from zope.component.hooks import getSite
from persistent.dict import PersistentDict

class DavizSettings(SimpleItem):
    """ Daviz Settings
    """
    meta_type = "EEA Daviz Settings"
    security = ClassSecurityInfo()
    implements(IDavizSettings)
    id = 'portal_daviz'

    manage_options = (
        {'label': 'Edit', 'action': 'zmi_edit_html'},
    ) + SimpleItem.manage_options

    def __init__(self, p_id, title="all daviz settings"):
        super(DavizSettings, self).__init__()
        self._setId(p_id)
        self.title = title
        self.settings = PersistentDict()

        site = getSite()
        sm = site.getSiteManager()
        ds = sm.queryUtility(IDavizSettings)
        if ds:
            sm.unregisterUtility(ds, IDavizSettings)
        sm.registerUtility(self, IDavizSettings)

    def disabled(self, view, content_type):
        """ Is view disabled for given content_type
        """
        if not isinstance(view, (str, unicode)):
            view = getattr(view, '__name__', '')
        if not isinstance(content_type, (str, unicode)):
            content_type = getattr(content_type, 'portal_type',
                           getattr(content_type, 'meta_type', None))
        portal_types = self.settings.get(u'forbidden.%s' % view, None) or []
        return content_type in portal_types

class DavizSettingsZMIEditForm(EditForm):
    """ ZMI Edit Form
    """
    prefix = "davizsettings"
    label = "Daviz Visualization Settings"
    template = ViewPageTemplateFile("zmi_davizsettings_edit.pt")

    def __init__(self, context, request):
        super(DavizSettingsZMIEditForm, self).__init__(context, request)
        self._sections = None
        self._form_fields = None

    @property
    def sections(self):
        """ Sections
        """
        if self._sections is not None:
            return self._sections

        self._sections = []
        extensions = [ex for _name, ex in getUtilitiesFor(IDavizSection)]
        for extension in extensions:
            if not hasattr(extension, "form_fields"):
                continue

            self._sections.append({
                'name': extension.prefix,
                'title': extension.title,
                'widgets': [(self.prefix + '.' + field.__name__)
                            for field in extension.form_fields]
            })
        return self._sections

    @property
    def form_fields(self):
        """ Form fields
        """
        if self._form_fields is not None:
            return self._form_fields

        self._form_fields = FormFields()
        extensions = [ex for _name, ex in getUtilitiesFor(IDavizSection)]
        for extension in extensions:
            if not hasattr(extension, "form_fields"):
                continue
            self._form_fields += extension.form_fields
        return self._form_fields

    @property
    def _data(self):
        """ daviz saved settings
        """
        return self.context.settings

    def setUpWidgets(self, ignore_request=False):
        """ Sets up widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    def handle_save_action(self, saction, data):
        """ Handle save
        """
        for field in self.form_fields.__FormFields_byname__.keys():
            self.context.settings[field] = data.get(field, None)

    @action(u"Save Changes", name=u'save')
    def handle_save_action_daviz(self, saction, data):
        """ Save action"""
        self.handle_save_action(saction, data)
        self.request.SESSION['messages'] = [
            "Saved changes. (%s)" % (datetime.now())]
        self.request.RESPONSE.redirect(
            self.context.absolute_url() + '/manage_workspace')


zmi_addDavizSettings_html = PageTemplateFile(
    'zmi_davizsettings_add.pt', globals())

def zmi_addDavizSettings(parent, id, title, REQUEST=None):
    """ Create a new DavizSettings """

    ob = DavizSettings(id, title)
    parent._setObject(id, ob)
    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(
            parent.absolute_url() + '/manage_workspace')

class DavizSettingsControlPanelEditForm(DavizSettingsZMIEditForm):
    """ Plone Control Panel Edit Form
    """
    template = ViewPageTemplateFile("controlpanel_davizsettings_edit.pt")

    def __init__(self, context, request):
        daviz_settings = queryUtility(IDavizSettings)
        daviz_settings = context.__of__(daviz_settings)
        super(DavizSettingsControlPanelEditForm, self).__init__(
            daviz_settings, request)

    @action(u"Save", name=u'save')
    def handle_save_action_daviz(self, saction, data):
        """ Save action """
        self.handle_save_action(saction, data)
        IStatusMessage(self.request).addStatusMessage(u"Settings saved")
        self.request.response.redirect("@@daviz-settings")

    @action(u"Cancel", name=u'cancel')
    def handle_cancel_action_daviz(self, saction, data):
        """ Cancel action """
        IStatusMessage(self.request).addStatusMessage(u"Edit cancelled")
        self.request.response.redirect("@@overview-controlpanel")
