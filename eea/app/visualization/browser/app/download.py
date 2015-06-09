""" Downloads controllers

    >>> portal = layer['portal']
    >>> from eea.app.visualization.tests.utils import loadblobfile
    >>> sid = portal.invokeFactory('File', 'sandbox')
    >>> sandbox = portal._getOb(sid)
    >>> _ = loadblobfile(sandbox, 'data/data-sample-v4.tsv', 'text/tsv')
    >>> support = sandbox.restrictedTraverse('@@daviz_support')
    >>> _ = support.enable()

    >>> from eea.app.visualization.interfaces import IVisualizationEnabled
    >>> IVisualizationEnabled.providedBy(sandbox)
    True

"""
import json
import csv
import logging
from StringIO import StringIO
from zope.component import queryMultiAdapter, queryUtility
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IVisualizationJsonUtils

logger = logging.getLogger('eea.app.visualization')

class ExcelTSV(csv.excel):
    """ CSV Tab Separated Dialect
    """
    delimiter = '\t'
    quoting = csv.QUOTE_MINIMAL
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
            prop.append(item.get('label', key))
            propsList.append(prop)
            def_order += 1
        propsList.sort()

        return [p[1:4] for p in propsList]

    def table(self):
        """ Download as HTML table

            >>> output = sandbox.restrictedTraverse('@@download.table')
            >>> print output()
            <html lang="en-US"...
            ...
            <th>
              FacilityID
            </th>
            ...
            <td>
              Energy - Mineral oil and gas refineries
            </td>
            ...

        """
        for item in self.data.get('items', []):
            yield item

    def csv(self, dialect='excel', attachment=True):
        """ Download as Comma Separated File

            >>> output = sandbox.restrictedTraverse('@@download.csv')
            >>> print output(attachment=False)
            FacilityID:number,FacilityName:text...
            ...
            118563,ENI SpA Divisione Refining & Marketing...

        """
        if dialect == 'excel':
            self.request.response.setHeader(
                'Content-Type', 'application/csv')
            if attachment:
                self.request.response.setHeader(
                    'Content-Disposition',
                    'attachment; filename="%s.csv"' % self.context.getId())
        else:
            self.request.response.setHeader(
                'Content-Type', 'application/tsv')
            if attachment:
                self.request.response.setHeader(
                    'Content-Disposition',
                    'attachment; filename="%s.tsv"' % self.context.getId())

        if attachment:
            output = self.request.response
        else:
            output = StringIO()

        writter = csv.writer(output, dialect=dialect)

        row = []
        headers = self.headers
        for col in headers:
            hprops = self.data.get('properties', {}).get(col[0], {})
            columnLabel = (
                hprops.get('label', col[0])
                if isinstance(hprops, dict) else col[0]
            )
            columnType = (
                hprops.get('columnType', hprops.get('valueType', 'text'))
                if isinstance(hprops, dict) else hprops
            )
            header = u'%s:%s' % (columnLabel, columnType)
            row.append(header.encode('utf-8'))
        writter.writerow(row)

        for item in self.data['items']:
            row = []
            for col in headers:
                hprops = self.data.get('properties', {}).get(col[0], {})
                columnType = (
                    hprops.get('columnType', hprops.get('valueType', 'text'))
                    if isinstance(hprops, dict) else hprops
                )
                if columnType == 'boolean' and \
                    (item.get(col[0], None) is None or
                     item.get(col[0], None) == 'null'):
                    row.append('null')
                else:
                    row.append(
                        unicode(item.get(col[0], '')).encode('utf-8')
                    )
            writter.writerow(row)

        text = u''
        if not attachment:
            output.seek(0)
            text = output.read()
            if isinstance(text, str):
                text = text.decode('utf-8')
        return text

    def tsv(self, dialect='eea.app.visualization.tsv', attachment=True):
        """ Download as Tab Separated File

            >>> output = sandbox.restrictedTraverse('@@download.tsv')
            >>> print output(attachment=False)
            FacilityID:number	FacilityName:text...
            ...
            118563	ENI SpA Divisione Refining & Marketing...

            Load another set of data from a json file and use that to generate
            a new Tab Separated File

            >>> import json
            >>> from eea.app.visualization.tests.utils import loadfile
            >>> data_file = loadfile('data/data-sample-v5.json')
            >>> data = json.loads(data_file.get('data'))
            >>> download = sandbox.restrictedTraverse('@@download.table')
            >>> download._data = data
            >>> out = download.tsv(attachment=False)
            >>> print out
            Country:text        ValueA:boolean  ValueB:boolean
            Italy       null    False
            France      null    True
            Germany     True    null
            Spain       True    False
            Hungary     False   null

        """
        return self.csv(dialect=dialect, attachment=attachment)

    def json(self):
        """ Downlaod as JSON

            >>> output = sandbox.restrictedTraverse('@@download.json')
            >>> print output()
            {
              "head": {
                "vars": [
                  "facilityid",
            ...
              "results": {
                "bindings": [
            ...
                "country": {
                  "datatype": "http://www.w3.org/2001/XMLSchema#string",
                  "type": "typed-literal",
                  "value": "Italy"
                },
            ...

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
                    "value": item.get(header[0])
                }
            data['results']['bindings'].append(convertedItem)

        return json.dumps(data, indent=2)

    def exhibit(self):
        """ Download as Exhibit JSON

            >>> output = sandbox.restrictedTraverse('@@download.exhibit')
            >>> print output()
            {
              "items": [
                {
            ...
                    "main_activity": "Energy - Mineral oil and gas refineries",
            ...
              ],
              "properties":{
            ...
                "main_activity": {"valueType": "text", "columnType": ...
            ...

        """
        self.request.response.setHeader(
            'Content-Type', 'application/json')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s.exhibit.json"' % self.context.getId())
        return self.sortProperties(json.dumps(self.data, indent=2), indent=2)

    def xml(self):
        """ Download as XML

            >>> output = sandbox.restrictedTraverse('@@download.xml')
            >>> print output()
            <?xml version='1.0' encoding='UTF-8'?>
            <sparql xmlns=...http://www.w3.org/2005/sparql-results#...>
              <head>
                <variable name="facilityid"/>
            ...
            <results>
              <result>
                <binding name="facilityid">
                  <literal ...>1298</literal>
            ...
            <binding name="main_activity">
              <literal...>Energy - Mineral oil and gas refineries</literal>
            </binding>
            ...
            <BLANKLINE>

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

            >>> output = sandbox.restrictedTraverse('@@download.schema.xml')
            >>> print output()
            <?xml version="1.0" encoding="UTF-8"?>
            <root xmlns:xsd="http://www.w3.org/2001/XMLSchema">
              <dataroot>
                <resources>
                  <facilityid>1298</facilityid>
            ...
                  <main_activity>Energy - Mineral oil and gas refineries...
            ...
              </dataroot>
              <xsd:schema>
                <xsd:element name="dataroot">
            ...
                <xsd:element minOccurs="0" ...name="facilityid".../>
            ...

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
