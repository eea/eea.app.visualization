""" JS/CSS provided by this package
"""
from zope.interface import implements
from eea.app.visualization.interfaces import IVisualizationViewResources
from eea.app.visualization.interfaces import IVisualizationEditResources

class VisualizationViewResources(object):
    """ JS/CSS provided by this package that should be included in view mode
    """
    implements(IVisualizationViewResources)

    @property
    def extcss(self):
        """ Required CSS resources
        """
        return [
            u'++resource++eea.jquery.css',
        ]

    @property
    def css(self):
        """ CSS resources
        """
        return [
            '++resource++eea.daviz.buttons.css',
            '++resource++eea.daviz.view.css',
        ]

    @property
    def extjs(self):
        """ Required JS resources
        """
        return [
            u'++resource++eea.jquery.js',
            u'++resource++eea.jquery.tools.js',
        ]

    @property
    def js(self):
        """ JS resources
        """
        return [
            u'++resource++eea.daviz.view.js',
        ]

class VisualizationEditResources(object):
    """ JS/CSS provided by this package that should be included in edit mode
    """
    implements(IVisualizationEditResources)

    @property
    def extcss(self):
        """ Required CSS resources
        """
        return [
            u'++resource++eea.jquery.css',
            u'++resource++eea.jquery.ui.css',
            u'++resource++jquery.slickgrid.css',
        ]

    @property
    def css(self):
        """ CSS resources
        """
        return [
            '++resource++eea.daviz.bootstrap.css',
            '++resource++eea.daviz.common.css',
            '++resource++eea.daviz.edit.css',
        ]

    @property
    def extjs(self):
        """ Required JS resources
        """
        return [
            u'++resource++eea.jquery.js',
            u'++resource++eea.jquery.tools.js',
            u'++resource++eea.jquery.ui.js',
            u'++resource++jquery.slickgrid.js',
        ]

    @property
    def js(self):
        """ JS resources
        """
        return [
            u'++resource++eea.daviz.common.js',
            u'++resource++eea.daviz.edit.js',
        ]
