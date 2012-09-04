""" Vocabulary logic for returning available registered visualization views
"""
from zope.component import queryAdapter
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from eea.app.visualization.interfaces import IVisualizationConfig

class FacetsVocabulary(object):
    """ Available registered visualization facets
    """
    implements(IVocabularyFactory)

    def _facets(self, context):
        """ Returns facets
        """
        accessor = queryAdapter(context, IVisualizationConfig)
        for facet in accessor.facets:
            yield facet

    def __call__(self, context=None):
        """ See IVocabularyFactory interface
        """
        return SimpleVocabulary([
            SimpleTerm(facet.get('name'),
                       facet.get('name'),
                       facet.get('label', facet.get('name')))
            for facet in self._facets(context)])

FacetsVocabularyFactory = FacetsVocabulary()
