""" Layout upgrades
"""
import logging
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from eea.app.visualization.interfaces import IVisualizationEnabled
from eea.app.visualization.interfaces import IPossibleVisualization
from zope.component.interface import interfaceToName
logger = logging.getLogger("eea.app.visualization.upgrades")

def fix_layout(context):
    """ Fix layout for old style IVisualizationEnabled objects
    """
    ctool = getToolByName(context, 'portal_catalog')
    # Fix broken brains
    iface = interfaceToName(context, IPossibleVisualization)
    brains = ctool(
        portal_type=['File', 'DataFile', 'EEAFigureFile'],
        object_provides=iface,
        show_inactive=True, Language='all'
    )
    logger.info('Fixing daviz broken brains: %s', len(brains))
    for brain in brains:
        doc = brain.getObject()
        if not doc:
            continue
        support = queryMultiAdapter(
            (doc, context.REQUEST), name='daviz_support')
        if support.is_visualization:
            doc.reindexObject(['object_provides', ])

    # Fix daviz layouts
    iface = interfaceToName(context, IVisualizationEnabled)
    brains = ctool(
        object_provides=iface,
        show_inactive=True, Language='all'
    )
    logger.info('Fixing daviz layouts: %s', len(brains))
    for brain in brains:
        doc = brain.getObject()
        layout = doc.getLayout()
        if not layout.startswith('daviz-view.html'):
            logger.info("Fixing layout for %s", doc.absolute_url())
            doc.setLayout('daviz-view.html')
