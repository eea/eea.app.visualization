""" Daviz Settings Section
"""
from zope import schema
from zope.interface import implements
from zope.formlib.form import FormFields
from eea.app.visualization.controlpanel.interfaces import IDavizSection
from eea.app.visualization.config import EEAMessageFactory as _

class DataSection(object):
    """ Daviz  Settings Section
    """
    implements(IDavizSection)
    prefix = 'data'
    title = 'Data Settings'

    def __init__(self):
        self.form_fields = FormFields(
            schema.Text(
                __name__='data.annotations',
                title=_(u"Annotations"),
                description=_("Data annotations - lowercase - to be "
                              "ignored/handled as annotations when processing "
                              "data tables. One per line "
                              "(e.g. 'n/a', 'n.a.', ':')"),
                required=False),
            )
