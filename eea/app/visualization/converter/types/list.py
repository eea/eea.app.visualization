""" List utility
"""
from eea.app.visualization.converter.types import GuessType

class GuessList(GuessType):
    """ Utility to guess and convert text to list:

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'list')
        >>> guess
        <eea.app.visualization.converter.types.list.GuessList...>

    """
    order = 80
    aliases = ('list', 'tuple', 'iter', 'iterator')

    def convert(self, text, fallback=None, **options):
        """
        Convert text to list

            Works with ";"
            >>> guess.convert('\t\n  Pig; \t\n Goat;\n Cow  \t\n\n')
            ['Pig', 'Goat', 'Cow']

            Also with ","
            >>> guess.convert('  Pig, Goat, Cow  ')
            ['Pig', 'Goat', 'Cow']

            If it can't find any comma or semicolon it will return
            a list of one item
            >>> guess.convert('  Pig')
            ['Pig']

        You can use fallback to force text to list:

            >>> guess.convert('Pig Goat Cow',
            ...   fallback=lambda x: x.split())
            ['Pig', 'Goat', 'Cow']


        """
        if "," in text:
            text = text.split(",")
        elif ";" in text:
            text = text.split(";")
        else:
            if fallback is not None:
                if callable(fallback):
                    text = fallback(text)
                else:
                    text = fallback
            else:
                if text.strip():
                    text = [text, ]
                else:
                    text = []

        text = [item.strip() for item in text]
        return text

    def __call__(self, text, label=''):
        """
        Is provided text a list:

            >>> guess("This shouldn't be a list, should it? "
            ...       "Or maybe it should, shouldn't it?")
            False

            >>> guess('Romania')
            False

        You can also force the type from column header:

            >>> guess('I was forced to be a list', label='items:list')
            True
            >>> guess('I was forced to be a list', label='countries:List')
            True

        """
        for alias in self.aliases:
            if isinstance(alias, unicode):
                alias = alias.encode('utf-8')
            if ':%s' % alias in label.lower():
                return True
        return False
