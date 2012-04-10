""" Browser
"""
import hashlib
from zope import event
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView
from eea.app.visualization.cache import InvalidateCacheEvent

class InvalidateMemCache(BrowserView):
    """ Utils view to invalidate eea.daviz cache
    """
    def __call__(self, **kwargs):
        keys = frozenset((
            'eea.app.visualization.converter.browser.json:%s:%s',
            'eea.app.visualization.browser.app.view.json:%s:%s'
        ))

        names = frozenset((
            'daviz-relateditems.json',
            'daviz-view.json'
        ))

        for key in keys:
            for name in names:
                xkey = key % (self.context.absolute_url(1), name)
                xkey = hashlib.md5(xkey).hexdigest()
                event.notify(InvalidateCacheEvent(key=xkey, raw=True))
        return "Memcache invalidated"

def purgeOnModified(obj, evt):
    """ Purge memcache on modify
    """
    request = getattr(obj, 'REQUEST', None)
    if not request:
        return

    invalidate = queryMultiAdapter((obj, request), name=u'memcache.invalidate')
    if not invalidate:
        return

    invalidate()
