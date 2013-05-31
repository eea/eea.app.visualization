""" Edit Form for Facetds
"""
from zope.component import queryAdapter
from zope.formlib.form import SubPageForm
from zope.formlib.form import action as formAction
from zope.formlib.form import setUpWidgets, haveInputWidgets
from zope.formlib.form import Fields
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.zopera import IStatusMessage
from eea.app.visualization.facets.interfaces import IVisualizationEditFacet
from eea.app.visualization.config import EEAMessageFactory as _

class EditForm(SubPageForm):
    """
    Basic layer to edit daviz facets. For more details on how to use this,
    see implementation in eea.app.visualization.facets.list.edit.Edit.

    Assign these attributes in your subclass:
      - form_fields: Fields(Interface)

    """
    form_fields = None
    _prefix = ''

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        for key in self.request.form:
            if key.endswith('.label'):
                self._prefix = key.split('.')[0]
                break

    def getPrefix(self):
        """ Form prefix getter
        """
        return self._prefix

    def setPrefix(self, value):
        """ Form prefix setter
        """
        self._prefix = value

    prefix = property(getPrefix, setPrefix)

    @property
    def label(self):
        """ Label
        """
        return self.prefix

    @property
    def _data(self):
        """ Form data
        """
        accessor = queryAdapter(self.context, IVisualizationConfig)
        return accessor.facet(self.prefix, {})

    def setUpWidgets(self, ignore_request=False):
        """ Setup form widgets
        """
        self.adapters = {}
        for key, value in self.request.form.items():
            if isinstance(value, str):
                value = value.decode('utf-8')
                self.request.form[key] = value

        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    @formAction(_('Save'), condition=haveInputWidgets)
    def save(self, action, data):
        """ Handle save action
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        mutator.edit_facet(self.prefix, **data)

        name = action.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return _('Changes saved')
        return self.nextUrl

    @property
    def nextUrl(self):
        """ Next URL
        """
        status = queryAdapter(self.request, IStatusMessage)
        if status:
            status.addStatusMessage(_('Changes saved'), type='info')
        to = self.context.absolute_url() + '/daviz-edit.html'
        self.request.response.redirect(to)

class Edit(EditForm):
    """ Edit list facet
    """
    form_fields = Fields(IVisualizationEditFacet)
