""" No cache
"""
def ramcache(*ar, **kwargs):
    """ RAM cache
    """
    def decorator(method):
        """ Decorator
        """
        def replacement(*args, **kwargs):
            """ Replacement
            """
            return method(*args, **kwargs)
        return replacement
    return decorator


def flush(*args, **kwargs):
    """ Flush cache
    """
    return

flushRelatedItems = flush
flushBackRefs = flush
