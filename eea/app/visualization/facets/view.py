""" List facets view module
"""
from zope import schema
from zope.interface import implements
from eea.app.visualization.facets.interfaces import IVisualizationFacet
from Products.Five.browser import BrowserView

class ViewForm(BrowserView):
    """ list facets BrowserView
    """
    implements(IVisualizationFacet)

    ex_template = (
        '<div ex:role="exhibit-facet" ex:facetClass="%(type)s" '
          'ex:expression=".%(name)s" ex:facetLabel="%(label)s"'
          'id="%(name)s-facet" %(extra)s></div>'
    )

    facetType = ""
    facetInterface = None

    def __init__(self, context, request):
        """ List facets BrowserView init
        """
        super(ViewForm, self).__init__(context, request)
        self._data = {}
        self._extra = ""

    @property
    def extra(self):
        """ Extra properties
        """
        if not self._extra:

            extra = []
            for name, field in schema.getFieldsInOrder(self.facetInterface):
                if not name.startswith('ex_'):
                    continue

                value = self.settings(name, field.default)
                if value is None:
                    continue

                ex_name = name.replace('ex_', 'ex:')
                extra.append('%s="%s"' % (ex_name, value))

            self._extra = " ".join(extra)
        return self._extra

    @property
    def data(self):
        """ Get facets data
        """
        return self._data

    @data.setter
    def data(self, data):
        """ Set facets data
        """
        self._data = data

    def settings(self, key, default=None):
        """ Getter facets data
        """
        return self.data.get(key, default)

    def render(self, **kwargs):
        """ Render exhibit view
        """
        options = {
            'type': self.facetType,
            'name': self.settings('name', ''),
            'label': self.settings('label', ''),
            'extra': self.extra
        }

        return self.ex_template % options

    def __call__(self, **kwargs):
        return self.render(**kwargs)
