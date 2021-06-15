""" RestAPI enpoint @dataprovenance GET
"""
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter, queryAdapter
from plone.restapi.services import Service
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.interfaces import IExpandableElement
from eea.app.visualization.interfaces import IDataProvenance, IMultiDataProvenance
from Products.CMFPlone.interfaces import IPloneSiteRoot


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class DataProvenance(object):
    """ Get dataprovenance
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"data.provenance": {
            "@id": "{}/@dataprovenance".format(self.context.absolute_url()),
        }}

        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        result['data.provenance']['provenances'] = []
        source = queryAdapter(self.context, IDataProvenance)
        if source:
            result['data.provenance']['provenances'].append({
                "title": json_compatible(source.title),
                "owner": json_compatible(source.owner),
                "link": json_compatible(source.link)
            })

            if hasattr(source, "copyrights"):
                result['data.provenance']['provenances'][0].update({"copyrights": json_compatible(source.copyrights)})

        # also get IMultiDataProvenance
        multi = queryAdapter(self.context, IMultiDataProvenance)
        if multi:
            provenances = json_compatible(multi.provenances)
            result['data.provenance']['provenances'] += provenances
        return result


@implementer(IPublishTraverse)
class Get(Service):
    """GET"""

    def reply(self):
        """Reply"""
        info = DataProvenance(self.context, self.request)
        return info(expand=True)["data.provenance"]