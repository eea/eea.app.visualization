""" Charts
"""
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter, queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from eea.app.visualization.interfaces import IVisualizationEnabled

@implementer(IExpandableElement)
@adapter(IVisualizationEnabled, Interface)
class Charts(object):
    """ Charts
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"charts": {"@id": "{}/@charts".format(
            self.context.absolute_url())}}

        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        view = queryMultiAdapter((
            self.context, self.request),
            name='daviz-view.html'
        )

        if not view:
            return result

        result["charts"]["items"] = []
        for tab in view.tabs:
            result["charts"]["items"].append(json_compatible(tab))
        return result


class ChartsGet(Service):
    """Get charts information"""

    def reply(self):
        """ Reply
        """
        info = Charts(self.context, self.request)
        return info(expand=True)["charts"]
