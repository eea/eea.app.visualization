""" Daviz Visualization Control Panel
"""
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from zope import schema
from persistent.dict import PersistentDict

from eea.app.visualization.controlpanel.interfaces import IDavizSettings

from zope.formlib.form import EditForm, setUpWidgets, action, FormFields

from zope.component import getUtilitiesFor

class DavizSettingsEditForm(EditForm):
    """
    DavizSettings Control Panel
    """
    label = "Daviz settings"
    prefix = ""
    template = ViewPageTemplateFile("controlpanel.pt")

    @property
    def _data(self):
        """ Data for edit form
        """
        settingsdict = {}
        for x in getUtilitiesFor(IDavizSettings):
            settingsdict.update(x[1].settings)
        return settingsdict

    def setUpWidgets(self, ignore_request=False):
        """ Sets up widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    def __init__(self, context, request):
        self.form_fields = FormFields()
        self.sections = []
        extensions = [x for x in getUtilitiesFor(IDavizSettings)]
        pos = 0
        for extension in extensions:
            if hasattr(extension[1], "form_fields"):
                self.form_fields = \
                    self.form_fields.__add__(extension[1].form_fields)
                self.sections.append(
                    (extension[1].prefix, extension[1].title, pos))
                pos += len(extension[1].form_fields)
        super(DavizSettingsEditForm, self).__init__(context, request)

    @action(u"Save", name=u'save')
    def handle_save_action_daviz(self, saction, data):
        """ Save action """
        extensions = [x[1] for x in getUtilitiesFor(IDavizSettings)]
        for extension in extensions:
            extension.settings = PersistentDict()
            fields = extension.form_fields.__FormFields_byname__.keys()
            for field in fields:
                value = self.request.get(field, None)
                extension.settings[field] = value
        IStatusMessage(self.request).addStatusMessage(u"Settings saved")
        self.request.response.redirect("@@daviz-settings")

    @action(u"Cancel", name=u'cancel')
    def handle_cancel_action_daviz(self, saction, data):
        """ Cancel action """
        IStatusMessage(self.request).addStatusMessage(u"Edit cancelled")
        self.request.response.redirect("@@overview-controlpanel")


class DavizSettings(object):
    """ Daviz Settings
    """
    implements(IDavizSettings)
    prefix = 'daviz'
    title = 'Daviz General Settings'
    settings = PersistentDict()

    form_fields = FormFields(
        schema.TextLine(
            __name__='daviz.defaultfolder',
            title=u'Default Folder for Visualizations',
            required=False),
    )
