""" Tiles view module
"""
from zope.interface import implements
from eea.app.visualization.views.view import ViewForm
from eea.app.visualization.views.data.interfaces import IDataView

class View(ViewForm):
    """ Tile view
    """
    label = 'Data settings'
    implements(IDataView)

    @property
    def tabs(self):
        """ Tab(s) headers to be displayed in view mode
        """
        return []
