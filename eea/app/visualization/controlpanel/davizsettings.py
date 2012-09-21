""" Daviz Settings ZMI and Plone Control Panel Views
"""
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib.form import EditForm, FormFields, setUpWidgets, action
from zope.component import getUtilitiesFor
from zope.component import queryUtility
from eea.app.visualization.controlpanel.interfaces import IDavizSection
from eea.app.visualization.controlpanel.interfaces import IDavizSettings
from persistent.dict import PersistentDict
from Products.statusmessages.interfaces import IStatusMessage
from datetime import datetime
from zope.interface import implements
from zope.component.hooks import getSite

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


    def mergedFields(self):
        """ merge all fields from registered extensions
        """
        form_fields = FormFields()
        sections = []
        extensions = [x for x in getUtilitiesFor(IDavizSection)]
        pos = 0
        for extension in extensions:
            if hasattr(extension[1], "form_fields"):
                form_fields = \
                    form_fields.__add__(extension[1].form_fields)
                sections.append(
                    (extension[1].prefix, extension[1].title, pos))
                pos += len(extension[1].form_fields)
        return {'form_fields':form_fields, 'sections': sections}

class DavizSettingsZMIEditForm(EditForm):
    """ ZMI Edit Form
    """
    prefix = ""
    label = "Daviz settings"
    template = ViewPageTemplateFile("zmi_davizsettings_edit.pt")

    def __init__(self, context, request):
        self.context = context
        mergedFields = context.mergedFields()
        self.form_fields = mergedFields['form_fields']
        self.sections = mergedFields['sections']
        super(DavizSettingsZMIEditForm, self).__init__(context, request)

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

    @action(u"Save Changes", name=u'save')
    def handle_save_action_daviz(self, saction, data):
        """ Save action"""
        for field in self.form_fields.__FormFields_byname__.keys():
            value = self.request.get(field, None)
            self.context.settings[field] = value

        self.request.SESSION['messages'] = ["Saved changes. (%s)" 
            % (datetime.now())]
        self.request.RESPONSE.redirect(self.context.absolute_url() + 
            '/manage_workspace')


zmi_addDavizSettings_html = PageTemplateFile('zmi_davizsettings_add.pt',
                                            globals())

def zmi_addDavizSettings(parent, id, title, REQUEST=None):
    """ Create a new DavizSettings """

    ob = DavizSettings(id, title)
    parent._setObject(id, ob)
    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(parent.absolute_url() +
                                    '/manage_workspace')

class DavizSettingsControlPanelEditForm(DavizSettingsZMIEditForm):
    """ Plone Control Panel Edit Form
    """
    template = ViewPageTemplateFile("controlpanel_davizsettings_edit.pt")

    def __init__(self, context, request):
        daviz_settings = queryUtility(IDavizSettings)
        daviz_settings = context.__of__(daviz_settings)
        super(DavizSettingsControlPanelEditForm, self).__init__(daviz_settings,
                                                                 request)

    @action(u"Save", name=u'save')
    def handle_save_action_daviz(self, saction, data):
        """ Save action """
        for field in self.form_fields.__FormFields_byname__.keys():
            value = self.request.get(field, None)
            self.context.settings[field] = value
        IStatusMessage(self.request).addStatusMessage(u"Settings saved")
        self.request.response.redirect("@@daviz-settings")

    @action(u"Cancel", name=u'cancel')
    def handle_cancel_action_daviz(self, saction, data):
        """ Cancel action """
        IStatusMessage(self.request).addStatusMessage(u"Edit cancelled")
        self.request.response.redirect("@@overview-controlpanel")

