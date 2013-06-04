""" JS/CSS resources utilities
"""
from zope import schema
from zope.interface import Interface

from eea.app.visualization.config import EEAMessageFactory as _

class IVisualizationViewResources(Interface):
    """ CSS/JS to be included by daviz-view.html
    """
    extcss = schema.List(
        title=_(u'External or required stylesheets'),
        description=_(u'List of CSS resources to be included in view mode '
                     'before CSS reources provided by css attribute'),
        value_type=schema.TextLine(title=u'ExtCSS'),
        readonly=True
    )

    css = schema.List(
        title=_(u'Stylesheets'),
        description=\
            _(u'List of CSS resources to be included by daviz-view.html'),
        value_type=schema.TextLine(title=u'CSS'),
        readonly=True
    )

    extjs = schema.List(
        title=_(u'External or required javascripts'),
        description=_(u'List of JS resources to be included in view mode '
                     'before JS reources provided by js attribute'),
        value_type=schema.TextLine(title=u'ExtJS'),
        readonly=True
    )
    js = schema.List(
        title=_(u'Javascripts'),
        description=\
            _(u'List of JS resources to be included by daviz-view.html'),
        value_type=schema.TextLine(title=u'JS'),
        readonly=True
    )

class IVisualizationEditResources(Interface):
    """ CSS/JS to be included by daviz-edit.html
    """
    extcss = schema.List(
        title=_(u'External or required stylesheets'),
        description=_(u'List of CSS resources to be included in edit mode '
                     'before CSS reources provided by css attribute'),
        value_type=schema.TextLine(title=u'ExtCSS'),
        readonly=True
    )

    css = schema.List(
        title=_(u'Stylesheets'),
        description=\
            _(u'List of CSS resources to be included by daviz-view.html'),
        value_type=schema.TextLine(title=u'CSS'),
        readonly=True
    )
    extjs = schema.List(
            title=_(u'External or required javascripts'),
            description=_(u'List of JS resources to be included in edit mode '
                         'before JS reources provided by js attribute'),
            value_type=schema.TextLine(title=u'EXTJS'),
            readonly=True
        )
    js = schema.List(
        title=_(u'Javascripts'),
        description=\
            _(u'List of JS resources to be included by daviz-view.html'),
        value_type=schema.TextLine(title=u'JS'),
        readonly=True
    )

class IVisualizationViewHeader(Interface):
    """ Custom HTML to be included by daviz-view.html within <head>
    """
    def __call__(context, request):
        """ Get HTML header
        """
