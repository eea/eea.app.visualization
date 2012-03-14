""" Converter column types
"""
from zope.interface import Interface

class IGuessType(Interface):
    """ All named utilities for guessing CSV column type should provide this
    interface.
    """
    def convert(text, fallback=None, **options):
        """ Convert provided text to boolean, number or whatever the utility is
        about.

        text     -- CSV cell content
        fallback -- If the provided text can not be converted, fallback on this
                    value. Default no fallback, returns provided text.
        options  -- Utility specific options, like date format, float number of
                    decimals, etc
        """

    def __call__(text, label=''):
        """ Check if the provided text is an url, date, or whatever the utility
        tries to guess.

        text  -- CSV cell to guess on
        label -- CSV column header
        """

class IGuessTypes(Interface):
    """ Guess CSV column types
    """
    def __call__(datatable):
        """ Guess column types for given CSV datatable.
        Returns a mapping between column names and types.

        datatable -- CSV datatable (list of rows)
        """
