""" Boolean utility
"""
from eea.app.visualization.converter.types import GuessType

TRUE = frozenset(('yes', 'true', '1', 'x', 'y'))
FALSE = frozenset(('no', 'false', '0', '', 'n'))

class GuessBoolean(GuessType):
    """ Utility to guess and convert text to boolean:

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'boolean')
        >>> guess
        <eea.app.visualization.converter.types.boolean.GuessBoolean object...>

    """
    order = 20

    def convert(self, text, fallback=None, **options):
        """
        Convert text to boolean:

            >>> guess.convert('False')
            False
            >>> guess.convert('true')
            True
            >>> guess.convert('YES')
            True
            >>> guess.convert('0')
            False
            >>> guess.convert('')
            False
            >>> guess.convert('x')
            True
            >>> guess.convert('n')
            False
            >>> guess.convert('Oui')
            'Oui'

        You can use fallback to force text to boolean:

            >>> guess.convert('Oui', fallback=False)
            False
            >>> guess.convert('Oui', fallback=bool)
            True

        """
        res = text.strip().lower()

        if res in TRUE:
            return True
        elif res in FALSE:
            return False

        if fallback is not None:
            if callable(fallback):
                return fallback(text)
            return fallback
        return text

    def __call__(self, text, label=''):
        """
        Is provided text a Boolean:

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
            >>> guess('X')
            True
            >>> guess('Y')
            True
            >>> guess('n')
            True
            >>> guess('Oui')
            False
            >>> guess('o')
            False

        You can also force the type from column header:

            >>> guess('I was forced to be a Boolean', label='exists:bool')
            True
            >>> guess('I was forced to be a Boolean', label='exists:Boolean')
            True

        """

        if label and ":bool" in label.lower():
            return True

        res = text.strip().lower()
        if res in TRUE:
            return True
        elif res in FALSE:
            return True
        return False
