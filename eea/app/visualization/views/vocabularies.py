""" Vocabularies for views
"""
import operator
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from eea.app.visualization.views.interfaces import IVisualizationViews

class ViewsVocabulary(object):
    """ Available registered visualization views
    """
    implements(IVocabularyFactory)

    def _adapters(self, context):
        """ Return adapters
        """
        views = getUtility(IVisualizationViews)
        for key, label in views.views.items():
            yield key, label

    def __call__(self, context=None):
        """ See IVocabularyFactory interface

        views = [
          (u'daviz.map', 'Map View'),
          (u'daviz.timeline', 'Timeline View'),
          (u'daviz.tile', 'Tile View'),
          (u'daviz.tabular', 'Tabular View')
        ]
        """
        views = [(name, label) for name, label in self._adapters(context)]
        views.sort(key=operator.itemgetter(1))
        views = [SimpleTerm(key, key, val) for key, val in views]
        return SimpleVocabulary(views)

ViewsVocabularyFactory = ViewsVocabulary()
