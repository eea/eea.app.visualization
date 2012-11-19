""" Browser views converter utilities
"""
import json
from zope.component import queryUtility, queryMultiAdapter
from eea.app.visualization.interfaces import ITable2JsonConverter
from eea.app.visualization.interfaces import IVisualizationJsonUtils
from Products.Five.browser import BrowserView

class Table2Json(BrowserView):
    """ Convert CSV table to JSON
    """
    def __call__(self, **kwargs):
        form = getattr(self.request, 'form', {})
        form.update(kwargs)
        table = form.get('table', '')
        convert = queryUtility(ITable2JsonConverter)
        _columns, data = convert(table)
        self.request.response.setHeader(
            'Content-Type', 'application/json')

        utils = queryUtility(IVisualizationJsonUtils)
        return utils.sortProperties(json.dumps(data))

class Json2Table(BrowserView):
    """ Convert JSOn to CSV
    """
    def __call__(self, **kwargs):
        form = getattr(self.request, 'form', {})
        form.update(kwargs)
        data = form.get('json', '{}')
        data = json.loads(data)
        download = queryMultiAdapter((self.context, self.request),
                                     name=u'download.table')
        download._data = data
        return download.tsv(attachment=False)
