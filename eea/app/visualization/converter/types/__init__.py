""" Column types utilities
"""
from zope.interface import implements
from eea.app.visualization.converter.types.interfaces import IGuessType

class GuessType(object):
    """ Base class to inherit from your IGuessType utility

    order -- This attribute is used to order utilities while trying to
             autodetect CSV column type. Use this if you want for example to
             apply date utility before number one, and so on.
    """
    implements(IGuessType)

    order = 100
    priority = 0
    aliases = ()
    valueType = u'text'
    fmt = None
