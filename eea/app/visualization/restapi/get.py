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

    def __call__(self):
        result = []

        if IPloneSiteRoot.providedBy(self.context):
            return result

        source = queryAdapter(self.context, IDataProvenance)
        if source:
            result.append({
                "title": json_compatible(source.title),
                "owner": json_compatible(source.owner),
                "link": json_compatible(source.link)
            })

            if hasattr(source, "copyrights"):
                result[0].update({"copyrights": json_compatible(source.copyrights)})

        # also get IMultiDataProvenance
        multi = queryAdapter(self.context, IMultiDataProvenance)
        if multi:
            provenances = json_compatible(multi.provenances)

            if hasattr(multi, "copyrights"):
                provenances[0].update({"copyrights": json_compatible(multi.copyrights)})

        result += provenances
        return result


@implementer(IPublishTraverse)
class Get(Service):
    """GET"""

    def reply(self):
        """Reply"""
        data = DataProvenance(self.context, self.request)
        return data()