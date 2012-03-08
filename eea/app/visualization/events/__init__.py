""" Visualization/events init module with VisualizationEnabledEvent class
"""
from zope.interface import implements
from eea.app.visualization.events.interfaces import (
    IVisualizationEnabledEvent,
    IVisualizationFacetDeletedEvent,
)

class VisualizationEnabledEvent(object):
    """ Sent if a document was converted to exhibit json
    """
    implements(IVisualizationEnabledEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.columns = kwargs.get('columns', [])
        self.cleanup = kwargs.get('cleanup', True)

class VisualizationFacetDeletedEvent(object):
    """ Sent if a visualization facet was deleted
    """
    implements(IVisualizationFacetDeletedEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.facet = kwargs.get('facet', '')
