""" URL utility
"""
import re

protocols = frozenset((
    'http', 'ftp', 'irc', 'news', 'imap', 'gopher', 'jabber',
    'webdav', 'smb', 'fish', 'ldap', 'pop3', 'smtp', 'sftp', 'ssh', 'feed'
))

REGEX = re.compile(r'(%s)s?://[^\s\r\n]+' % '|'.join(protocols))

class GuessURL(object):
    """
    Is provided text a valid URL::

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.converter.types.interfaces import \
        ...     IGuessType
        >>> guess = getUtility(IGuessType, 'url')
        >>> print guess('http://eea.europa.eu/data-and-maps')
        True

        >>> print guess('The url is: http://eea.europa.eu/data-and-maps')
        False

        >>> print guess('https://localhost:9923')
        True

    You can also force the type from column header::

        >>> guess('I was forced to be an URL', label='homepage:url')
        True

    """
    def __call__(self, text, label=''):
        if label and ":url" in label.lower():
            return True

        if re.match(REGEX, text):
            return True
        return False
