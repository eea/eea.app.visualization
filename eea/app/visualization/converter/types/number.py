""" Number utility
"""
class GuessNumber(object):
    """
    Is provided text a Number::

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'number')

        >>> guess('0')
        True

        >>> guess('2')
        True

        >>> guess('2.0')
        True

        >>> guess(' 234.3423423   ')
        True

        >>> guess('')
        False

        >>> guess('23,456')
        False

        >>> guess('23.45.6')
        False

        >>> guess('23 45')
        False

    You can also force the type from column header::

        >>> guess('I was forced to be a Number', label='exists:int')
        True

        >>> guess('I was forced to be a Number', label='exists:Integer')
        True

        >>> guess('I was forced to be a Number', label='exists:Number')
        True

    """
    def __call__(self, text, label=''):
        if label and ":int" in label.lower():
            return True

        if label and ":number" in label.lower():
            return True

        try:
            float(text)
        except Exception:
            return False
        return True
