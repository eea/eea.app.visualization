""" Visualization views configuration interfaces
"""
from zope.interface import Interface
from zope.schema import TextLine
from zope.publisher.interfaces.browser import IBrowserView

class IVisualizationView(IBrowserView):
    """ Access / update visualization view configuration
    """
    label = TextLine(title=u'Label for visualization view')

class IVisualizationViews(Interface):
    """ Utility to get available visualization views
    """
