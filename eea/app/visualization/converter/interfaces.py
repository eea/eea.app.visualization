""" Converter interfaces
"""
from zope.interface import Interface
from eea.app.visualization.converter.types.interfaces import IGuessType
from eea.app.visualization.converter.types.interfaces import IGuessTypes

class ITable2JsonConverter(Interface):
    """ Converts CSV to JSON
    """

# BBB: This will be removed in the next version of this package
IExhibitJsonConverter = ITable2JsonConverter

__all__ = (
    IGuessType.__name__,
    IGuessTypes.__name__,
    ITable2JsonConverter.__name__,
)
