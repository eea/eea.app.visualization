""" Custom meta-directives DaViz Views
"""
from zope.interface import implements, Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.app.visualization.interfaces import IVisualizationFacets
from Products.Five.browser.metaconfigure import page

class VisualizationFacets(object):
    """ Registry for daviz facets views registered via ZCML
    """
    implements(IVisualizationFacets)
    _views = {}
    _edits = {}

    @property
    def views(self):
        """ Views
        """
        return self._views

    @property
    def edits(self):
        """ Edits
        """
        return self._edits

    def keys(self):
        """ Views names
        """
        return self.views.keys()

    def edit_keys(self):
        """ Edits names
        """
        return self.edits.keys()

    def label(self, key):
        """ View label or key
        """
        return self.views.get(key, key)

    def edit_label(self, key):
        """ Edit label or key
        """
        return self.edits.get(key, key)

    def __call__(self, mode='view'):
        if mode != 'view':
            return self.edit_keys()
        return self.keys()

def ViewDirective(_context, name, permission=None, for_=Interface,
                  layer=IDefaultBrowserLayer, template=None, class_=None,
                  allowed_interface=None, allowed_attributes=None,
                  attribute='__call__', menu=None, title=None):
    """ Daviz View Facet
    """
    if not name:
        raise TypeError("No name provided")

    label = title
    if title and not menu:
        title = None

    page(_context=_context, name=name, permission=permission,
         for_=for_, layer=layer, template=template, class_=class_,
         allowed_interface=allowed_interface,
         allowed_attributes=allowed_attributes,
         attribute=attribute, menu=menu, title=title)

    VisualizationFacets._views[name] = label or name

def EditDirective(_context, name, permission=None, for_=Interface,
                  layer=IDefaultBrowserLayer, template=None, class_=None,
                  allowed_interface=None, allowed_attributes=None,
                  attribute='__call__', menu=None, title=None):
    """ Daviz Edit Facet
    """
    if not name:
        raise TypeError("No name provided")

    label = title
    if title and not menu:
        title = None

    if not name.endswith('.edit'):
        name += u'.edit'

    page(_context=_context, name=name, permission=permission,
         for_=for_, layer=layer, template=template, class_=class_,
         allowed_interface=allowed_interface,
         allowed_attributes=allowed_attributes,
         attribute=attribute, menu=menu, title=title)

    VisualizationFacets._edits[name] = label or name
