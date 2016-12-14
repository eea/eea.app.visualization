""" Utilities to get data from External URL
"""
import logging
from urllib2 import urlparse
from AccessControl import Unauthorized
from AccessControl import SpecialUsers
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from zope.interface import implements
from zope.component.hooks import getSite
from eea.app.visualization.zopera import IATBlob
from eea.app.visualization.interfaces import IInternalData
logger = logging.getLogger('eea.app.visualization')

class InternalData(object):
    """ Utility to get visualization data from external URL

        >>> from zope.component import getUtility
        >>> from eea.app.visualization.interfaces import IInternalData

        >>> data = getUtility(IInternalData)
        >>> data
        <eea.app.visualization.data.internal.InternalData ...>

    """
    implements(IInternalData)


    def _data(self, view, query):
        """ Bypass security and try to call view with query kwargs
        """
        data = u''

        oldSecurityManager = getSecurityManager()
        newSecurityManager(None, SpecialUsers.system)

        try:
            data = view(**query)
        except Exception, err:
            logger.exception(err)
        setSecurityManager(oldSecurityManager)

        return data

    def test(self, url):
        """ Test to see if provided URL is a valid internal URL
        """
        if url.startswith('resolveuid/'):
            return True

        site = getSite()

        site_url = site.absolute_url()
        site_url = site_url.replace('https://', 'http://', 1)

        url = url.replace('https://', 'http://', 1)
        if url.startswith(site_url):
            return True

        return False

    def __call__(self, url, timeout=15):
        """ Get data and convert it to TSV if possible
        """
        data = u''
        if not self.test(url):
            return data

        ourl = urlparse.urlparse(url)
        query = ourl.query
        query = urlparse.parse_qs(query)
        site = getSite()
        request = getattr(site, 'REQUEST', None)
        if getattr(request, 'form', None) is not None:
            request.form.update(query)

        try:
            view = site.unrestrictedTraverse(ourl.path)
        except Exception as err:
            logger.warn("Invalid data url '%s'", url)
            return data

        if IATBlob.providedBy(view):
            query = {}
            view = view.getFile

        if getattr(view, 'meta_type', None) == 'File':
            query = {}
            oldView = view
            view = lambda: oldView.data

        try:
            try:
                data = view(**query)
            except TypeError: # got an unexpected keyword argument
                query = {}
                data = view()
        except Unauthorized:
            data = self._data(view, query)
        except Exception, err:
            logger.exception(err)

        if not isinstance(data, (str, unicode)):
            data = getattr(data, 'read', lambda: getattr(data, 'data', u''))()

        return data
