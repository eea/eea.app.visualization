""" Visualization Events interfaces
"""
from zope.component.interfaces import IObjectEvent

class IVisualizationEvent(IObjectEvent):
    """ All visualization events should inherit from this class
    """

class IVisualizationEnabledEvent(IVisualizationEvent):
    """ Visualization was enabled
    """

class IVisualizationDisabledEvent(IVisualizationEvent):
    """ Visualization was disabled
    """

class IVisualizationFacetDeletedEvent(IVisualizationEvent):
    """ Visualization facet deleted
    """

__all__ = [
    IVisualizationEvent.__name__,
    IVisualizationEnabledEvent.__name__,
    IVisualizationDisabledEvent.__name__,
    IVisualizationFacetDeletedEvent.__name__,
]
