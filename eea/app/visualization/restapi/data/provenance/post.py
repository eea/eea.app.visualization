""" RestAPI enpoint POST
"""
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer, alsoProvides
from zope.interface import Interface
from zope.component import adapter, queryAdapter
from plone.restapi.services import Service
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.deserializer import json_body
from eea.app.visualization.interfaces import IDataProvenance, IMultiDataProvenance
from Products.CMFPlone.interfaces import IPloneSiteRoot


import plone.protect.interfaces


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class DataProvenance(object):
    """ Set DataProvenance
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, data=[]):
        if IPloneSiteRoot.providedBy(self.context):
            self.request.response.setStatus(400)
            return dict(
                error=dict(
                    type="BadRequest",
                    message="Tried to set data provenances on site root.",
                )
            )

        source = queryAdapter(self.context, IDataProvenance)
        multi = queryAdapter(self.context, IMultiDataProvenance)
        if not source and not multi:
            self.request.response.setStatus(400)
            return dict(
                error=dict(
                    type="BadRequest",
                    message="Can't adapt IDataProvenance/IMultiDataProvenance to context.",
                )
            )

        multi_provenances = []
        provenances = data.get('provenances', [])
        if len(provenances) < 1:
            self.request.response.setStatus(400)
            return dict(
                error=dict(
                    type="BadRequest",
                    message="No data provenances provided.",
                )
            )

        # differentiate between multi and normal provenances
        if not len(provenances) == 1:
            if not multi:
                multi_provenances = []
            if not source:
                multi_provenances = provenances
                provenances = []
            if multi and source:
                multi_provenances = [prov for prov in provenances if prov.get('multi', True) != 'False']
                provenances = [prov for prov in provenances if prov not in multi_provenances]

        # if more than one non multi provenance is given, save the last one
        if len(provenances) > 1:
            provenances = [provenances[-1]]

        # True if len == 1
        if len(provenances) == 1:
            data = provenances[0]
            source.title = data["title"]
            source.owner = data["owner"]
            source.link = data["link"]

            if "copyrights" in data and hasattr(source, "copyrights"):
                copyrights = data['copyrights']

                if len(copyrights) > 2 and isinstance(copyrights, list):
                    self.request.response.setStatus(400)
                    return dict(
                        error=dict(
                            type="BadRequest",
                            message="Copyrights must be a list with <= 2 items or string.",
                        )
                    )

                if isinstance(copyrights, (str, unicode)):
                    source.copyrights = copyrights
                else:
                    source.copyrights = tuple(copyrights)
            elif "copyrights" in data:
                self.request.response.setStatus(400)
                return dict(
                    error=dict(
                        type="BadRequest",
                        message="Can't set copyrights, not a blob object.",
                    )
                )

        # multi provenances
        if len(multi_provenances) > 0:
            multi.provenances = multi_provenances

        self.request.response.setStatus(200)
        return dict(message="Successfully set data provenance")


@implementer(IPublishTraverse)
class Post(Service):
    """POST"""

    def reply(self):
        """Reply"""
        data = json_body(self.request)

        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)

        post = DataProvenance(self.context, self.request)
        return post(data)