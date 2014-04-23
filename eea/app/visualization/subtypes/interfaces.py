""" Subtyping interfaces
"""
from zope.annotation.interfaces import IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope import schema
from zope.interface import Interface

class IPossibleVisualization(Interface):
    """ Objects which can enable Visualization.
    """

class IVisualizationEnabled(Interface):
    """ Objects which have Visualization enabled
    """

class IVisualizationSubtyper(Interface):
    """ Support for subtyping objects
    """

    can_enable = schema.Bool(
        u'Can enable visualization',
        readonly=True)
    can_disable = schema.Bool(
        u'Can disable visualization',
        readonly=True)
    can_edit = schema.Bool(
        u'Can edit visualization',
        readonly=True)
    is_visualization = schema.Bool(
        u'Is visualization enabled for current object',
        readonly=True)

    def enable():
        """ Enable visualization
        """

    def disable():
        """ Disable visualization
        """

__all__ = [
    IAnnotations.__name__,
    AttributeAnnotations.__name__
]
