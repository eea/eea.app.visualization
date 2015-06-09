""" Daviz Settings Section
"""
from zope import schema
from zope.interface import implements
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
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

class ForbiddenVisualizations(object):
    """ Enable / disable visualizations per content-type
    """
    implements(IDavizSection)
    prefix = 'forbidden'
    title = _('Enable / Disable')

    def __init__(self):
        voc = queryUtility(IVocabularyFactory,
                           name=u'eea.daviz.vocabularies.ViewsVocabulary')
        value_type = schema.Choice(
            vocabulary="plone.app.vocabularies.UserFriendlyTypes")

        fields = []
        for term in voc():
            field = schema.List(
                __name__='.'.join((self.prefix, term.value)),
                title=u'Disable ' + term.title,
                description=(
                    u"Disable %s for the "
                    "following content-types" % term.title),
                required=False,
                value_type=value_type
            )
            fields.append(field)
        self.form_fields = FormFields(*fields)
