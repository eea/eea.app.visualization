""" Data utilities
"""
import logging
import operator
import json as simplejson
from zope.interface import implements
from eea.app.visualization.interfaces import IVisualizationJsonUtils
logger = logging.getLogger("eea.app.visualization.utils")

class VisualizationJsonUtils(object):
    """ Utility for Visualization JSON operations
    """
    implements(IVisualizationJsonUtils)

    def merge(self, old, new):
        """ Merge new dictionary to old one.

        old and new dictionaries should have the following structure::

            {
              'key-1': {
                'prop-1': 'value',
                'prop-2': 'value',
                ...
              },
              key-2 : {
              ...
              }
            }

        """
        for key in new:
            if key not in old:
                old[key] = new[key]
                continue

            old[key].update(new[key])
        return old

    def sortProperties(self, strJson, indent=1):
        """
        In the json string set the correct order of the columns
        """
        def compare(a, b):
            """ Custom cmp
            """
            return cmp(a.get('order', 0), b.get('order', 0))

        try:
            indent1 = u' ' * indent
            indent2 = u' ' * (indent + indent)

            json = simplejson.loads(strJson)
            properties = json.get('properties', {})
            newProperties = sorted(
                properties.items(), key=operator.itemgetter(1), cmp=compare)
            json['properties'] = ''
            json = simplejson.dumps(json, indent=indent)

            newPropStr = [
                u'"properties"', u':', u'{'
            ]

            for key, value in newProperties:
                newPropStr.extend([
                    u'\n', indent2, u'"%s"' % key, u': ',
                    simplejson.dumps(value), u","
                ])

            if newPropStr[-1] == u',':
                newPropStr.pop()

            newPropStr.extend([
                u'\n', indent1, u'}'
            ])

            newPropStr = u''.join(newPropStr)

            json = json.replace('"properties": ""', newPropStr)
            return json
        except Exception, err:
            logger.exception(err)
            return strJson
