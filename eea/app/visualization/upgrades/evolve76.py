"""update long column names
"""
import logging
from eea.app.visualization.converter.interfaces import ITable2JsonConverter
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName

from zope.annotation.interfaces import IAnnotations

from eea.app.visualization.config import (
    ANNO_VIEWS, ANNO_FACETS, ANNO_JSON
)
from persistent.dict import PersistentDict
from persistent.list import PersistentList


logger = logging.getLogger("eea.app.visualization.upgrades")

def replace_values(obj, orig, new):
    """ replace all occurences of column name
    """
    if isinstance(obj, PersistentList) or isinstance(obj, list):
        if isinstance(obj, PersistentList):
            new_obj = PersistentList()
        else:
            new_obj = []
        for item in obj:
            new_item = replace_values(item, orig, new)
            new_obj.append(new_item)
        return new_obj

    if isinstance(obj, PersistentDict) or isinstance(obj, dict):
        if isinstance(obj, PersistentDict):
            new_obj = PersistentDict()
        else:
            new_obj = {}
        for key in obj.keys():
            new_value = replace_values(obj[key], orig, new)
            new_key = replace_values(key, orig, new)
            new_obj[new_key] = new_value
        return new_obj

    if isinstance(obj, basestring):
        new_obj = obj.replace(orig, new)
        return new_obj

    return obj

def fix_long_column_labels(context):
    """ Fix long column labels
    """
    converter = queryUtility(ITable2JsonConverter)
    normalizer = queryUtility(IIDNormalizer)

    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool(object_provides=('eea.app.visualization.subtypes.interfaces.'
                                    'IVisualizationEnabled'))

    logger.info('Updating long column labels')
    for brain in brains:
        obj = brain.getObject()
        try:
            obj_json = converter(obj.spreadsheet)
        except Exception:
            continue

        for key in obj_json[1]['properties'].keys():
            obj_label = obj_json[1]['properties'][key]['label']
            key1 = normalizer.normalize(obj_label)
            key1 = key1.replace("-", "_")
            key2 = normalizer.normalize(obj_label, max_length=255)
            key2 = key2.replace("-", "_")
            if key1 != key2:
                logger.info("fixing: "+brain.getURL())
                logger.info(key1 + "   -   " + key2)
                org_views = IAnnotations(obj).get(ANNO_VIEWS, {})
                org_facets = IAnnotations(obj).get(ANNO_FACETS, {})
                org_json = IAnnotations(obj).get(ANNO_JSON, {})
                IAnnotations(obj)[ANNO_VIEWS] = \
                    replace_values(org_views, key1, key2)
                IAnnotations(obj)[ANNO_FACETS] = \
                    replace_values(org_facets, key1, key2)
                IAnnotations(obj)[ANNO_JSON] = \
                    replace_values(org_json, key1, key2)

    logger.info("done")

