""" Caching
"""
def cacheJsonKey(method, self, *args, **kwargs):
    """ Generate unique cache id
    """
    name = getattr(self, '__name__', '')
    return ':'.join((self.context.absolute_url(1), name))


class InvalidateCacheEvent(object):
    """ his event will be raised if there is no cache support
    """
