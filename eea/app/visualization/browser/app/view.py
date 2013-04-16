""" Module that contains default view
"""
import logging
from zope.component import getAllUtilitiesRegisteredFor
from zope.security import checkPermission
from zope.component import queryAdapter, queryMultiAdapter
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationViewHeader

logger = logging.getLogger('eea.app.visualization')

class View(BrowserView):
    """ daviz-view.html
    """
    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self._accessor = None

    @property
    def accessor(self):
        """ Get config
        """
        if not self._accessor:
            self._accessor = queryAdapter(self.context, IVisualizationConfig)
        return self._accessor

    @property
    def facets(self):
        """ Returns facets
        """
        facets = self.accessor.facets
        for facet in facets:
            if not facet.get('show', False):
                continue
            yield facet.get('name')

    @property
    def views(self):
        """ Returns views
        """
        views = self.accessor.views
        for view in views:
            yield view.get('name')

    def get_facet(self, name):
        """ Get faceted by name
        """
        facet = self.accessor.facet(key=name)
        facet_type = facet.get('type')
        if not isinstance(facet_type, unicode):
            facet_type = facet_type.decode('utf-8')
        view = queryMultiAdapter((self.context, self.request), name=facet_type)
        view.data = facet
        return view

    def get_view(self, name):
        """ Get view by name
        """
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        view = queryMultiAdapter((self.context, self.request), name=name)
        return view

    @property
    def tabs(self):
        """ Return view tab headers
        """
        views = self.accessor.views
        tabs = []
        for view in views:
            name = view.get('name')
            browser = queryMultiAdapter(
                (self.context, self.request), name=name)
            tabs.extend(getattr(browser, 'tabs', []))
        return tabs

    @property
    def headers(self):
        """ Custom HTML to insert within head.
        """
        headers = getAllUtilitiesRegisteredFor(IVisualizationViewHeader)
        for header in headers:
            yield header(self.context, self.request)

    def __call__(self, **kwargs):
        """ If daviz is not configured redirects to edit page.
        """
        if not checkPermission('eea.app.visualization.configure', self.context):
            return self.index()

        referer = getattr(self.request, 'HTTP_REFERER', '')
        if '/portal_factory/' not in referer:
            return self.index()

        return self.request.response.redirect(
            self.context.absolute_url() + '/daviz-edit.html')
