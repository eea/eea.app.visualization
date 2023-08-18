""" RestAPI GET enpoints
"""
from plone import api
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter, queryAdapter
from plone.restapi.services import Service
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.interfaces import IExpandableElement
from eea.app.visualization.interfaces import IDataProvenance
from eea.app.visualization.interfaces import IMultiDataProvenance
from eea.app.visualization.cache import ramcache
from Products.CMFPlone.interfaces import IPloneSiteRoot


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class DataProvenance(object):
    """ Get data provenances
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @ramcache(lambda *args: "organisations", lifetime=86400)
    def organisations(self):
        """ Get a mapping of organisations url to title
        """
        organisations = {}
        brains = api.content.find(portal_type='Organisation')
        for brain in brains:
            org = brain.getObject()
            url = getattr(org, 'organisationUrl', '')
            organisations[url] = brain.Title
        return organisations

    def __call__(self, expand=False):
        result = {"provenances": {
            "@id": "{}/@provenances".format(self.context.absolute_url()),
        }}

        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        organisations = self.organisations()
        result['provenances']['items'] = []

        # Get IMultiDataProvenance
        multi = queryAdapter(self.context, IMultiDataProvenance)
        if multi:
            for provenance in multi.provenances:
                owner = provenance.get('owner', '')
                provenance['organisation'] = organisations.get(owner, '')
                result['provenances']['items'].append(json_compatible(provenance))

        source = queryAdapter(self.context, IDataProvenance)
        if (getattr(source, 'link', None) and
            getattr(source, 'title', None) and
            getattr(source, 'owner', None)):
            provenance = {
                "title": json_compatible(source.title),
                "owner": json_compatible(source.owner),
                "link": json_compatible(source.link),
                "organisation": json_compatible(organisations.get(source.owner, ''))
            }

            if getattr(source, "copyrights", None):
                provenance['copyrights'] = json_compatible(source.copyrights)

            result['provenances']['items'].append(provenance)
        return result


@implementer(IPublishTraverse)
class Get(Service):
    """GET"""

    def reply(self):
        """Reply"""
        info = DataProvenance(self.context, self.request)
        return info(expand=True)["provenances"]
