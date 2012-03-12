""" Longitude utility
"""
class GuessLongitude(object):
    """
    Is provided text a valid longitude number::

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'longitude')

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


    You can also force the type from column header::

        >>> guess('I was forced to be a Longitude', label='longitude:long')
        True

        >>> guess('I was forced to be a Longitude', label='long:Longitude')
        True

    """
    def __call__(self, text, label=''):
        if label and ':long' in label.lower():
            return True

        try:
            text = float(text)
        except Exception:
            return False

        if -180 <= text <= 180:
            return True
        return False
