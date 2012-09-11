""" Visualization Data Interfaces
"""
from zope.interface import Interface
from zope import schema

class IVisualizationData(Interface):
    """ Visualization Data Adapter.
    """
    data = schema.Text(
            title=u'Data',
            description=u'Data to be converted to JSON',
            readonly=True
        )

class IVisualizationJson(Interface):
    """ Visualization data JSON (daviz-view.json)
    """
    json = schema.Text(
        title=u'JSON',
        description=u'Visualization JSON',
        readonly=True
    )
