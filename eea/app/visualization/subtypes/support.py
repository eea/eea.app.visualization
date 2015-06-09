""" Module to enable or disable visualization
"""
import logging
from Products.Five.browser import BrowserView
from StringIO import StringIO

from zope.component import queryAdapter, queryUtility, queryMultiAdapter
from zope.event import notify
from zope.interface import alsoProvides, noLongerProvides, implements
from zope.publisher.interfaces import NotFound

from eea.app.visualization.converter.interfaces import ITable2JsonConverter
from eea.app.visualization.events import VisualizationEnabledEvent
from eea.app.visualization.events import VisualizationDisabledEvent
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.interfaces import IVisualizationEnabled
from eea.app.visualization.interfaces import IVisualizationData
from eea.app.visualization.subtypes.interfaces import IVisualizationSubtyper
from eea.app.visualization.zopera import IStatusMessage

logger = logging.getLogger('eea.app.visualization.converter')

class DavizPublicSupport(BrowserView):
    """ Public support for subtyping objects
        view for non IPossibleVisualization objects
    """
    implements(IVisualizationSubtyper)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _redirect(self, msg='', to=''):
        """ Redirect
        """
        if self.request:
            if msg:
                status = queryAdapter(self.request, IStatusMessage)
                if status:
                    status.addStatusMessage(str(msg), type='info')
            if to:
                self.request.response.redirect(
                    self.context.absolute_url() + to)
            else:
                self.request.response.redirect(
                    self.context.absolute_url() + "/view")
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
    def can_edit(self):
        """ See IVisualizationSubtyper
        """
        return False

    @property
    def is_visualization(self):
        """ Is visualization enabled?
        """
        return False

    #BBB: This will be removed in the next version of this package
    is_exhibit = is_visualization

    def enable(self):
        """ See IVisualizationSubtyper
        """
        raise NotFound(self.context, 'enable', self.request)

    def disable(self):
        """ See IVisualizationSubtyper
        """
        raise NotFound(self.context, 'disable', self.request)


class DavizSupport(DavizPublicSupport):
    """ Enable/Disable visualization
    """

    def _redirect(self, msg='', to='/daviz-edit.html'):
        """ Return or redirect
        """
        if self.request:
            if msg:
                status = queryAdapter(self.request, IStatusMessage)
                if status:
                    status.addStatusMessage(str(msg), type='info')
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
        return not self.is_visualization

    @property
    def can_disable(self):
        """ See IVisualizationSubtyper
        """
        return self.is_visualization

    @property
    def can_edit(self):
        """ Can edit visualization
        """
        if not self.is_visualization:
            return False

        # Is locked
        locked = queryMultiAdapter((self.context, self.request),
                                      name=u'plone_lock_info')
        locked = getattr(locked, 'is_locked_for_current_user', lambda: False)

        if locked():
            return False

        return True

    @property
    def is_visualization(self):
        """ Is visualization enabled?
        """
        return IVisualizationEnabled.providedBy(self.context)

    #BBB: This will be removed in the next version of this package
    is_exhibit = is_visualization

    def enable(self):
        """ Enable visualization
        """
        visualization = queryAdapter(self.context, IVisualizationData)
        datafile = StringIO(visualization.data)
        converter = queryUtility(ITable2JsonConverter)
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
        return self._redirect('Visualization enabled')

    def disable(self):
        """ Disable visualization
        """
        noLongerProvides(self.context, IVisualizationEnabled)
        notify(VisualizationDisabledEvent(self.context))
        return self._redirect('Visualization disabled', to='')
