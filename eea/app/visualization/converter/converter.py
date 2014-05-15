""" Converter module responsible for converting from cvs to json
"""
import logging
import csv
import warnings
from StringIO import StringIO
from zope.component import getUtility, queryUtility
from zope.interface import implements
from eea.app.visualization.interfaces import IGuessType
from eea.app.visualization.interfaces import IGuessTypes
from eea.app.visualization.interfaces import ITable2JsonConverter
from eea.app.visualization.interfaces import IVisualizationJsonUtils

logger = logging.getLogger("eea.app.visualization.converter")

class EEADialectTab(csv.Dialect):
    """ CSV dialect having tab as delimiter
    """
    delimiter = '\t'
    quotechar = '"'
    # Should be set to quotechar = csv.QUOTE_NONE when we will use Python 2.5
    # as setting quotechar to nothing does not work in Python 2.4.
    # For more details see
    # http://stackoverflow.com/questions/494054/
    # how-can-i-disable-quoting-in-the-python-2-4-csv-reader/494126
    escapechar = '\\'
    doublequote = False
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_NONE

csv.register_dialect("eea-tab", EEADialectTab)

class Table2JsonConverter(object):
    """ Utility to convert csv to json

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.interfaces import \
        ...      ITable2JsonConverter

        >>> converter = getUtility(ITable2JsonConverter)
        >>> converter
        <eea.app.visualization.converter.converter.Table2JsonConverter ...>

    """
    implements(ITable2JsonConverter)

    def dialect(self, datafile):
        """ Try to guess CSV dialect
        """
        if isinstance(datafile, (unicode, str)):
            datafile = StringIO(datafile)

        datafile.seek(0)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(datafile.read(4096),
                                    delimiters='\t ;,:')
        except Exception, err:
            logger.debug(err)
            dialect = 'eea-tab'
        datafile.seek(0)
        return dialect

    def sample(self, datafile, rows=21):
        """ Get CSV sample from datafile

        >>> csvfile = '\n'.join((
        ...   'label,   year, country',
        ...   'romania, 2010, Romania',
        ...   'italy,   2011, Italy',
        ...   'france,  2012, France',
        ... ))

        >>> for row in converter.sample(csvfile, rows=1):
        ...     print '   '.join(row)
        label   year   country
        romania   2010   Romania

        """
        if isinstance(datafile, (unicode, str)):
            datafile = StringIO(datafile)

        datafile.seek(0)
        reader = csv.reader(datafile, dialect=self.dialect(datafile))
        sample = []
        for index, row in enumerate(reader):
            if not row:
                rows += 1
                continue
            if index > rows:
                return sample
            sample.append(row)
        return sample

    def text_annotation(self, text, annotations=()):
        """ Extract text and annotation from given text based on
        annotations dict

        >>> converter.text_annotation('4438868(s)', annotations=[
        ...   {'name': u'(s)', 'title': u'Eurostat estimate'},
        ...   {'name': u':', 'title': u'Not available'},
        ... ])
        (u'4438868', u'Eurostat estimate')

        """
        for annotation in annotations:
            name = annotation.get('name')
            if not name:
                continue

            if not isinstance(text, (str, unicode)):
                text = repr(text)

            if text.find(name) != -1:
                return text.replace(name, ''), annotation.get('title', name)
        return text, u''

    def __call__(self, datafile, column_types=None, **kwargs):
        """
        Returns: columns_headers_with_type, exhibit_dict:

          ( <generator
              (('label', 'text'), ('year', 'date'), ('country', 'text'))>,

            {'items': [
                {'country': 'Romania', 'year': '2010', 'label': 'romania'},
              ],
             'properties': {
               'country': {'valueType': 'text'},
               'year': {'valueType': 'text'},
               'label': {'valueType': 'text'}
              }
            }
          )

        Let's see how it works:

          CSV

            >>> csvfile = '\n'.join((
            ...   'label, year:date, country, latit:lat, longitude:long, popul',
            ...   'romania, 2010, Romania, 45.7666667, 27.9833333, 95',
            ...   'italy, 2012, Italy, 42.763667, 12.9833333, 10',
            ...   'junk, , n.a., Junk, 34, 12'
            ... ))

            >>> columns, jsondict = converter(csvfile)

            >>> print '\n'.join(' => '.join(x) for x in columns)
            label => text
            year => date
            country => text
            latit => latitude
            longitude => longitude
            popul => number

            >>> jsondict['properties']['year']
            {'valueType': u'date', 'columnType': u'date', 'order': 1, ...}

            >>> jsondict['items'][0]['year']
            '2010-...'

            >>> jsondict['properties']['latit']
            {'valueType': u'text', 'columnType': u'latitude', 'order': 3, ...}

            >>> jsondict['items'][0]['longitude']
            '27.983333'

          TSV

            >>> tabfile = '\n'.join((
            ...   'label, year:number, country',
            ...   'romania, one, Romania',
            ... ))

            >>> columns, jsondict = converter(tabfile)
            >>> [x for x in columns]
            [('label', u'text'), ('year', u'number'), ('country', u'text')]

            >>> jsondict['properties']['year']
            {'valueType': u'number', 'columnType': u'number', 'order': 1, ...}

        """
        if isinstance(datafile, (unicode, str)):
            datafile = StringIO(datafile)

        columns = []
        hasLabel = False
        out = []
        properties = {}
        annotations = kwargs.get('annotations', {})

        guess = getUtility(IGuessTypes)

        if not column_types:
            sample = self.sample(datafile)
            column_types = guess(sample)

        datafile.seek(0)
        reader = csv.reader(datafile, dialect=self.dialect(datafile))

        for index, row in enumerate(reader):
            # Ignore empty rows
            if row == []:
                continue

            # Get column headers
            if columns == []:
                for name in row:
                    name = name.strip()
                    columnLabel = guess.column_label(name)
                    name = name.replace(' ', '+')
                    if name.lower().endswith('label'):
                        name = "label"
                        hasLabel = True
                    name, columnType = guess.column_type(name)
                    columns.append((
                        name,
                        column_types.get(name, columnType or u'text'),
                        columnLabel
                    ))

                    # Annotations
                    if name in annotations:
                        anno = annotations[name]
                        columns.append((
                            anno.get('name', name + u'__annotations__'),
                            anno.get('columnType', u'annotations'),
                            anno.get('label', name + u':annotations')
                        ))
                continue

            # Create JSON
            row = iter(row)
            data = {}

            # Required by Exhibit
            if not hasLabel:
                data['label'] = index

            order = 0
            for col, columnType, columnLabel in columns:
                if columnType == u'annotations':
                    continue

                try:
                    text = row.next()
                except StopIteration:
                    text = u''

                util = queryUtility(IGuessType, name=columnType)
                valueType = getattr(util, 'valueType', columnType)
                fmt = getattr(util, 'fmt', None)

                # Annotations
                anno = annotations.get(col, None)
                if anno:
                    text, annotation = self.text_annotation(
                        text, anno.get('annotations', []))
                    data[anno.get('name',
                                  col + u'__annotations__')] = annotation

                try:
                    text = (util.convert(text, fallback=None, format=fmt)
                            if util else text)
                except ValueError, err:
                    # Skip key: value from JSON
                    logger.debug(err)
                else:
                    data[col] = text


                properties[col] = {
                    "valueType": valueType,
                    'columnType': columnType,
                    'label': columnLabel,
                    "order": order
                }
                order += 1

                # Annotations
                if anno:
                    properties[anno.get('name', col + u'__annotations__')] = {
                        "valueType": anno.get('valueType', u'text'),
                        'columnType': anno.get('columnType', u'annotations'),
                        'label': anno.get('label', col + u':annotations'),
                        "order": order
                    }
                    order += 1

            out.append(data)

        return (
            [(x[0], x[1]) for x in columns],
            {'items': out, 'properties': properties}
        )

def sortProperties(strJson, indent=1):
    """ In the json string set the correct order of the columns
    """
    warnings.warn(
        "eea.app.visualization.converter.converter.sortProperties is "
        "deprecated. Please use "
        "eea.app.visualization.interfaces.IVisualizationJsonUtils "
        "utility instead",
        DeprecationWarning
    )

    utils = queryUtility(IVisualizationJsonUtils)
    return utils(strJson, indent)
