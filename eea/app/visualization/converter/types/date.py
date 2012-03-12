""" Date utility
"""
from dateutil import parser

class GuessDate(object):
    """
    Is provided text a Date::

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'date')

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

        >>> guess('2012.12.23')
        True

        >>> guess('2012.12.23 12:34PM')
        True

        >>> guess('23.12.2001 23:34')
        True

        >>> guess('12:34PM')
        True

        >>> guess('23:01')
        True

        >>> guess('2012/23/12')
        False

        >>> guess('2012.23.12')
        False

        >>> guess('23.45.6')
        False

        >>> guess('2012 23 45')
        False

    You can also force the type from column header::

        >>> guess('I was forced to be a Date', label='exists:date')
        True

        >>> guess('I was forced to be a Date', label='exists:DateTime')
        True

    """

    def __call__(self, text, label=''):
        if label and ":date" in label.lower():
            return True

        try:
            parser.parse(text)
        except Exception:
            return False
        return True
