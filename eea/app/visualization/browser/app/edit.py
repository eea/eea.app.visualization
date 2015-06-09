""" Module for Edit logic of browser/app package
"""
import logging
import json
from zope import event
from zope.component import queryUtility
from zope.component import queryAdapter, queryMultiAdapter
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory
from Products.Five.browser import BrowserView
from zope.schema.vocabulary import SimpleTerm
from eea.app.visualization.interfaces import IVisualizationConfig
from eea.app.visualization.events import VisualizationFacetDeletedEvent
from eea.app.visualization.zopera import IStatusMessage
from eea.app.visualization.zopera import EditBegunEvent
from eea.app.visualization.interfaces import IDavizSettings
from eea.app.visualization.config import EEAMessageFactory as _

logger = logging.getLogger('eea.app.visualization')

DAVIZ_WARNING_WRONG_DATASET = """Data is missing, or is not well formated."""
DAVIZ_WARNING_NO_DATA = """Your data contains no rows."""
DAVIZ_WARNING_DATA_2000 = """Your data contains more than 2000 rows.
    The visualisation may be slow in Internet Explorer below version 9."""
DAVIZ_WARNING_DATA_4000 = """Your data contains more than 4000 rows.
    The visualisation may be slow or become unresponsive."""


class Edit(BrowserView):
    """ Edit page
    """
    @property
    def views_vocabulary(self):
        """ Views vocabulary
        """
        voc = queryUtility(IVocabularyFactory,
                           name=u'eea.daviz.vocabularies.ViewsVocabulary')
        return voc(self.context)

    @property
    def facets_vocabulary(self):
        """ Return facets
        """
        accessor = queryAdapter(self.context, IVisualizationConfig)
        for facet in accessor.facets:
            yield facet

    @property
    def enabled_views(self):
        """ Return saved views
        """
        accessor = queryAdapter(self.context, IVisualizationConfig)
        return [view.get('name') for view in accessor.views]

    @property
    def sorted_views(self):
        """ Return all views sorted by enabled views as a SimpleVocabulary
        """
        views = self.views_vocabulary
        mapping = dict((term.value, term.title) for term in views)

        enabled = self.enabled_views
        for name in enabled:
            yield SimpleTerm(name, name, mapping.get(name, name))

        settings = queryUtility(IDavizSettings)
        for view in views:
            if settings and settings.disabled(view.value, self.context):
                continue
            if view.value in enabled:
                continue
            yield SimpleTerm(view.value, "", view.title)

    def get_view(self, name):
        """ Return given view
        """
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        return queryMultiAdapter((self.context, self.request), name=name)

    def get_edit(self, name):
        """ Return edit page
        """
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        name += u'.edit'
        return queryMultiAdapter((self.context, self.request), name=name)

    def get_facet_form(self, facet):
        """ Edit form for facet
        """
        ftype = facet.get('type', '')
        if not isinstance(ftype, unicode):
            ftype = ftype.decode('utf-8')
        ftype += u'.edit'

        form = queryMultiAdapter((self.context, self.request), name=ftype)
        if form:
            name = facet.get('name', '')
            form.prefix = name

        return form

    def get_facet_add(self, facetname):
        """ Add form for facet
        """
        form = queryMultiAdapter((self.context, self.request), name=facetname)
        if form:
            form.prefix = facetname.replace('.', '-')
        return form

    def hasErrors(self):
        """ Check if data has any issues
        """
        results = getMultiAdapter((self.context, self.request),
                                    name="daviz.json")()
        results_json = json.loads(results)
        items_nr = len(results_json.get('items', []))
        if not results_json.get('properties', {}):
            return DAVIZ_WARNING_WRONG_DATASET
        if items_nr == 0:
            return DAVIZ_WARNING_NO_DATA
        if items_nr > 2000 and items_nr < 4001:
            return DAVIZ_WARNING_DATA_2000
        if items_nr > 4000:
            return DAVIZ_WARNING_DATA_4000
        return ""

    def __call__(self, **kwargs):
        support = queryMultiAdapter((self.context, self.request),
                                    name='daviz_support')
        if support.can_edit:
            event.notify(EditBegunEvent(self.context))
            return self.index()

        return self.request.response.redirect(self.context.absolute_url())

class Configure(BrowserView):
    """ Edit controller
    """
    def _redirect(self, msg='', ajax=False, to='daviz-edit.html'):
        """ Return or redirect
        """
        if ajax:
            return msg

        if not self.request:
            return msg

        status = queryAdapter(self.request, IStatusMessage)
        if msg and status:
            status.addStatusMessage(str(msg), type='info')
        self.request.response.redirect(to)
        return msg

    def handle_facets(self, **kwargs):
        """ Update facets position
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        order = kwargs.get('order', [])
        ajax = (kwargs.get('daviz.facets.save') == 'ajax')

        if not order:
            return self._redirect(
                _('Exhibit facets settings not saved: Nothing to do'), ajax)

        if not isinstance(order, list):
            return self._redirect(
                _('Exhibit facets settings not saved: Nothing to do'), ajax)

        if len(order) == 1:
            return self._redirect(
                _('Exhibit facets settings not saved: Nothing to do'), ajax)

        facets = mutator.facets
        facets = dict((facet.get('name'), dict(facet)) for facet in facets)
        mutator.delete_facets()

        for name in order:
            properties = facets.get(name, {})
            if not properties:
                logger.exception('Unknown facet id: %s', name)
                continue
            mutator.add_facet(**properties)

        return self._redirect(_('Exhibit facets settings saved'), ajax)

    def handle_facetDelete(self, **kwargs):
        """ Delete facet
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        name = kwargs.get('name', '')
        ajax = (kwargs.get('daviz.facet.delete') == 'ajax')
        try:
            mutator.delete_facet(name)
        except KeyError, err:
            logger.exception(err)
            return self._redirect(err, ajax)
        else:
            event.notify(VisualizationFacetDeletedEvent(
                self.context, facet=name))

        return self._redirect(_('Exhibit facet deleted'), ajax)

    def handle_viewEnable(self, **kwargs):
        """ Enable view
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        name = kwargs.get('name', '')
        ajax = (kwargs.get('daviz.view.enable') == 'ajax')
        try:
            mutator.add_view(name)
        except Exception, err:
            logger.exception(err)
            return self._redirect(err, ajax)
        return self._redirect(_('View enabled'), ajax)

    def handle_views(self, **kwargs):
        """ Sort views
        """
        mutator = queryAdapter(self.context, IVisualizationConfig)
        order = kwargs.get('order', [])
        ajax = (kwargs.get('daviz.views.save') == 'ajax')

        if not order:
            return self._redirect(
                _('Views settings not saved: Nothing to do'), ajax)

        if not isinstance(order, list):
            return self._redirect(
                _('Views order not saved: Nothing to do'), ajax)

        if len(order) == 1:
            return self._redirect(
                _('Views order not saved: Nothing to do'), ajax)

        views = mutator.views
        views = dict((view.get('name'), dict(view)) for view in views)
        mutator.delete_views()

        for name in order:
            properties = views.get(name, {})
            if not properties:
                continue
            mutator.add_view(**properties)

        return self._redirect(_('Views order changed'), ajax)



    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        if kwargs.get('daviz.facets.save', None):
            return self.handle_facets(**kwargs)
        elif kwargs.get('daviz.facet.delete', None):
            return self.handle_facetDelete(**kwargs)
        elif kwargs.get('daviz.view.enable', None):
            return self.handle_viewEnable(**kwargs)
        elif kwargs.get('daviz.views.save', None):
            return self.handle_views(**kwargs)

        return self._redirect('Invalid action provided')
