""" Downloads controllers
"""
import json
import csv
import logging
from zope.component import queryMultiAdapter, queryUtility
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IVisualizationJsonUtils

logger = logging.getLogger('eea.app.visualization')

class ExcelTSV(csv.excel):
    """ CSV Tab Separated Dialect
    """
    delimiter = '\t'
csv.register_dialect("eea.app.visualization.tsv", ExcelTSV)

class Download(BrowserView):
    """ Download Visualization data in various formats
    """
    def __init__(self, context, request):
        super(Download, self).__init__(context, request)
        self._data = {}

    def sortProperties(self, strJson, indent=1):
        """ Sort JSON properties
        """
        utils = queryUtility(IVisualizationJsonUtils)
        return utils.sortProperties(strJson, indent)

    @property
    def data(self):
        """ JSON data
        """
        if not self._data:
            data = queryMultiAdapter((self.context, self.request),
                                     name=u'daviz.json')
            try:
                self._data = json.loads(data())
            except Exception, err:
                logger.debug(err)
                self._data = {'properties':{}, 'items': []}
        return self._data

    @property
    def headers(self):
        """ JSON headers
        """
        props = self.data.get('properties', {})
        propsList = []
        def_order = 0
        for key, item in props.items():
            prop = []
            prop.append(item.get('order', def_order))
            prop.append(key)
            prop.append(item.get('columnType', item.get('valueType', 'text')))
            propsList.append(prop)
            def_order += 1
        propsList.sort()
        finalProps = []
        for prop in propsList:
            finalProp = []
            finalProp.append(prop[1])
            finalProp.append(prop[2])
            finalProps.append(finalProp)
        return finalProps
#        return self.data.get('properties', {})

    def table(self):
        """ Download as HTML table
        """
        for item in self.data.get('items', []):
            yield item

    def csv(self, dialect='excel'):
        """ Download as Comma Separated File
        """
        if dialect == 'excel':
            self.request.response.setHeader(
                'Content-Type', 'application/csv')
            self.request.response.setHeader(
                'Content-Disposition',
                'attachment; filename="%s.csv"' % self.context.getId())
        else:
            self.request.response.setHeader(
                'Content-Type', 'application/tsv')
            self.request.response.setHeader(
                'Content-Disposition',
                'attachment; filename="%s.tsv"' % self.context.getId())

        writter = csv.writer(self.request.response, dialect=dialect)
        row = []
        headers = self.headers
#        headers = self.data.get('properties', {}).keys()
        for col in headers:
            hprops = self.data.get('properties', {}).get(col[0], {})
            header = u'%s:%s' % (col[0], hprops.get('columnType',
                                hprops.get('valueType', 'text'))
                                 if isinstance(hprops, dict) else hprops)
            row.append(header)
        writter.writerow(row)

        for item in self.data['items']:
            row = []
            for col in headers:
                row.append(unicode(item.get(col[0], '')))
            writter.writerow(row)
        return ''

    def tsv(self, dialect='eea.app.visualization.tsv'):
        """ Download as Tab Separated File
        """
        return self.csv(dialect=dialect)

    def json(self):
        """ Downlaod as JSON
        """
        headers = {'Accept' : 'application/sparql-results+json'}
        self.request.response.setHeader(
            'Content-Type', 'application/json')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s.json"' % self.context.getId())

        headers = self.headers
        header_vars = []
        for header in headers:
            header_vars.append(header[0])

        data = {
            'head': {
                'vars': header_vars,
            },
            'results': {
                'bindings': [
                    # Items here
                ]
            }
        }

        for item in self.data.get('items', []):
            convertedItem = {}
            for header in headers:
                hprops = self.data.get('properties', {}).get(header[0], {})

#                hprops = headers.get(header, {})
                valueType = (hprops.get('valueType', 'text')
                             if isinstance(hprops, dict) else hprops)
                convertedItem[header[0]] = {
                    "type": "typed-literal",
                    "datatype": self.xmlType(valueType),
                    "value": item.get(header[0], "")
                }
            data['results']['bindings'].append(convertedItem)

        return self.sortProperties(json.dumps(data, indent=2), indent=2)

    def exhibit(self):
        """ Download as Exhibit JSON
        """
        self.request.response.setHeader(
            'Content-Type', 'application/json')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s.exhibit.json"' % self.context.getId())
        return self.sortProperties(json.dumps(self.data, indent=2), indent=2)

    def xml(self):
        """ Download as XML
        """
        self.request.response.setHeader(
            'Content-Type', 'application/xml')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s.xml"' % self.context.getId())

    def xmlType(self, value):
        """ Convert JSON valueType to xmlType
        """
        if not value:
            return None
        if value in ('text', 'url',):
            value = 'string'
        elif value in ('number',):
            value = 'double'
        return 'http://www.w3.org/2001/XMLSchema#%s' % value

    def schema(self):
        """ Download as XML with schema
        """
        self.request.response.setHeader(
            'Content-Type', 'application/xml')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s.schema.xml"' % self.context.getId())

    def schemaType(self, value):
        """ Convert JSON valueType to schemaType
        """
        if not value:
            return None
        if value in ('text', 'url',):
            value = 'string'
        elif value in ('number',):
            value = 'double'
        return 'xsd:%s' % value
