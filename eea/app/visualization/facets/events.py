""" Facets events module
"""
import logging
from zope.component import queryAdapter
from eea.app.visualization.interfaces import IVisualizationConfig
logger = logging.getLogger('eea.app.visualization.facets.events')

def create_default_facets(obj, evt):
    """ Create default facets
    """
    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        logger.warn("Couldn't find any IVisualizationConfig adapter for %s",
                    obj.absolute_url(1))
        return

    if evt.cleanup:
        # Remove all facets
        mutator.delete_facets()

    # Add new facets or edit existing
    for facet, typo in evt.columns:
        if not mutator.facet(facet):
            show = ('label' not in facet) or ('id' not in facet)
            mutator.add_facet(
                name=facet, label=facet, show=show, item_type=typo)
        else:
            mutator.edit_facet(facet, item_type=typo)
