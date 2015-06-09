""" Views to get images for Visualizations
"""
# pylint: disable = E1102
from urllib2 import urlparse
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from eea.app.visualization.views.preview import PreviewImage
from eea.depiction.browser.interfaces import IImageView

class ImageView(BrowserView):
    """ Get cover image from
    """
    implements(IImageView)

    def __init__(self, context, request):
        super(ImageView, self).__init__(context, request)
        self._img = None

    @property
    def img(self):
        """ Image
        """
        if self._img:
            return self._img

        objectIds = getattr(self.context, 'objectIds', lambda: [])
        if 'cover.png' in objectIds():
            self._img = self.context.restrictedTraverse('cover.png')
            return self._img

        view = queryMultiAdapter((self.context, self.request),
                                 name='daviz-view.html')

        for tab in view.tabs:
            fallback = tab.get('fallback-image', None)
            if not fallback:
                continue

            url = urlparse.urlparse(fallback)
            query = urlparse.parse_qs(url.query)

            img = url.path.split('/')[-1]
            if isinstance(img, unicode):
                img = img.encode('utf-8')

            if img.startswith('embed-chart.svg'):
                img = query['chart'][0] + '.svg'

            img = self.context.restrictedTraverse(img, None)
            if not img:
                continue

            self._img = img
            break

        return self._img

    def display(self, scalename='thumb'):
        """ Display
        """
        if self.img and scalename:
            return True
        return False

    def __call__(self, scalename='thumb', **kwargs):
        if not self.display(scalename):
            raise NotFound(self.request, scalename)

        if isinstance(self.img, PreviewImage):
            return self.img(scale=scalename)

        imgview = queryMultiAdapter((self.img, self.request), name='imgview')
        if imgview:
            return imgview(scalename)
