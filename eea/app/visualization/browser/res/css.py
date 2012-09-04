""" CSS
"""
from App.Common import rfc1123_date
from DateTime import DateTime
from zope.component import getMultiAdapter, getAllUtilitiesRegisteredFor
from zope.publisher.browser import TestRequest
from eea.app.visualization.zopera import getToolByName
from eea.app.visualization.zopera import packer
from eea.app.visualization.interfaces import IVisualizationViewResources
from eea.app.visualization.interfaces import IVisualizationEditResources

class CSS(object):
    """ Handle criteria
    """
    def __init__(self, context, request, resources=()):
        self.context = context
        self.request = request
        self._resources = resources
        self.duration = 3600*24*365
        self.debug = False

        self.csstool = getToolByName(context, 'portal_css', None)
        if self.csstool:
            self.debug = self.csstool.getDebugMode()

    @property
    def resources(self):
        """ Return resources
        """
        return self._resources

    def get_resource(self, resource):
        """ Get resource content
        """
        # If resources are retrieved via GET, the request headers
        # are used for caching AND are mangled.
        # That can result in getting 304 responses
        # There is no API to extract the data from the view without
        # mangling the headers, so we must use a fake request
        # that can be modified without harm
        if resource.startswith('++resource++'):
            traverser = getMultiAdapter((self.context, TestRequest()),
                name='resource')
            obj = traverser.traverse(resource[12:], None)
        else:
            obj = self.context.restrictedTraverse(resource, None)
        if not obj:
            return '/* ERROR */'
        try:
            content = obj.GET()
        except AttributeError, err:
            return str(obj)
        except Exception, err:
            return '/* ERROR: %s */' % err
        else:
            return content

    def get_content(self, **kwargs):
        """ Get content
        """
        output = []
        for resource in self.resources:
            content = self.get_resource(resource)
            header = '\n/* - %s - */\n' % resource
            if not self.debug:
                content = packer.CSSPacker('safe').pack(content)
            output.append(header + content)
        return '\n'.join(output)

    @property
    def helper_css(self):
        """ Helper css
        """
        return []

class ViewCSS(CSS):
    """ CSS libs used in view mode
    """
    @property
    def css_libs(self):
        """ CSS libs
        """
        res = []
        for util in getAllUtilitiesRegisteredFor(IVisualizationViewResources):
            res.extend(util.css)
        return res

    @property
    def resources(self):
        """ Return view resources
        """
        res = self.helper_css
        res.extend(self.css_libs)
        return res

    def __call__(self, *args, **kwargs):
        """ view.css
        """
        self.request.RESPONSE.setHeader('content-type', 'text/css')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Cache-Control',
                                        'max-age=%d' % self.duration)
        return self.get_content()

class ViewRequiresCSS(ViewCSS):
    """ CSS libraries required by daviz-view.css
    """
    @property
    def css_libs(self):
        """ CSS libs
        """
        res = []
        for util in getAllUtilitiesRegisteredFor(IVisualizationViewResources):
            res.extend(util.extcss)
        return res

class EditCSS(CSS):
    """ CSS libs used in edit form
    """
    @property
    def css_libs(self):
        """ CSS Libs
        """
        res = []
        for util in getAllUtilitiesRegisteredFor(IVisualizationEditResources):
            res.extend(util.css)
        return res

    @property
    def resources(self):
        """ Return edit resources
        """
        res = self.helper_css
        res.extend(self.css_libs)
        return res

    def __call__(self, *args, **kwargs):
        """ edit.css
        """
        self.request.RESPONSE.setHeader('content-type', 'text/css')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Cache-Control',
                                        'max-age=%d' % self.duration)
        return self.get_content()

class EditRequiresCSS(EditCSS):
    """ CSS libraries required by daviz-edit.css
    """
    @property
    def css_libs(self):
        """ CSS Libs
        """
        res = []
        for util in getAllUtilitiesRegisteredFor(IVisualizationEditResources):
            res.extend(util.extcss)
        return res
