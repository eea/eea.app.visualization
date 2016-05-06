""" Visualization config module
"""
from zope.i18nmessageid.message import MessageFactory

ANNO_VIEWS = 'eea.daviz.config.views'
ANNO_FACETS = 'eea.daviz.config.facets'
ANNO_JSON = 'eea.daviz.config.json'
ANNO_SOURCES = 'eea.daviz.config.sources'
ANNO_DATA = 'eea.daviz.config.datasource'
ANNO_MULTIDATA = 'eea.daviz.config.multidatasource'

EEAMessageFactory = MessageFactory('eea')

DATA_ANNOTATIONS = [
    '', 'n/a', 'n.a.', 'na', 'n.a',
    '.', ':', '-', '_', '/', '\\', "[]", "{}", "()", "<>", "*",
    'empty', "<empty>", 'not set', "<not set>", "notset",
    "<notset>", 'none', "<none>", "missing", "<missing>",
    'undefined', "<undefined>", "null", "<null>"
]
