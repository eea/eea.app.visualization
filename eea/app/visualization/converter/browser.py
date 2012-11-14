""" Browser views converter utilities
"""
import json
from zope.component import queryUtility
from eea.app.visualization.interfaces import ITable2JsonConverter
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
        return json.dumps(data)
