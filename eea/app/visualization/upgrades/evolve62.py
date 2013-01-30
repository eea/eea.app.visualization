""" Evolve to version 6.2
"""
import logging
from zope.component import queryAdapter, queryUtility
from zope.component.interface import interfaceToName
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationEnabled
from eea.app.visualization.interfaces import IDavizSettings
from eea.app.visualization.config import DATA_ANNOTATIONS
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger("eea.app.visualization.upgrades")

def fix_column_labels(context):
    """ Move column label settings from facet annotations directly to daviz JSON
    """
    ctool = getToolByName(context, 'portal_catalog')
    iface = interfaceToName(context, IVisualizationEnabled)
    brains = ctool(
        object_provides=iface,
        show_inactive=True, Language='all'
    )

    logger.info('Fixing daviz column labels: %s', len(brains))
    for brain in brains:
        try:
            doc = brain.getObject()
            mutator = queryAdapter(doc, IVisualizationConfig)
            data = mutator.json
            properties = data.get('properties', {})
            facets = mutator.facets
            logger.info("Fixing column labels for %s", doc.absolute_url())
            for facet in facets:
                name = facet.get('name')
                label = facet.get('label', name)
                if isinstance(label, str):
                    label = label.decode('utf-8')
                config = properties.get(name, {})
                config.setdefault('label', label)
                if isinstance(config['label'], str):
                    config['label'] = config['label'].decode('utf-8')
            mutator.json = data
        except Exception:
            logger.info("Failed to fix")

def update_davizSettings(context):
    """ Add data settings to daviz settings
    """
    logger.info('Adding daviz data settings...')
    tool = queryUtility(IDavizSettings)
    if not tool:
        logger.info('Adding daviz data settings... Nothing to do')
        return

    if tool.settings.get('data.annotations'):
        logger.info('Adding daviz data settings... Nothing to do')
        return

    tool.settings['data.annotations'] = u"\n".join(DATA_ANNOTATIONS)
    logger.info('Adding daviz data settings... DONE')
