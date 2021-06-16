""" RestAPI GET enpoints
"""
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter, queryMultiAdapter
from plone.restapi.services import Service
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.interfaces import IExpandableElement
from Products.CMFPlone.interfaces import IPloneSiteRoot
from eea.app.visualization.interfaces import IVisualizationEnabled


@implementer(IExpandableElement)
@adapter(IVisualizationEnabled, Interface)
class DataTable(object):
    """ Get data table
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"table": {
            "@id": "{}/@table".format(self.context.absolute_url()),
        }}

        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        view = queryMultiAdapter((
            self.context, self.request),
            name='download.table'
        )

        if not view:
            return result

        result['table'].update(json_compatible(view.data))
        return result


@implementer(IPublishTraverse)
class Get(Service):
    """GET"""

    def reply(self):
        """Reply"""
        info = DataTable(self.context, self.request)
        return info(expand=True)["table"]
