""" Visualization Data Interfaces
"""
from zope.interface import Interface
from zope import schema

class IDataProvenance(Interface):
    """ Data Provenance
    """
    title = schema.TextLine(
        title=u"Data source title",
        description=u"Specify data source",
    )

    link = schema.TextLine(
        title=u"Data source link",
        description=u"Specify data source link"
    )

    owner = schema.TextLine(
        title=u"Data source Organisation",
        description=u"Specify data source Organisation"
    )

class IVisualizationData(Interface):
    """ Visualization Data Adapter.
    """
    data = schema.Text(
        title=u'Data',
        description=u'Data to be converted to JSON',
        readonly=True
        )

class IVisualizationJson(Interface):
    """ Visualization data JSON (daviz.json)
    """
    json = schema.Text(
        title=u'JSON',
        description=u'Visualization JSON',
        readonly=True
    )

class IVisualizationJsonUtils(Interface):
    """ Utility to handle Visualization JSON
    """
    def mergeProperties(old, new):
        """ Merge new dictionary to old one and returns the old one
        """

    def sortProperties(strJson, indent=1):
        """ In the JSON string set the correct order of the columns
        """
