""" RestAPI enpoint @dataprovenance GET
"""
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter
from plone.restapi.services import Service
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.interfaces import IExpandableElement
from eea.app.visualization.interfaces import IDataProvenance
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
        result = {}

        if IPloneSiteRoot.providedBy(self.context):
            return result

        source = IDataProvenance(self.context)
        result.update({"@title": json_compatible(source.title)})
        result.update({"@owner": json_compatible(source.owner)})
        result.update({"@link": json_compatible(source.link)})

        if hasattr(source, "copyrights"):
            result.update({"@copyrights": json_compatible(source.copyrights)})

        return result


@implementer(IPublishTraverse)
class Get(Service):
    """GET"""

    def reply(self):
        """Reply"""
        data = DataProvenance(self.context, self.request)
        return data()