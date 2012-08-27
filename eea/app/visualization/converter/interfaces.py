""" Converter interfaces
"""
from zope.interface import Interface
from eea.app.visualization.converter.types.interfaces import IGuessType
from eea.app.visualization.converter.types.interfaces import IGuessTypes

class ITable2JsonConverter(Interface):
    """ Converts CSV to JSON
    """

__all__ = (
    IGuessType.__name__,
    IGuessTypes.__name__,
    ITable2JsonConverter.__name__,
)
