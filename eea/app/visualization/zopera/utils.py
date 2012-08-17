""" Provide missing utilities when used without Plone
"""
from zope.interface import implements
from eea.app.visualization.zopera import IPropertiesTool

class PropertiesTool(object):
    """ Missing properties_tool outside CMFPlone
    """
    implements(IPropertiesTool)

    def __init__(self, context=None):
        self.context = context

    def geographical_properties(self, context=None, **kwargs):
        """ Geographical properties"""
        class Properties(object):
            """ portal_properties
            """
            @property
            def google_key(self):
                """ Google key
                """
                return getattr(context, 'google_key', '')
        return Properties()
