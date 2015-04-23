""" Preview images
"""
from Products.Five.browser import BrowserView
from eea.app.visualization.zopera import scaleImage

class PreviewImage(BrowserView):
    """ Preview image
    """
    def __call__(self, **kwargs):
        img = self.context.restrictedTraverse("++resource++" + self.__name__)
        scale = kwargs.get('scale', None)
        data = img.GET()
        if not scale:
            return data

        width = kwargs.get('width', 128)
        height = kwargs.get('height', 128)
        data, _format, _dim = scaleImage(data, width=width, height=height)
        return data
