""" Visualization views configuration interfaces
"""
from zope.interface import Interface
from zope.schema import TextLine
from zope.publisher.interfaces.browser import IBrowserView

from eea.app.visualization.config import EEAMessageFactory as _

class IVisualizationView(IBrowserView):
    """ Access / update visualization view configuration
    """
    label = TextLine(title=_(u'Label for visualization view'))

class IVisualizationViews(Interface):
    """ Utility to get available visualization views
    """
