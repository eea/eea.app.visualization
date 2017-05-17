""" Convert data to table utilities
"""
import json
import csv
import logging
from StringIO import StringIO
from zope.interface import implements
from zope.component import queryUtility
from eea.app.visualization.interfaces import IData2TableConverter
from eea.app.visualization.converter.csvutils import UnicodeWriter
logger = logging.getLogger('eea.app.visualization')


class CSV(object):
    """ Utility to get visualization data from external TSV

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.interfaces import IData2TableConverter

        >>> data = getUtility(IData2TableConverter, name=u'text/csv')
        >>> data
        <eea.app.visualization.converter.data.CSV ...>

    """

    implements(IData2TableConverter)

    def __call__(self, data):
        return data


class JSON(object):
    """ Utility to get visualization data from external TSV

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.interfaces import IData2TableConverter

        >>> data = getUtility(IData2TableConverter, name=u'application/json')
        >>> data
        <eea.app.visualization.converter.data.JSON ...>

    """

    implements(IData2TableConverter)

    def listing(self, data):
        """ JSON is a list of items
        """
        if not data:
            return u''

        columns = data[0]
        if not isinstance(columns, dict):
            return u''

        columns = columns.keys()

        output = StringIO()
        writer = UnicodeWriter(output)

        writer.writerow(columns)
        for item in data:
            row = []
            for key in columns:
                value = item.get(key, u'')
                if isinstance(value, (list, tuple)):
                    value = u';'.join(value)
                row.append(value)
            writer.writerow(row)

        output.seek(0)
        return output.read()

    def exhibit(self, data):
        """ JSON is an Exhibit JSON
        """
        items = data.get('items', [])
        if not items:
            return u''

        properties = data.get('properties', {})
        columns = properties.keys()
        if not columns:
            columns = items[0].keys()

        output = StringIO()
        writer = UnicodeWriter(output)

        row = []
        for column in columns:
            col = (properties[column]
                   if isinstance(properties.get(column, None), dict) else {})
            ctype = col.get('columnType', col.get('valueType', ''))
            if ctype:
                column = u"%s:%s" % (column, ctype)
            row.append(column)
        writer.writerow(row)

        for item in items:
            row = []
            for column in columns:
                value = item.get(column, u'')
                if isinstance(value, (list, tuple)):
                    value = u';'.join(value)
                row.append(value)
            writer.writerow(row)

        output.seek(0)
        return output.read()

    def json(self, data):
        """ JSON is an Eionet JSON
        """
        items = data.get('results', {}).get('bindings', [])
        if not items:
            return u''

        columns = data.get('head', {}).get('vars', [])
        if not columns:
            columns = items[0].keys()

        output = StringIO()
        writer = UnicodeWriter(output)

        row = []
        for column in columns:
            data = items[0].get(column, {})
            ctype = data.get('datatype', u'').replace(
                'http://www.w3.org/2001/XMLSchema#', '')
            if ctype == 'double':
                ctype = 'number'
            if ctype:
                column = u"%s:%s" % (column, ctype)
            row.append(column)
        writer.writerow(row)

        for item in items:
            row = []
            for column in columns:
                value = item.get(column, {}).get('value', u'')
                if isinstance(value, (tuple, list)):
                    value = u';'.join(value)
                row.append(value)
            writer.writerow(row)

        output.seek(0)
        return output.read()

    def __call__(self, data):
        try:
            data = json.loads(data)
        except Exception:
            return u''

        # List of items JSON
        if isinstance(data, list):
            return self.listing(data)

        if not isinstance(data, dict):
            return u''

        # Exhibit JSON
        if 'items' in data or 'properties' in data:
            return self.exhibit(data)

        # Eionet JSON
        if 'head' in data or 'results' in data:
            return self.json(data)

        return u''


class Text(object):
    """ Utility to get visualization data from external text/plain URL

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.interfaces import IData2TableConverter

        >>> data = getUtility(IData2TableConverter, name=u'text/plain')
        >>> data
        <eea.app.visualization.converter.data.Text ...>

    """
    implements(IData2TableConverter)

    def __call__(self, data):
        # Maybe it's a JSON file
        try:
            json.loads(data)
        except Exception, err:
            logger.debug(err)
        else:
            util = queryUtility(IData2TableConverter, name='application/json')
            return util(data)

        # Maybe it's a CSV file
        try:
            sniffer = csv.Sniffer()
            sniffer.sniff(data[:1024])
        except Exception, err:
            logger.debug(err)
        else:
            util = queryUtility(IData2TableConverter, name='text/csv')
            return util(data)

        return u''
