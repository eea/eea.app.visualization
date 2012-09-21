""" Custom converters to JSON
"""
import logging
import json as simplejson
from StringIO import StringIO
from zope.interface import implements
from zope.component import queryUtility, queryAdapter
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IVisualizationData
from eea.app.visualization.interfaces import IVisualizationJson
from eea.app.visualization.interfaces import IVisualizationJsonUtils
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.converter.interfaces import ITable2JsonConverter
from eea.app.visualization.cache import ramcache, cacheJsonKey

logger = logging.getLogger('eea.app.visualization')

class JSON(BrowserView):
    """ Abstract view to provide "daviz.json" multiadapter
    """
    implements(IVisualizationJson)

    def merge(self, old, new):
        """ Merge new dictionary to old one.
        """
        utils = queryUtility(IVisualizationJsonUtils)
        return utils.merge(old, new)

    def sortProperties(self, strJson, indent=1):
        """ Sort JSON properties
        """
        utils = queryUtility(IVisualizationJsonUtils)
        return utils.sortProperties(strJson, indent)

    @ramcache(cacheJsonKey, dependencies=['eea.daviz'])
    def json(self, column_types=None):
        """ Implement this method in order to provide a valid exhibit JSON
        """
        res = {'items': [], 'properties': {}}

        # Get data
        adapter = queryAdapter(self.context, IVisualizationData)
        if not (adapter or adapter.data):
            return simplejson.dumps(res)

        # Update JSON with existing annotations properties
        accessor = queryAdapter(self.context, IVisualizationConfig)
        my_json = {'items': [], 'properties': {}}
        if accessor:
            my_json = accessor.json
            if not column_types:
                column_types = dict(
                    (key, value.get('columnType',
                                    value.get('valueType', 'text'))
                     if isinstance(value, dict) else value)
                    for key, value in my_json.get('properties', {}).items()
                )

        # Convert to JSON
        datafile = StringIO(adapter.data)
        converter = queryUtility(ITable2JsonConverter)
        try:
            _cols, res = converter(datafile, column_types)
        except Exception, err:
            logger.debug(err)
            return simplejson.dumps(res)

        res.setdefault('properties', {})
        self.merge(
            res['properties'],
            my_json.get('properties', {})
        )
        return self.sortProperties(simplejson.dumps(res))
