""" LatLong utility
"""
from zope.component import getUtility
from eea.app.visualization.converter.types.interfaces import IGuessType

class GuessLatLong(object):
    """
    Is provided text a valid latlong text::

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'latlong')

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


    You can also force the type from column header::

        >>> guess('I was forced to be a LatLong', label='geolocation:latlong')
        True

        >>> guess('I was forced to be a LatLong', label='geolocation:latlng')
        True

        >>> guess('I was forced to be a Longitude', label='geo:LatLong')
        True

    """
    def __call__(self, text, label=''):
        if label and ':latlong' in label.lower():
            return True

        if label and ':latlng' in label.lower():
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
