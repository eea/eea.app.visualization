""" Text utility
"""
from eea.app.visualization.converter.types import GuessType

class GuessText(GuessType):
    """ Utility to guess and convert text to text. This is a fallback utility,
    if none of the other utilities managed to guess type, this will apply

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'text')
        >>> guess
        <eea.app.visualization.converter.types.text.GuessText...>

    """
    priority = -3
    order = 200
    aliases = ('text', 'string', 'label')

    def convert(self, text, fallback=None, **options):
        """ Convert text

            >>> guess.convert('This is it')
            'This is it'

        You can use fallback to force text value:

            >>> guess.convert('', fallback='<NOT SET>')
            '<NOT SET>'

            >>> guess.convert('', fallback=lambda x: unicode(x))
            u''

        If you don't provide a fallback for a wrong value, a ValueError will be
        raised:

            >>> guess.convert(None)
            Traceback (most recent call last):
            ...
            ValueError: None

        """
        if not text:
            if fallback is not None:
                if callable(fallback):
                    return fallback(text)
                return fallback
            else:
                if text == "":
                    return text
                raise ValueError(text)

        return text

    def __call__(self, text, label=''):
        """
        Is provided text a Text:

            >>> guess('This is it')
            True

        """
        return True
