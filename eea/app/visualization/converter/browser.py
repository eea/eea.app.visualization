""" Custom converters to JSON
"""
import logging
import json as simplejson
from StringIO import StringIO
from zope.component import queryUtility
from eea.app.visualization.converter.interfaces import IExhibitJsonConverter
from eea.app.visualization.cache import ramcache, cacheJsonKey
from eea.app.visualization.browser.app.view import JSONView
logger = logging.getLogger('eea.app.visualization')

class TSVFileJSONView(JSONView):
    """ daviz-view.json for Tab separated files which is not daviz enabled
    """
    @ramcache(cacheJsonKey, dependencies=['eea.daviz'])
    def json(self):
        """ Convert file to JSON
        """
        datafile = StringIO(self.context.getFile().data)
        converter = queryUtility(IExhibitJsonConverter)
        try:
            _cols, json = converter(datafile)
        except Exception, err:
            logger.debug(err)
            return super(TSVFileJSONView, self).json()
        return simplejson.dumps(json)
