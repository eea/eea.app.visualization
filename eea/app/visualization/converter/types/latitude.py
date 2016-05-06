""" Latitude utility
"""
import logging
from eea.app.visualization.converter.types import GuessType

logger = logging.getLogger('eea.app.visualization')

class GuessLatitude(GuessType):
    """ Utility to guess and convert text to latitude:

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'latitude')
        >>> guess
        <eea.app.visualization.converter.types.latitude.GuessLatitude object...>

    """
    order = 30
    priority = -2
    aliases = (u'lat', u'latitude')
    fmt = '%.6f'

    def convert(self, text, fallback=None, **options):
        """
        Convert text to latitude

            >>> guess.convert('42.3456')
            42.345...

        You can use fallback to force text to latitude:

            >>> guess.convert('42.3456.', fallback=0)
            0
            >>> guess.convert('42.3456.',
            ...               fallback=lambda x: float(x.strip('.')))
            42.345...

        If you don't provide a fallback for a wrong value, a ValueError will be
        raised:

            >>> guess.convert('A latitude: 23.45')
            Traceback (most recent call last):
            ...
            ValueError: A latitude: 23.45

        You can also convert given text to another text providing 'format'
        keyword:

            >>> guess.convert('42.3432', format='%.2f')
            '42.34'

        """
        try:
            text = float(text)
        except Exception:
            if fallback is not None:
                if callable(fallback):
                    text = fallback(text)
                else:
                    text = fallback
            else:
                raise ValueError(text)

        if not isinstance(text, float):
            return text

        strformat = options.get('format', None)
        if not strformat:
            return text

        return strformat % text

    def __call__(self, text, label=''):
        """
        Is provided text a valid latitude number:

            >>> guess('46.232')
            True
            >>> guess('-90')
            True
            >>> guess('0')
            True
            >>> guess('90')
            True

            >>> guess('90.001')
            False
            >>> guess('-90.001')
            False
            >>> guess('89.34.45')
            False
            >>> guess('43,25')
            False

        You can also force the type from column header:

            >>> guess('I was forced to be a Latitude', label='latitude:lat')
            True
            >>> guess('I was forced to be a Latitude', label='lat:Latitude')
            True

        """
        for alias in self.aliases:
            if isinstance(alias, unicode):
                alias = alias.encode('utf-8')
            if ':%s' % alias in label.lower():
                return True

        try:
            text = float(text)
        except Exception:
            return False

        if -90 <= text <= 90:
            return True
        return False
