""" Views exhibit tile interfaces
"""
from zope import schema
from zope.interface import Interface
from eea.app.visualization.views.interfaces import IVisualizationView
from eea.app.visualization.config import EEAMessageFactory as _

class IDataView(IVisualizationView):
    """ Data Settings View
    """

class IDataEdit(Interface):
    """ Data settings Edit
    """
    json = schema.Text(
        title=_(u"Data table"),
        description=_(u"<ul>"
                       "<li>Click on the top-left pencil to "
                           "inspect and edit generate JSON.</li>"
                       "<li>Click on the table's columns headers to adjust "
                       "their labels (user friendly-names)</li>"
                     "</ul>"),
        required=False
    )
    json.order = 20

    sources = schema.List(
        title=_(u'Additional sources'),
        required=False,
        description=_(
            u"(Simile-Exhibit only) "
            "Add additional external exhibit sources to be merged. "
            "Supported formats: "
            "'Exhibit JSON', 'Google Spreadsheet' and 'RDF/XML'. "
            "See more details "
            "http://www.simile-widgets.org/wiki/Exhibit/Creating"
            "%2C_Importing%2C_and_Managing_Data#Conversion_at_Load_Time"),
        value_type=schema.TextLine(title=u'URL')
    )
    sources.order = 30
