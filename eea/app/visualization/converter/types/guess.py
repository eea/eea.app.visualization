""" Guess All Types utility
"""
import re
import operator
from zope.component import getUtilitiesFor, queryUtility
from zope.interface import implements
from plone.i18n.normalizer.interfaces import IIDNormalizer
from eea.app.visualization.converter.types.interfaces import IGuessType
from eea.app.visualization.converter.types.interfaces import IGuessTypes
from eea.app.visualization.config import DATA_ANNOTATIONS
from eea.app.visualization.interfaces import IDavizSettings

REGEX = re.compile(r"[\W]+")

def normalizeString(text, context=None, encoding=None):
    """
    The relaxed mode was removed in Plone 4.0. You should use either the url
    or file name normalizer from the plone.i18n package instead.
    """
    return queryUtility(IIDNormalizer).normalize(text, max_length=255)

def compare(a, b):
    """ Compare utilities tuples
    """
    return cmp(a[1].order, b[1].order)

class GuessTypes(object):
    """ Guess types utility

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessTypes
        >>> guess = getUtility(IGuessTypes)
        >>> guess
        <eea.app.visualization.converter.types.guess.GuessTypes object...>

    """
    implements(IGuessTypes)

    @property
    def missing(self):
        """ Missing annotations
        """
        tool = queryUtility(IDavizSettings)
        if not tool:
            return set(DATA_ANNOTATIONS)

        anno = tool.settings.get('data.annotations')
        if anno is None:
            return set(DATA_ANNOTATIONS)

        anno = set(anno.splitlines())
        anno.add('')
        return anno

    def column_type(self, column):
        """ Get column and type from column name

            >>> guess.column_type("start:Date")
            ('start', 'date')

            >>> guess.column_type("Website:URL")
            ('website', 'url')

            >>> guess.column_type("Items: one, two:List")
            ('items_one_two', 'list')

            >>> guess.column_type("Title")
            ('title', '')

            >>> guess.column_type("Title is some-thing. + something @lse")
            ('title_is_some_thing_something_lse', '')

        """

        if ":" not in column:
            column = normalizeString(column, encoding='utf-8')
            column = REGEX.sub('_', column)
            return column, ""

        columnType = column.split(":")[-1].lower()
        column = ":".join(column.split(":")[:-1])
        column = normalizeString(column, encoding='utf-8')
        column = REGEX.sub('_', column)
        return column, columnType

    def column_label(self, column):
        """ Extract column label from column name
        """
        if isinstance(column, str):
            column = column.decode('utf-8')
        if u":" not in column:
            return column
        return u":".join(column.split(u":")[:-1])

    def guessUtility(self, columnType=''):
        """ Get guess utility from columnType
        """
        if not columnType:
            return None, None

        for name, util in getUtilitiesFor(IGuessType):
            if columnType in util.aliases:
                return name, util
        return None, None

    def guessHeader(self, header, output):
        """ Column type is forced in header using :type syntax
        """
        for label in header:
            title, columnType = self.column_type(label)
            name, util = self.guessUtility(columnType)
            if util:
                output[title] = {name: 99999}
        return output

    def guessBody(self, table, header, output):
        """ Discover column types from table body
        """
        utilities = getUtilitiesFor(IGuessType)
        utilities = sorted(utilities, cmp=compare)

        missing = self.missing

        for row in table:
            for index, cell in enumerate(row):
                # Skip missing values
                if cell.lower().strip() in missing:
                    continue

                label = header[index]
                title, columnType = self.column_type(label)

                # Type in header, skip this column
                if columnType:
                    continue

                output.setdefault(title, {})
                for name, guess in utilities:
                    if guess(cell, label):
                        output[title].setdefault(name, guess.priority)
                        output[title][name] += 1

    def __call__(self, datatable):
        """ Guess CSV column types

            >>> csvtable = [
            ... ['label:label', 'Year', 'country', 'Map', 'Population', 'EU'],
            ... ['romania', '2010', 'Romania', '45.76, 27.98', '21959278', 'y'],
            ... ['italy', '2012', 'Italy', '42.8333, 12.83', '60340328', 'N'],
            ... ['china', '', '-', '12.123, 34.542', '3423432', 'N']
            ... ]

            >>> mapping = guess(csvtable)
            >>> print '\n'.join(' => '.join(x) for x in sorted(mapping.items()))
            country => text
            eu => boolean
            label => text
            map => latlong
            population => number
            year => year

        You can't guess latitude and longitude as they are numbers, and you
        don't want to detect, for example, a percent column as latitude:

            >>> csvtable = [
            ...   ['Country', 'Working Population'],
            ...   ['Romania', '57.43'],
            ...   ['Italy', '83.45']
            ... ]

            >>> mapping = guess(csvtable)
            >>> print '\n'.join(' => '.join(x) for x in sorted(mapping.items()))
            country => text
            working_population => number

        If you still want to detect latitude and longitude, add this in label:

            >>> csvtable = [
            ...   ['Country', 'y:latitude', 'x:longitude'],
            ...   ['Romania', '45.76', '27.98'],
            ...   ['Italy', '42.83', '12.83'],
            ... ]

            >>> mapping = guess(csvtable)
            >>> print '\n'.join(' => '.join(x) for x in sorted(mapping.items()))
            country => text
            x => longitude
            y => latitude

        """
        mapping = {}
        if not datatable:
            return mapping

        csvtable = datatable[:]
        header = csvtable.pop(0)

        # Discover column types in table header
        self.guessHeader(header, mapping)

        # Discover column types in table body
        if set(header).difference(mapping.keys()):
            self.guessBody(csvtable, header, mapping)

        res = {}
        for label, statistics in sorted(mapping.items()):
            types = sorted(statistics.items(), key=operator.itemgetter(1),
                           reverse=True)
            res[label] = types[0][0]
        return res
