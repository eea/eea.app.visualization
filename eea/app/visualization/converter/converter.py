""" Converter module responsible for converting from cvs to json
"""
import logging
import csv
from StringIO import StringIO
from zope.component import getUtility, queryUtility
from zope.interface import implements
from eea.app.visualization.interfaces import IGuessType
from eea.app.visualization.interfaces import IGuessTypes
from eea.app.visualization.interfaces import IExhibitJsonConverter

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

class ExhibitJsonConverter(object):
    """ Utility to convert csv to json

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.interfaces import \
        ...      IExhibitJsonConverter

        >>> converter = getUtility(IExhibitJsonConverter)
        >>> converter
        <eea.app.visualization.converter.converter.ExhibitJsonConverter ...>

    """
    implements(IExhibitJsonConverter)

    def dialect(self, datafile):
        """ Try to guess CSV dialect
        """
        if isinstance(datafile, (unicode, str)):
            datafile = StringIO(datafile)

        datafile.seek(0)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(datafile.read(1024))
        except Exception, err:
            logger.debug(err)
            dialect = 'eea-tab'
        datafile.seek(0)
        return dialect

    def sample(self, datafile, rows=5):
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

    def __call__(self, datafile):
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
            ...   'romania, 2010, Romania, 45.7666667, 27.9833333, 2195',
            ...   'italy, 2012, Italy, 42.763667, 12.9833333, 2010',
            ...   'junk, , 2001, Junk, 34, 12'
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
            {'valueType': 'date'}

            >>> jsondict['items'][0]['year']
            '2010-...'

            >>> jsondict['properties']['latit']
            {'valueType': u'text'}

            >>> jsondict['items'][0]['longitude']
            '27.983333'

          TSV

            >>> tabfile = '\n'.join((
            ...   'label   \t year:number \t country',
            ...   'romania \t 2010        \t Romania',
            ... ))

            >>> columns, jsondict = converter(tabfile)
            >>> [x for x in columns]
            [('label', 'text'), ('year', u'number'), ('country', 'text')]

            >>> jsondict['properties']['year']
            {'valueType': u'number'}

        """
        if isinstance(datafile, (unicode, str)):
            datafile = StringIO(datafile)

        columns = []
        hasLabel = False
        out = []
        properties = {}

        sample = self.sample(datafile)
        guess = getUtility(IGuessTypes)
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
                    name = name.replace(' ', '+')
                    if name.lower().endswith('label'):
                        name = "label"
                        hasLabel = True
                    name, typo = guess.column_type(name)
                    columns.append((name, column_types.get(name, typo)))
                continue

            # Create JSON
            row = iter(row)
            data = {}

            # Required by Exhibit
            if not hasLabel:
                data['label'] = index

            for col, typo in columns:
                text = row.next()

                fmt = None
                valueType = typo
                if typo in ('latitude', 'longitude', 'latlong'):
                    fmt = '%.6f'
                    valueType = u'text'
                if typo in ('date'):
                    fmt = '%Y-%m-%d'
                util = queryUtility(IGuessType, name=typo)

                fallback = None
                if typo in ('boolean', 'latitude', 'longitude', 'number'):
                    fallback = 0
                elif typo in ('latlong',):
                    fallback = '0, 0'
                elif typo in ('date',):
                    fallback = '1970-01-01'

                text = (util.convert(text, fallback=fallback, format=fmt)
                        if util else text)
                data[col] = text

                properties[col] = {"valueType": valueType}

            out.append(data)

        return columns, {'items': out, 'properties': properties}
