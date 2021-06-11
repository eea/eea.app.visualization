""" RestAPI enpoint @dataprovenance POST
"""
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implementer, alsoProvides
from zope.interface import Interface
from zope.component import adapter
from plone.restapi.services import Service
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.deserializer import json_body
from eea.app.visualization.interfaces import IDataProvenance
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

    def __call__(self, data={}):
        if IPloneSiteRoot.providedBy(self.context):
            self.request.response.setStatus(400)
            return dict(
                error=dict(
                    type="BadRequest",
                    message="Tried to set dataprovenance on site root.",
                )
            )

        source = IDataProvenance(self.context)
        source.title = data["@title"]
        source.owner = data["@owner"]
        source.link = data["@link"]

        if "@copyrights" in data and hasattr(source, "copyrights"):
            copyrights = data['@copyrights']

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
        elif "@copyrights" in data:
            self.request.response.setStatus(400)
            return dict(
                error=dict(
                    type="BadRequest",
                    message="Can't set copyrights, not a blob object.",
                )
            )

        self.request.response.setStatus(200)
        return dict(message="Successfully set dataprovenance")



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