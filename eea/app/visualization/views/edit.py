""" Basic layer for daviz edit views
"""
from zope.component import queryAdapter
from zope.formlib.form import SubPageForm
from zope.formlib.form import action, setUpWidgets
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.zopera import IStatusMessage
from eea.app.visualization.config import EEAMessageFactory as _

class EditForm(SubPageForm):
    """
    Basic layer to edit daviz views. For more details on how to use this,
    see implementation in eea.exhibit.views.map.edit.Edit.

    Assign these attributes in your subclass:
      - form_fields: Fields(Interface)

    """
    form_fields = None
    previewname = None

    def __init__(self, context, request):
        """ EditForm init
        """
        super(EditForm, self).__init__(context, request)
        name = self.__name__
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        self.prefix = name.replace('.edit', '', 1)

    @property
    def _data(self):
        """ Return view
        """
        accessor = queryAdapter(self.context, IVisualizationConfig)
        return accessor.view(self.prefix, {})

    def setUpWidgets(self, ignore_request=False):
        """ Sets up widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    @action(_('Save'))
    def save(self, saction, data):
        """ Handle save action
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        mutator.edit_view(self.prefix, **data)

        name = saction.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return _('Changes saved')
        return self.nextUrl

    @action(_('Disable'))
    def disable(self, saction, data):
        """ Handle disable action
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        mutator.delete_view(self.prefix)

        name = saction.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return _('View disabled')
        return self.nextUrl

    @property
    def nextUrl(self):
        """ Redirect to daviz-edit.html as next_url
        """
        status = queryAdapter(self.request, IStatusMessage)
        if status:
            status.addStatusMessage(_('Changes saved'), type='info')
        next_url = self.context.absolute_url() + '/daviz-edit.html'
        self.request.response.redirect(next_url)
