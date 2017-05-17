""" Edit
"""
import logging
import json as simplejson
from zope.event import notify
from zope.formlib.form import Fields
from zope.component import queryAdapter, queryUtility
from zope.lifecycleevent import ObjectModifiedEvent
from zope.formlib.form import action as formaction
from zope.formlib.form import setUpWidgets, haveInputWidgets
from eea.app.visualization.events import VisualizationFacetDeletedEvent
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationJsonUtils
from eea.app.visualization.interfaces import IGuessType
from eea.app.visualization.interfaces import IDavizSettings
from eea.app.visualization.views.data.interfaces import IDataEdit
from eea.app.visualization.views.edit import EditForm
from eea.app.visualization.config import EEAMessageFactory as _

logger = logging.getLogger('eea.app.visualization')


class Edit(EditForm):
    """ Edit view
    """
    label = _(u"Data settings")
    form_fields = Fields(IDataEdit)
    previewname = "daviz.properties.preview.png"
    message = _('Changes saved')

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
        for key, value in self.request.form.items():
            if isinstance(value, str):
                value = value.decode('utf-8')
                self.request.form[key] = value

        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    def handle_json(self, data):
        """ Handle json property
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        old_columns = set(mutator.json.get('properties', {}).keys())

        json = data.get('json', None)
        if json is None:
            return

        try:
            json = dict(simplejson.loads(json))
        except Exception, err:
            logger.exception(err)
            self.message = "ERROR: %s" % err
            return

        properties = json.get('properties', {})
        new_columns = set(properties.keys())

        for _name, props in properties.items():
            columnType = props.get('columnType',
                                   props.get('valueType', 'text'))
            util = queryUtility(IGuessType, columnType)
            if not util:
                continue
            props['columnType'] = columnType
            props['valueType'] = util.valueType

        # Columns deleted
        for column in old_columns.difference(new_columns):
            notify(VisualizationFacetDeletedEvent(self.context, facet=column))

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

    @property
    def annotations(self):
        """ Global annotations from portal_daviz
        """
        tool = queryUtility(IDavizSettings)
        annotations = tool.settings.get('data.annotations', '')

        annotations = [{'name': key, 'title': key}
                       for key in annotations.splitlines()]
        return simplejson.dumps(annotations)

    @formaction(_('Save'), condition=haveInputWidgets)
    def save(self, saction, data):
        """ Handle save action
        """
        self.handle_json(data)
        self.handle_sources(data)

        # Return
        name = saction.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return self.message
        return self.nextUrl

    @formaction(_('Disable'))
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
