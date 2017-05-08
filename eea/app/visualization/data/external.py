""" Utilities to get data from External URL
"""
import logging
import contextlib
from eventlet.green import urllib2
from zope.interface import implements
from zope.component import queryUtility
from eea.app.visualization.interfaces import IExternalData, IInternalData
from eea.app.visualization.interfaces import IData2TableConverter
logger = logging.getLogger('eea.app.visualization')

class ExternalData(object):
    """ Utility to get visualization data from external URL

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.interfaces import IExternalData

        >>> data = getUtility(IExternalData)
        >>> data
        <eea.app.visualization.data.external.ExternalData ...>

    """
    implements(IExternalData)

    def test(self, url, timeout=15):
        """ Test to see if provided URL is a valid URL
        """
        internal = queryUtility(IInternalData)
        if internal.test(url):
            return True

        res = False
        try:
            with contextlib.closing(
                urllib2.urlopen(url, timeout=timeout)) as conn:
                headers = conn.headers
                ctype = headers.get('content-type', '').split(';')[0].strip()
                convert = queryUtility(IData2TableConverter, name=ctype)
                res = True if convert else False
        except Exception, err:
            logger.exception(err)
        return res

    def __call__(self, url, timeout=15):
        """ Get data and convert it to TSV if possible
        """
        internal = queryUtility(IInternalData)
        data = internal(url)
        if data:
            return data

        try:
            with contextlib.closing(
                urllib2.urlopen(url, timeout=timeout)) as conn:
                headers = conn.headers
                ctype = headers.get('content-type', '').split(';')[0].strip()
                convert = queryUtility(IData2TableConverter, name=ctype)
                data = convert(conn.read()) if convert else u''
        except Exception, err:
            logger.exception(err)
        return data
