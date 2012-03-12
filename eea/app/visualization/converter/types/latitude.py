""" Latitude utility
"""
class GuessLatitude(object):
    """
    Is provided text a valid latitude number::

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'latitude')

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


    You can also force the type from column header::

        >>> guess('I was forced to be a Latitude', label='latitude:lat')
        True

        >>> guess('I was forced to be a Latitude', label='lat:Latitude')
        True

    """
    def __call__(self, text, label=''):
        if label and ':lat' in label.lower():
            return True

        try:
            text = float(text)
        except Exception:
            return False

        if -90 <= text <= 90:
            return True
        return False
