""" LatLong utility
"""
from zope.component import getUtility
from eea.app.visualization.converter.types import GuessType
from eea.app.visualization.converter.types.interfaces import IGuessType

class GuessLatLong(GuessType):
    """ Utility to guess and convert text to latlong:

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'latlong')
        >>> guess
        <eea.app.visualization.converter.types.latlong.GuessLatLong...>

    """
    order = 50
    aliases = (u'latlong', u'latlng', u'latlon')
    fmt = '%.6f'

    def convert(self, text, fallback=None, **options):
        """
        Convert text to latlong

            >>> guess.convert('  42.3456    , 25.3434  ')
            '42.3456, 25.3434'

        You can use fallback to force text to latlong:

            >>> guess.convert('42,3456 25,345', fallback='0, 0')
            '0, 0'
            >>> guess.convert('42,3456 25,345',
            ...   fallback=lambda x: x.replace(',', '.').replace(' ', ', '))
            '42.3456, 25.345'

        If you don't provide a fallback for a wrong value, a ValueError will be
        raised:

            >>> guess.convert('A latlong: 23.45')
            Traceback (most recent call last):
            ...
            ValueError: A latlong: 23.45

        You can also convert given text to another text providing 'format'
        keyword:

            >>> guess.convert('42.3456, 25.3434', format='%.6f')
            '42.345600, 25.343400'

        """
        res = text.split(',')
        if len(res) != 2:
            if fallback is not None:
                if callable(fallback):
                    return fallback(text)
                return fallback
            else:
                raise ValueError(text)

        lat, lng = res
        guess = getUtility(IGuessType, 'latitude')
        lat = guess.convert(lat, **options)
        guess = getUtility(IGuessType, 'longitude')
        lng = guess.convert(lng, **options)

        return '%s, %s' % (lat, lng)

    def __call__(self, text, label=''):
        """
        Is provided text a valid latlong text:

            >>> guess('46.232, 25.345')
            True
            >>> guess('-90, -180')
            True
            >>> guess('0, 0')
            True
            >>> guess('90, 180')
            True

            >>> guess('90.0001, 180.001')
            False
            >>> guess('-90.0001, -180.001')
            False
            >>> guess('89,34,45')
            False
            >>> guess('43,25 34.56')
            False

        You can also force the type from column header:

            >>> guess('I was forced to be a LatLong', label='geo:latlong')
            True
            >>> guess('I was forced to be a LatLong', label='geo:latlng')
            True
            >>> guess('I was forced to be a Longitude', label='geo:LatLong')
            True

        """
        for alias in self.aliases:
            if isinstance(alias, unicode):
                alias = alias.encode('utf-8')
            if ':%s' % alias in label.lower():
                return True

        text = text.split(',')
        if len(text) != 2:
            return False

        lat, lng = text
        guess = getUtility(IGuessType, 'latitude')
        if not guess(lat):
            return False

        guess = getUtility(IGuessType, 'longitude')
        if not guess(lng):
            return False

        return True
