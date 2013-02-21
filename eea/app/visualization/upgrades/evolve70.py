""" Evolve to version 7.0
"""
import logging
from zope.component import queryAdapter
from zope.component.interface import interfaceToName
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationEnabled
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger("eea.app.visualization.upgrades")

def enable_davizSettings(context):
    """ Move column label settings from facet annotations directly to daviz JSON
    """
    ctool = getToolByName(context, 'portal_catalog')
    iface = interfaceToName(context, IVisualizationEnabled)
    brains = ctool(
        object_provides=iface,
        show_inactive=True, Language='all'
    )

    logger.info('Enabling daviz.properties: %s', len(brains))
    for brain in brains:
        try:
            doc = brain.getObject()
            logger.info("Enabling daviz.properties for %s", doc.absolute_url())
            mutator = queryAdapter(doc, IVisualizationConfig)
            if not mutator.view('daviz.properties'):
                mutator.add_view('daviz.properties')
        except Exception, err:
            logger.warn("Failed to enable daviz.properties: %s", err)
