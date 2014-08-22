""" Caching module
"""
try:
    from eea.cache import cache as eeacache
    from eea.cache import event
    InvalidateCacheEvent = event.InvalidateCacheEvent
    flush = event.flush
    flushBackRefs = event.flushBackRefs
    flushRelatedItems = event.flushRelatedItems
    ramcache = eeacache
except ImportError:
    # Fail quiet if required cache packages are not installed in order to use
    # this package without caching
    from eea.app.visualization.cache.nocache import ramcache
    from eea.app.visualization.cache.nocache import flush
    from eea.app.visualization.cache.nocache import flushBackRefs
    from eea.app.visualization.cache.nocache import flushRelatedItems
    from eea.app.visualization.cache.nocache import InvalidateCacheEvent

from eea.app.visualization.cache.cache import cacheJsonKey

__all__ = [
    ramcache.__name__,
    InvalidateCacheEvent.__name__,
    cacheJsonKey.__name__,
    flush.__name__,
    flushBackRefs.__name__,
    flushRelatedItems.__name__
]
