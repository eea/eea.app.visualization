""" Number utility
"""
import re
from eea.app.visualization.converter.types import GuessType

REGEX = re.compile(r'[0-9]*(\,|\.)?[0-9]+$')

class GuessNumber(GuessType):
    """ Utility to guess and convert text to number:

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'number')
        >>> guess
        <eea.app.visualization.converter.types.number.GuessNumber...>

    """
    order = 70
    priority = 1
    aliases = ('number', 'num', 'nr', 'int', 'integer', 'float', 'decimal')
    valueType = u'number'


    def convert(self, text, fallback=None, **options):
        """
        Convert text to number

            >>> guess.convert('  2011   ')
            2011
            >>> print guess.convert('.35')
            0.35
            >>> print guess.convert('2.3')
            2.3
            >>> print guess.convert('2,3')
            2.3

        You can use fallback to force text to number:

            >>> guess.convert('2.3.4', fallback=0)
            0
            >>> guess.convert('2.3.4',
            ...       fallback=lambda x: int(x.replace('.', '')))
            234

        If you don't provide a fallback for a wrong value, a ValueError will be
        raised:

            >>> guess.convert('A number: 23.45')
            Traceback (most recent call last):
            ...
            ValueError: A number: 23.45

        You can also convert given text to another text providing 'format'
        keyword:

            >>> guess.convert('2.3', format='%d')
            '2'
            >>> guess.convert('2.3', format='%.2f')
            '2.30'

        """
        if ',' in text:
            text = text.replace(',', '.')

        error = False
        if '.' in text:
            try:
                text = float(text)
            except Exception:
                error = True
        else:
            try:
                text = int(text)
            except Exception:
                error = True

        if error:
            if fallback is not None:
                if callable(fallback):
                    text = fallback(text)
                else:
                    text = fallback
            else:
                raise ValueError(text)

        if not isinstance(text, (int, float)):
            return text

        strformat = options.get('format', None)
        if not strformat:
            return text

        return strformat % text

    def __call__(self, text, label=''):
        """
        Is provided text a Number:

            >>> guess('0')
            True
            >>> guess('2')
            True
            >>> guess('.56')
            True
            >>> guess('2.0')
            True
            >>> guess(' 234.3423423   ')
            True
            >>> guess('23,456')
            True

            >>> guess('')
            False
            >>> guess('23.45.6')
            False
            >>> guess('23 45')
            False
            >>> guess('A number: 23.45')
            False

        You can also force the type from column header:

            >>> guess('I was forced to be a Number', label='exists:int')
            True
            >>> guess('I was forced to be a Number', label='exists:Integer')
            True
            >>> guess('I was forced to be a Number', label='exists:Number')
            True

        """
        for alias in self.aliases:
            if isinstance(alias, unicode):
                alias = alias.encode('utf-8')
            if ':%s' % alias in label.lower():
                return True

        text = text.strip()
        if re.match(REGEX, text):
            return True
        return False
