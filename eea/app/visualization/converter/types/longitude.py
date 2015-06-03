""" Longitude utility
"""
from eea.app.visualization.converter.types import GuessType

class GuessLongitude(GuessType):
    """ Utility to guess and convert text to longitude:

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'longitude')
        >>> guess
        <eea.app.visualization.converter.types.longitude.GuessLongitude...>

    """
    order = 40
    priority = -2
    aliases = ('long', 'lng', 'lon', 'longitude')
    fmt = '%.6f'

    def convert(self, text, fallback=None, **options):
        """
        Convert text to longitude

            >>> guess.convert('42.3456')
            42.345...

        You can use fallback to force text to longitude:

            >>> guess.convert('42.3456.', fallback=0)
            0
            >>> guess.convert('42.3456.',
            ...               fallback=lambda x: float(x.strip('.')))
            42.345...

        If you don't provide a fallback for a wrong value, a ValueError will be
        raised:

            >>> guess.convert('A longitude: 23.45')
            Traceback (most recent call last):
            ...
            ValueError: A longitude: 23.45

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
        Is provided text a valid longitude number:

            >>> guess('46.232')
            True
            >>> guess('-180')
            True
            >>> guess('0')
            True
            >>> guess('180')
            True

            >>> guess('180.001')
            False
            >>> guess('-180.001')
            False
            >>> guess('89.34.45')
            False
            >>> guess('43,25')
            False

        You can also force the type from column header:

            >>> guess('I was forced to be a Longitude', label='longitude:long')
            True
            >>> guess('I was forced to be a Longitude', label='long:Longitude')
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

        if -180 <= text <= 180:
            return True
        return False
