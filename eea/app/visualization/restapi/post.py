""" RestAPI enpoint @geolocation GET
"""
# pylint: disable = W0702
# pylint: disable = W0612
from plone import api
from plone.restapi.services import Service
from zope.component import getUtility, queryUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from plone.restapi.interfaces import IExpandableElement
from zope.component import adapter
from zope.interface import Interface
from plone.restapi.serializer.converters import json_compatible
from eea.app.visualization.interfaces import IDataProvenance


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class DataProvenance(object):
    """ Get workflow progress
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        result = {}
        import pdb; pdb.set_trace()
        if IPloneSiteRoot.providedBy(self.context):
            return result

        source = IDataProvenance(self.context)
        return result


@implementer(IPublishTraverse)
class Get(Service):
    """GET"""

    def reply(self):
        """Reply"""
        import pdb; pdb.set_trace()
        data = DataProvenance(self.context, self.request)
        return data