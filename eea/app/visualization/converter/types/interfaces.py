""" Converter column types
"""
from zope.interface import Interface

class IGuessType(Interface):
    """ All named utilities for guessing csv column type should provide this
    interface.
    """

    def __call__(text, label=''):
        """ Check if the provided text is an url, date, or whatever the utility
        tries to guess.

        text -- CSV cell to guess on
        label -- CSV column header
        """
