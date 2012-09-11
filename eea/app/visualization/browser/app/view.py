""" Module that contains default view
"""
import logging
from zope.security import checkPermission
from zope.component import queryUtility, queryAdapter, queryMultiAdapter
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.zopera import IPropertiesTool

logger = logging.getLogger('eea.app.visualization')

class View(BrowserView):
    """ daviz-view.html
    """
    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self.accessor = queryAdapter(self.context, IVisualizationConfig)

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

    @property
    def sources(self):
        """ External sources
        """
        sources = self.accessor.sources
        for source in sources:
            yield source

    @property
    def gmapkey(self):
        """ Get Google Maps key from
            portal_properties.geographical_properties.google_key
        """
        ptool = queryUtility(IPropertiesTool)
        props = getattr(ptool, 'geographical_properties', None)
        if callable(props):
            try:
                props = props(context=self.context, request=self.request)
            except Exception, err:
                logger.debug(err)

        if getattr(props, 'getProperty', None):
            key = props.getProperty('google_key', '')
        else:
            key = getattr(props, 'google_key', '')

        return key

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
    def sections(self):
        """ Returns view sections
        """
        views = self.accessor.views

        sections = {}
        for view in views:
            name = view.get('name')
            browser = queryMultiAdapter(
                (self.context, self.request), name=name)
            section = getattr(browser, 'section', 'Default')
            section_id = section.lower().replace(' ', '-')
            sections[section_id] = section
        return sections

    def section_views(self, section):
        """ Returns views for a section
        """
        views = self.accessor.views
        myviews = []
        for view in views:
            name = view.get('name')
            browser = queryMultiAdapter(
                            (self.context, self.request), name=name)
            section_name = getattr(browser, 'section', 'Default')
            if section_name.lower().replace(' ', '-') != section:
                continue
            myviews.append(name)
        return myviews

    def section(self, name):
        """ Get section by name
        """
        view = queryMultiAdapter((self.context, self.request), name=name)
        if not view:
            logger.warn('There is no %s view registered for %s',
                        name, self.context.absolute_url(1))
            return ''
        return view()

    def __call__(self, **kwargs):
        """ If daviz is not configured redirects to edit page.
        """
        if not checkPermission('eea.app.visualization.configure', self.context):
            return self.index()

        referer = getattr(self.request, 'HTTP_REFERER', '')
        if not (referer.endswith('/edit') or referer.endswith('/atct_edit')):
            return self.index()

        return self.request.response.redirect(
            self.context.absolute_url() + '/daviz-edit.html')
