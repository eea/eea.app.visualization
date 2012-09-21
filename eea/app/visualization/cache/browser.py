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
            'eea.app.visualization.data.browser.json:%s:%s',
            'eea.daviz.data.browser.json:%s:%s',
        ))

        names = frozenset((
            'daviz.json',
        ))

        items = set([self.context])
        getRelatedItems = getattr(self.context, 'getRelatedItems', None)
        if getRelatedItems:
            items.update(getRelatedItems())

        for key in keys:
            for name in names:
                for item in items:
                    xkey = key % (item.absolute_url(1), name)
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
