""" Basic layer for daviz views
"""
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IVisualizationConfig

class ViewForm(BrowserView):
    """ Basic layer for daviz views. For more details on how to use this,
    see implementation in eea.exhibit.views.map.view.View.
    """
    label = ''

    def __init__(self, context, request):
        super(ViewForm, self).__init__(context, request)
        self._data = {}

    @property
    def data(self):
        """ Return saved configuration
        """
        if self._data:
            return self._data

        accessor = queryAdapter(self.context, IVisualizationConfig)
        self._data = accessor.view(self.__name__, {})
        return self._data

    @property
    def tabs(self):
        """ Tab(s) headers to be displayed in view mode
        """
        tabname = self.tabname()
        return [
            {'name': self.__name__,
             'title': self.label,
             'css': tabname,
             'tabname': tabname,
             'fallback-image': self.context.absolute_url() + \
                                "/" + self.__name__ + ".preview.png"
             },
        ]

    def tabname(self):
        """ View tab name
        """
        return 'tab-%s' % self.__name__.replace('.', '-')
