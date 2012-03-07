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

    can_enable = schema.Bool(u'Can enable exhibit view',
                             readonly=True)
    can_disable = schema.Bool(u'Can disable disable exhibit view',
                              readonly=True)
    is_exhibit = schema.Bool(u'Is current object exhibit enabled',
                             readonly=True)

    def enable():
        """ Enable exhibit view
        """

    def disable():
        """ Disable exhibit view
        """

__all__ = [
    IAnnotations,
    AttributeAnnotations
]
