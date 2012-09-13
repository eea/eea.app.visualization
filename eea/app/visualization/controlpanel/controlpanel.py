""" Daviz Settings Section
"""
from zope.interface import implements
from eea.app.visualization.controlpanel.interfaces import IDavizSection
from zope.formlib.form import FormFields
from zope import schema

class DavizSection(object):
    """ Daviz  Settings Section
    """
    implements(IDavizSection)
    prefix = 'daviz'
    title = 'Daviz Settings'

    form_fields = FormFields(
        schema.TextLine(
            __name__='daviz.defaultfolder',
            title=u'Default Folder for Visualizations',
            required=True)
        )

DavizSectionFactory = DavizSection()