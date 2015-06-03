""" URL utility
"""
import re
from eea.app.visualization.converter.types import GuessType
protocols = frozenset((
    'http', 'ftp', 'irc', 'news', 'imap', 'gopher', 'jabber',
    'webdav', 'smb', 'fish', 'ldap', 'pop3', 'smtp', 'sftp', 'ssh', 'feed'
))

REGEX = re.compile(r'(%s)s?://[^\s\r\n]+' % '|'.join(protocols))

class GuessURL(GuessType):
    """ Utility to guess and convert text to url:

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'url')
        >>> guess
        <eea.app.visualization.converter.types.url.GuessURL object...>

    """
    order = 10
    aliases = ('url', 'link', 'hyperlink')
    valueType = u'url'

    def convert(self, text, fallback=None, **options):
        """ Convert text to url

            >>> guess.convert('http://eea.europa.eu')
            'http://eea.europa.eu'

        You can use fallback to force text to url:

            >>> guess.convert('data-and-maps',
            ...       fallback=lambda x: 'http://eea.europa.eu/' + x)
            'http://eea.europa.eu/data-and-maps'

        """
        if fallback is not None:
            if callable(fallback):
                return fallback(text)
            return fallback
        return text

    def __call__(self, text, label=''):
        """
        Is provided text a valid URL:

            >>> guess('http://eea.europa.eu/data-and-maps')
            True
            >>> guess('The url is: http://eea.europa.eu/data-and-maps')
            False
            >>> guess('https://localhost:9923')
            True

        You can also force the type from column header::

            >>> guess('I was forced to be an URL', label='homepage:url')
            True

        """
        for alias in self.aliases:
            if isinstance(alias, unicode):
                alias = alias.encode('utf-8')
            if ':%s' % alias in label.lower():
                return True

        if re.match(REGEX, text):
            return True
        return False
