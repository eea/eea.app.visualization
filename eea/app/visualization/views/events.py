""" Views events
"""
import logging
from zope.component import queryAdapter
from eea.app.visualization.interfaces import IVisualizationConfig
logger = logging.getLogger('eea.app.visualization.views.events')

def create_default_views(obj, evt):
    """ Create default views
    """
    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        logger.warn("Couldn't find any IVisualizationConfig adapter for %s",
                    obj.absolute_url(1))
        return

    if evt.cleanup:
        # Remove all views
        mutator.delete_views()


def facet_deleted(obj, evt, daviz_view):
    """ Cleanup removed facet from view properties
    """
    facet = evt.facet
    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        logger.warn("Couldn't find any IVisualizationConfig adapter for %s",
                    obj.absolute_url(1))
        return

    view = mutator.view(daviz_view)
    if not view:
        return

    changed = False
    properties = dict(view)
    for key, value in properties.items():
        if isinstance(value, (unicode, str)):
            if value == facet:
                properties.pop(key)
                changed = True
        elif isinstance(value, (list, tuple)):
            if facet in value:
                value = list(item for item in value if item != facet)
                properties[key] = value
                changed = True

    if changed:
        mutator.edit_view(daviz_view, **properties)
