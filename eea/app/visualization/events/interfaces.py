""" Visualization Events interfaces
"""
from zope.component.interfaces import IObjectEvent

class IVisualizationEvent(IObjectEvent):
    """ All visualization events should inherit from this class
    """

class IVisualizationEnabledEvent(IVisualizationEvent):
    """ Visualization was enabled
    """

class IVisualizationFacetDeletedEvent(IVisualizationEvent):
    """ Visualization facet deleted
    """

__all__ = [
    IVisualizationEvent,
    IVisualizationEnabledEvent,
    IVisualizationFacetDeletedEvent,
]
