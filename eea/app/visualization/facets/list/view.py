""" Numeric facets view module
"""
from eea.app.visualization.facets.view import ViewForm
from eea.app.visualization.facets.list.interfaces import IListProperties

class View(ViewForm):
    """ View
    """
    facetType = u"List"
    facetInterface = IListProperties
