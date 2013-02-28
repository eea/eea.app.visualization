""" Facets interfaces
"""
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from eea.app.visualization.config import EEAMessageFactory as _

class IVisualizationFacets(Interface):
    """ Utility to get available visualization facets
    """

class IVisualizationFacet(IBrowserView):
    """ Access one facet configuration
    """
    def settings(key, default):
        """ Get settings for this facet by key
        """

class IVisualizationAddFacet(Interface):
    """ Add facet
    """
    name = schema.TextLine(
        title=_(u'Id'),
        description=_(u"Facet id. Same as the key id in your JSON. "
                      "(e.g. publishDate)"))

    label = schema.TextLine(
        title=_(u'Friendly name'),
        description=_(u"Label for facet (e.g. Effective Date)"),
        required=False
    )

    type = schema.Choice(
        title=_(u"Facet type"),
        description=_('Exhibit facet type'),
        default=u'daviz.list.facet',
        required=True,
        vocabulary=u"eea.daviz.vocabularies.FacetTypesVocabulary"
    )

class IVisualizationEditFacet(Interface):
    """ Edit facet
    """
    label = schema.TextLine(
        title=_(u'Friendly name'),
        description=_(u'Label for exhibit facet')
    )

    show = schema.Bool(
        title=_(u'Visible'),
        description=_(u'Is this facet visible?'),
        required=False
    )

    type = schema.Choice(
        title=_(u"Facet type"),
        description=_('Exhibit facet type'),
        default=u'daviz.list.facet',
        required=True,
        vocabulary=u"eea.daviz.vocabularies.FacetTypesVocabulary"
    )
