""" Visualization/events init module with VisualizationEnabledEvent class
"""
from zope.interface import implements
from eea.app.visualization.events.interfaces import (
    IVisualizationEnabledEvent,
    IVisualizationDisabledEvent,
    IVisualizationFacetDeletedEvent,
)

class VisualizationEnabledEvent(object):
    """ Visualization was enabled
    """
    implements(IVisualizationEnabledEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.columns = kwargs.get('columns', [])
        self.cleanup = kwargs.get('cleanup', True)

class VisualizationDisabledEvent(object):
    """ Visualization was disabled
    """
    implements(IVisualizationDisabledEvent)

    def __init__(self, context, **kwargs):
        self.object = context

class VisualizationFacetDeletedEvent(object):
    """ Sent if a visualization facet was deleted
    """
    implements(IVisualizationFacetDeletedEvent)

    def __init__(self, context, **kwargs):
        self.object = context
        self.facet = kwargs.get('facet', '')
