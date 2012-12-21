""" Vocabulary logic for returning available registered visualization views
"""
from zope.component import queryAdapter
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from eea.app.visualization.interfaces import IVisualizationConfig

def compare(a, b):
    """ Compare
    """
    order_a = a[1].get('order', -1)
    order_b = b[1].get('order', -1)
    return cmp(order_a, order_b)

class FacetsVocabulary(object):
    """ Available registered visualization facets
    """
    implements(IVocabularyFactory)

    def _facets(self, context):
        """ Returns facets
        """
        accessor = queryAdapter(context, IVisualizationConfig)
        properties = accessor.json.get('properties', {}).items()
        properties.sort(cmp=compare)

        for name, facet in properties:
            yield (name, facet.get('label', name))

    def __call__(self, context=None):
        """ See IVocabularyFactory interface
        """
        return SimpleVocabulary([SimpleTerm(name, name, label)
            for name, label in self._facets(context)])
