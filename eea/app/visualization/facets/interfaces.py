""" Facets interfaces
"""
from zope import schema
from zope.interface import Interface

class IVisualizationFacet(Interface):
    """ Access / update one facet configuration
    """

class IVisualizationAddFacet(Interface):
    """ Add facet
    """
    name = schema.TextLine(
        title=u'Id',
        description=(u"Facet id. Same as the key id in your JSON. "
                     "(e.g. publishDate)"))
    label = schema.TextLine(
        title=u'Friendly name',
        description=u"Label for facet (e.g. Effective Date)",
        required=False
    )
