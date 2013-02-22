""" Handle events
"""
import logging
from zope.component import queryAdapter, queryUtility
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IDavizSettings
logger = logging.getLogger('eea.app.visualization')

def create_default_views(obj, evt):
    """ Create default views
    """
    settings = queryUtility(IDavizSettings)
    if settings and settings.disabled('daviz.properties', obj):
        return

    mutator = queryAdapter(obj, IVisualizationConfig)
    if not mutator:
        logger.warn("Couldn't find any IVisualizationConfig adapter for %s",
                    obj.absolute_url(1))
        return

    if not mutator.view('daviz.properties'):
        mutator.add_view('daviz.properties')
