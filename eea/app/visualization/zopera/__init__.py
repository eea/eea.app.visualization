""" Plone/Zope2 safe imports
"""
from zope.interface import Interface
#
# from Products.statusmessages.interfaces import IStatusMessage
#
try:
    from Products.statusmessages import interfaces
    IStatusMessage = interfaces.IStatusMessage
except ImportError:
    class IStatusMessage(Interface):
        """ Fallback status message interface """
#
# from Products.CMFCore.interfaces import IPropertiesTool
#
try:
    from Products.CMFCore import interfaces
    IPropertiesTool = interfaces.IPropertiesTool
except ImportError:
    class IPropertiesTool(Interface):
        """ Empty properties tool"""

try:
    from Products.CMFCore import utils
    getToolByName = utils.getToolByName
except ImportError:
    _marker = ()  # Create a new marker object.

    def getToolByName(obj, name, default=_marker):

        """ Get the tool, 'toolname', by acquiring it.

        o Application code should use this method, rather than simply
          acquiring the tool by name, to ease forward migration (e.g.,
          to Zope3).
        """
        if default is _marker:
            raise AttributeError(name)
        return default
#
# from Products.CMFCore.interfaces import IFolderish
#
try:
    from Products.CMFCore import interfaces
    IFolderish = interfaces.IFolderish
except ImportError:
    class IFolderish(Interface):
        """ Fallback folderish interface
        """
#
# from Products.EEAContentTypes.interfaces import IEEAContent
#
try:
    from Products.EEAContentTypes import interfaces
    IEEAContent = interfaces.IEEAContent
except ImportError:
    class IEEAContent(Interface):
        """ Fallback interface
        """
#
# from Products.ResourceRegistries.tools import packer
#
try:
    from Products.ResourceRegistries import tools
    packer = tools.packer
except ImportError:
    from eea.app.visualization.zopera import packer
#
# from plone.app.blob.interfaces import IATBlob
#
try:
    from plone.app.blob import interfaces
    IATBlob = interfaces.IATBlob
except ImportError:
    class IATBlob(Interface):
        """ Fallback interface
        """
#
# from plone.scale import scaleImage
#
try:
    from plone.scale import scale
    scaleImage = scale.scaleImage
except ImportError:
    def scaleImage(image, **kwargs):
        """ Fallback scaleImage
        """
        return image
#
# from plone.app.form import default_subpage_template
#
try:
    from plone.app import form
    default_subpage_template = form.default_subpage_template
except ImportError:
    try:
        from zope.browserpage import ViewPageTemplateFile
        from zope.browserpage import namedtemplate
        __pyflakes__ = (namedtemplate, ViewPageTemplateFile)
    except ImportError:
        from zope.app import pagetemplate
        ViewPageTemplateFile = pagetemplate.ViewPageTemplateFile
        namedtemplate = pagetemplate.namedtemplate
    from zope.formlib.interfaces import ISubPageForm
    default_subpage_template = namedtemplate.NamedTemplateImplementation(
        ViewPageTemplateFile('subpageform.pt'), ISubPageForm)
#
# from plone.app.form.events import EditBegunEvent
#
try:
    from plone.app.form import events
    EditBegunEvent = events.EditBegunEvent
except ImportError:
    from zope.component.interfaces import ObjectEvent

    class EditBegunEvent(ObjectEvent):
        """ Fallback event
        """

__all__ = [
    IStatusMessage.__name__,
    IPropertiesTool.__name__,
    packer.__name__
]
