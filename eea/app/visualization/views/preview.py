""" Preview images
"""
from zope.interface import implementer
from zope.component import queryUtility
from zope.publisher.interfaces import IPublishTraverse
from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import IPropertiesTool
from eea.app.visualization.zopera import scaleImage


@implementer(IPublishTraverse)
class PreviewImage(BrowserView):
    """ Preview image
    """
    def __init__(self, context, request):
        super(PreviewImage, self).__init__(context, request)
        self._sizes = None

    @property
    def sizes(self):
        """ Allowed sizes
        """
        if self._sizes is None:
            props = queryUtility(IPropertiesTool).imaging_properties
            sizes = props.getProperty('allowed_sizes')
            self._sizes = {}
            for size in sizes:
                name, info = size.split(' ')
                w, h = info.split(':')
                self._sizes[name] = (int(w), int(h))
        return self._sizes

    def width(self, scale='thumb', default=128):
        """ Image width
        """
        width, _height = self.sizes.get(scale, (default, default))
        return width

    def height(self, scale='thumb', default=128):
        """ Image height
        """
        _width, height = self.sizes.get(scale, (default, default))
        return height

    def publishTraverse(self, request, name):
        """ Scale images
        """
        if name.startswith('image_'):
            try:
                _i, scale = name.split('_')
            # 25835 fix scales when we request the full image with
            # image_view_fullscreen because there are too many values to Unpack
            # in which case we show the entire image
            except ValueError:
                return self()
            return self(scale=scale)

    def __call__(self, **kwargs):
        img = self.context.restrictedTraverse("++resource++" + self.__name__)
        scale = kwargs.get('scale', None)
        data = img.GET()
        if not scale:
            return data

        width = kwargs.get('width', self.width(scale))
        height = kwargs.get('height', self.height(scale))
        data, _format, _dim = scaleImage(data, width=width, height=height)
        return data
