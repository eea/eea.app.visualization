""" Views to get images for Visualizations
"""
from urllib2 import urlparse
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
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
        if not self._img:
            view = queryMultiAdapter((self.context, self.request),
                                 name='daviz-view.html')
            for tab in view.tabs:
                fallback = tab.get('fallback-image', None)
                if not fallback:
                    continue

                url = urlparse.urlparse(fallback)
                query = dict((k, v[0])
                             for k, v in urlparse.parse_qs(url.query).items())
                self.request.form.update(query)

                img = url.path.split('/')[-1]
                img = self.context.restrictedTraverse(img, None)

                if not img:
                    continue

                self._img = queryMultiAdapter((img, self.request),
                                              name='imgview')
                break

        return self._img

    def display(self, scalename='thumb'):
        """ display """
        if not self.img:
            return False
        return self.img.display(scalename)

    def __call__(self, scalename='thumb'):
        if self.display(scalename):
            return self.img(scalename)
        raise NotFound(self.request, scalename)

