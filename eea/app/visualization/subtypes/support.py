""" Module to enable or disable Exhibit support
"""
import logging
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO

from zope.component import queryAdapter, queryUtility
from zope.event import notify
from zope.interface import alsoProvides, noLongerProvides, implements
from zope.publisher.interfaces import NotFound

from eea.app.visualization.converter.interfaces import IExhibitJsonConverter
from eea.app.visualization.events import VisualizationEnabledEvent
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationEnabled
from eea.app.visualization.subtypes.interfaces import IVisualizationSubtyper

logger = logging.getLogger('eea.app.visualization.converter')

class DavizPublicSupport(BrowserView):
    """ Public support for subtyping objects
        view for non IPossibleVisualization objects
    """
    implements(IVisualizationSubtyper)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _redirect(self, msg = '', to = ''):
        """ Redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(
                    str(msg), type='info')
            if to:
                self.request.response.redirect(self.context.absolute_url() + to)
            else:
                self.request.response.redirect(self.context.absolute_url()
                                                                + "/view")
        return msg

    @property
    def can_enable(self):
        """ See IVisualizationSubtyper
        """
        return False

    @property
    def can_disable(self):
        """ See IVisualizationSubtyper
        """
        return False

    @property
    def is_exhibit(self):
        """ Is exhibit?
        """
        return False


    def enable(self):
        """ See IVisualizationSubtyper
        """
        raise NotFound(self.context, 'enable', self.request)

    def disable(self):
        """ See IVisualizationSubtyper
        """
        raise NotFound(self.context, 'disable', self.request)


class DavizSupport(DavizPublicSupport):
    """ Enable/Disable Exhibit
    """

    def _redirect(self, msg='', to='/daviz-edit.html'):
        """ Return or redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(
                    str(msg), type='info')
            if to:
                self.request.response.redirect(self.context.absolute_url() + to)
            else:
                self.request.response.redirect(self.context.absolute_url()
                                                                + "/view")
        return msg

    @property
    def can_enable(self):
        """ See IVisualizationSubtyper
        """
        return not self.is_exhibit

    @property
    def can_disable(self):
        """ See IVisualizationSubtyper
        """
        return self.is_exhibit

    @property
    def is_exhibit(self):
        """ Is exhibit viewable?
        """
        return IVisualizationEnabled.providedBy(self.context)

    def enable(self):
        """ Enable Exhibit
        """
        datafile = StringIO(self.context.getFile().data)
        converter = queryUtility(IExhibitJsonConverter)
        try:
            columns, json = converter(datafile)
        except Exception, err:
            logger.exception(err)
            return self._redirect(('An error occured while trying to convert '
                                   'attached file. Please ensure you provided '
                                   'a valid CSV file'), '/view')

        if not IVisualizationEnabled.providedBy(self.context):
            alsoProvides(self.context, IVisualizationEnabled)

        # Update annotations
        mutator = queryAdapter(self.context, IVisualizationConfig)
        mutator.json = json
        notify(VisualizationEnabledEvent(self.context, columns=columns))
        return self._redirect('Enabled Exhibit view')

    def disable(self):
        """ Disable Exhibit
        """
        noLongerProvides(self.context, IVisualizationEnabled)
        return self._redirect('Removed Exhibit view', to='')