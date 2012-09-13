""" Visualization properties
"""
import logging
import json as simplejson
from zope import schema
from zope.event import notify
from zope.interface import Interface
from zope.formlib.form import Fields
from zope.component import queryAdapter, queryUtility
from zope.formlib.form import SubPageForm
from zope.lifecycleevent import ObjectModifiedEvent
from zope.formlib.form import action as formaction
from zope.formlib.form import setUpWidgets, haveInputWidgets
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationJsonUtils
from eea.app.visualization.interfaces import IGuessType
from eea.app.visualization.zopera import IStatusMessage

from eea.app.visualization.config import EEAMessageFactory as _
logger = logging.getLogger('eea.app.visualization')

class IVisualizationPropertiesEdit(Interface):
    """ Edit visualization global properties
    """
    json = schema.Text(
        title=u"Data table (preview)",
        description=(u"<ul>"
                       "<li>Click on the bottom-left pencil to "
                           "inspect and edit generate JSON.</li>"
                       "<li>Click on the table's columns headers to adjust "
                       "their labels (user friendly-names)</li>"
                     "</ul>"),
        required=False
    )
    json.order = 20

    sources = schema.List(
        title=u'Additional sources',
        required=False,
        description=(
            u"Add additional external exhibit sources to be merged. "
            "Supported formats: "
            "'Exhibit JSON', 'Google Spreadsheet' and 'RDF/XML'. "
            "See more details "
            "http://www.simile-widgets.org/wiki/Exhibit/Creating"
            "%2C_Importing%2C_and_Managing_Data#Conversion_at_Load_Time"),
        value_type=schema.TextLine(title=u'URL')
    )
    sources.order = 30

class EditForm(SubPageForm):
    """ Layer to edit daviz properties.
    """
    label = u"Data settings"
    form_fields = Fields(IVisualizationPropertiesEdit)

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        name = self.__name__
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        self.prefix = name.replace('.edit', '', 1)
        self.message = 'Changes saved'

    @property
    def _data(self):
        """ Form data
        """
        accessor = queryAdapter(self.context, IVisualizationConfig)
        json = simplejson.dumps(dict(accessor.json), indent=2)
        utils = queryUtility(IVisualizationJsonUtils)
        return {
            'name': self.prefix,
            'json': utils.sortProperties(json, indent=2),
            'views': [view.get('name') for view in accessor.views],
            'sources':
                [source.get('name') for source in accessor.sources],
        }

    def setUpWidgets(self, ignore_request=False):
        """ Setup widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    def handle_json(self, data):
        """ Handle json property
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        json = data.get('json', None)
        if json is None:
            return

        try:
            json = dict(simplejson.loads(json))
        except Exception, err:
            logger.exception(err)
            self.message = "ERROR: %s" % err
            return

        for _name, props in json.get('properties', {}).items():
            columnType = props.get('columnType', props.get('valueType', 'text'))
            util = queryUtility(IGuessType, columnType)
            if not util:
                continue
            props['columnType'] = columnType
            props['valueType'] = util.valueType
        mutator.json = json
        notify(ObjectModifiedEvent(self.context))

    def handle_sources(self, data):
        """ Handle sources property
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        sources = data.get('sources', None)
        if sources is None:
            return

        sources = set(sources)
        mutator.delete_sources()
        for source in sources:
            source = source.strip()
            if not source:
                continue

            properties = {
                "name": source,
                "converter": "",
                "type": "json"
            }

            if 'google' in source.lower():
                properties['type'] = 'jsonp'
                properties['converter'] = 'googleSpreadsheets'
            elif 'rdfa' in source.lower():
                properties['type'] = 'RDFa'
            elif ('rdf' in source.lower()) or ('xml' in source.lower()):
                properties['type'] = 'rdf+xml'

            mutator.add_source(**properties)

    @formaction(_('Save'), condition=haveInputWidgets)
    def save(self, action, data):
        """ Handle save action
        """
        self.handle_json(data)
        self.handle_sources(data)

        # Return
        name = action.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return self.message
        return self.nextUrl

    @property
    def nextUrl(self):
        """ Next
        """
        status = queryAdapter(self.request, IStatusMessage)
        if status:
            status.addStatusMessage(self.message, type='info')
        next_url = self.context.absolute_url() + '/daviz-edit.html'
        self.request.response.redirect(next_url)
