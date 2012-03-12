""" Boolean utility
"""
BOOLEAN = frozenset(('yes', 'no', 'true', 'false', '0', '1', ''))

class GuessBoolean(object):
    """
    Is provided text a Boolean::

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'boolean')
        >>> guess('yes')
        True

        >>> guess('No')
        True


        >>> guess('0')
        True

        >>> guess('1')
        True

        >>> guess('2')
        False

        >>> guess('true')
        True

        >>> guess('FALSE')
        True

        >>> guess('')
        True

        >>> guess('   ')
        True

        >>> guess('Oui')
        False

        >>> guess('o')
        False

    You can also force the type from column header::

        >>> guess('I was forced to be a Boolean', label='exists:bool')
        True

        >>> guess('I was forced to be a Boolean', label='exists:Boolean')
        True

    """
    def __call__(self, text, label=''):
        if label and ":bool" in label.lower():
            return True

        if text.strip().lower() in BOOLEAN:
            return True
        return False
