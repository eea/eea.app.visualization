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
    order = 70

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
            >>> guess.convert('Jan 2012')
            datetime.datetime(2012, 1...)

            >>> guess.convert('1 Ianuarie 2012')
            '1 Ianuarie 2012'

        You can use fallback to force text to datetime:

            >>> from datetime import datetime
            >>> guess.convert('1 Ianuarie 2012', fallback=datetime(1970, 1, 1))
            datetime.datetime(1970, 1, 1, 0, 0)

            >>> from dateutil.parser import parse
            >>> guess.convert('1 Ianuarie 2012',
            ...       fallback=lambda x: parse(x.replace('Ianuarie', 'Jan')))
            datetime.datetime(2012, 1, 1, 0, 0)

        You can also convert given text to another text providing 'format'
        keyword:

            >>> guess.convert('Dec 13, 2012', format='%Y/%m/%d')
            '2012/12/13'

        """
        try:
            text = parser.parse(text)
        except Exception:
            if fallback is not None:
                if callable(fallback):
                    text = fallback(text)
                else:
                    text = fallback

        if not isinstance(text, datetime):
            return text

        strftime = options.get('format', None)
        if not strftime:
            return text

        return text.strftime(strftime)


    def __call__(self, text, label=''):
        """
        Is provided text a Date:

            >>> guess('0')
            False
            >>> guess('1')
            True
            >>> guess('2012')
            True
            >>> guess('3245')
            True
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

        if label and ":date" in label.lower():
            return True

        try:
            parser.parse(text)
        except Exception:
            return False
        return True
