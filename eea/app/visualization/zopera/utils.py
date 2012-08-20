""" Provide missing utilities when used without Plone
"""
from zope.interface import implements
from eea.app.visualization.zopera import IPropertiesTool

class Properties(object):
    """ portal_properties
    """
    def __init__(self, context=None):
        self.context = context

    def getProperty(self, name, default=None):
        """ Get property
        """
        return getattr(self.context, name, default)

    def __getattr__(self, name, default):
        return self.getProperty(name, default)

class PropertiesTool(object):
    """ Missing properties_tool outside CMFPlone
    """
    implements(IPropertiesTool)

    def geographical_properties(self, context=None, **kwargs):
        """ Geographical properties
        """
        return Properties(context)

    def site_properties(self, context=None, **kwargs):
        """ Site properties
        """
        return Properties(context)
