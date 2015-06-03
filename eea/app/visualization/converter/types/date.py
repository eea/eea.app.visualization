""" Date utility
"""
import logging
from datetime import datetime
from dateutil import parser
from eea.app.visualization.converter.types import GuessType
logger = logging.getLogger('eea.app.visualization')


class GuessDate(GuessType):
    """ Utility to guess and convert text to date:

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'date')
        >>> guess
        <eea.app.visualization.converter.types.date.GuessDate object...>

    """
    order = 60
    priority = -1
    aliases = (u'date', u'datetime', u'time')
    valueType = u'date'
    fmt = '%Y-%m-%d'

    def convert(self, text, fallback=None, **options):
        """
        Convert text to date

            >>> guess.convert('2011')
            datetime.datetime(2011...)
            >>> guess.convert('2012.12.13')
            datetime.datetime(2012, 12, 13, 0, 0)
            >>> guess.convert('13.12.2012')
            datetime.datetime(2012, 12, 13, 0, 0)
            >>> guess.convert('Dec 13, 2012')
            datetime.datetime(2012, 12, 13, 0, 0)
            >>> guess.convert('Jan 1973')
            datetime.datetime(1973, 1...)

        You can use fallback to force text to datetime:

            >>> from datetime import datetime
            >>> guess.convert('1 Ianuarie 2012', fallback=datetime(1970, 1, 1))
            datetime.datetime(1970, 1, 1, 0, 0)

            >>> from dateutil.parser import parse
            >>> guess.convert('1 Ianuarie 2012',
            ...       fallback=lambda x: parse(x.replace('Ianuarie', 'Jan')))
            datetime.datetime(2012, 1, 1, 0, 0)

            >>> guess.convert('', fallback=lambda x: 'n.a.')
            'n.a.'

            >>> guess.convert('  \t  \t', fallback=lambda x: 'n.a.')
            'n.a.'

        If you don't provide a fallback for a wrong value, a ValueError will be
        raised:

            >>> guess.convert('1 Ianuarie 2012')
            Traceback (most recent call last):
            ...
            ValueError: 1 Ianuarie 2012

            >>> guess.convert('')
            Traceback (most recent call last):
            ...
            ValueError

            >>> guess.convert('  \t  \t')
            Traceback (most recent call last):
            ...
            ValueError:

        You can also convert given text to another text providing 'format'
        keyword:

            >>> guess.convert('Dec 13, 1601', format=guess.fmt)
            '1601-12-13'

        """
        try:
            if not text.strip():
                raise ValueError(text)
            text = parser.parse(text)
        except Exception:
            if fallback is not None:
                if callable(fallback):
                    text = fallback(text)
                else:
                    text = fallback
            else:
                raise ValueError(text)

        if not isinstance(text, datetime):
            return text

        strftime = options.get('format', None)
        if not strftime:
            return text

        return text.isoformat().split('T')[0]


    def __call__(self, text, label=''):
        """
        Is provided text a Date:

            >>> guess('0')
            False
            >>> guess('1')
            False
            >>> guess('2012')
            True
            >>> guess('3245')
            False
            >>> guess('2500')
            True
            >>> guess('2012/12/23')
            True
            >>> guess('23.12.2012')
            True
            >>> guess('Dec 23, 2012')
            True
            >>> guess('2012.12.23 12:34PM')
            True
            >>> guess('23.12.2001 23:34')
            True
            >>> guess('12:34PM')
            True
            >>> guess('23:01')
            True

            >>> guess('I am not a date: 2012.12.13')
            False
            >>> guess('2012/23/12')
            False
            >>> guess('2012.23.12')
            False
            >>> guess('23.45.6')
            False
            >>> guess('2012 23 45')
            False

        You can also force the type from column header:

            >>> guess('I was forced to be a Date', label='exists:date')
            True
            >>> guess('I was forced to be a Date', label='exists:DateTime')
            True

        """

        for alias in self.aliases:
            if isinstance(alias, unicode):
                alias = alias.encode('utf-8')
            if ':%s' % alias in label.lower():
                return True

        # Year
        try:
            year = int(text)
        except Exception:
            year = 1
        else:
            if 1500 <= year <= 2500:
                return True
            return False

        # Date
        try:
            parser.parse(text)
        except Exception:
            return False
        return True
