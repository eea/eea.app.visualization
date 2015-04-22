""" Preview images
"""
from Products.Five.browser import BrowserView

class PreviewImage(BrowserView):
    """ Preview image
    """
    def __call__(self, **kwargs):
        img = self.context.restrictedTraverse("++resource++" + self.__name__)
        return img.GET()
