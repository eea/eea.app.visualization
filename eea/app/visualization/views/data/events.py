""" Handle events
"""
import logging
from zope.component import queryAdapter
from eea.app.visualization.interfaces import IVisualizationConfig
logger = logging.getLogger('eea.app.visualization')

def create_default_views(obj, evt):
    """ Create default views
    """
    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        logger.warn("Couldn't find any IVisualizationConfig adapter for %s",
                    obj.absolute_url(1))
        return

    if not mutator.view('daviz.properties'):
        mutator.add_view('daviz.properties')
