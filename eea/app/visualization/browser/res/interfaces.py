""" JS/CSS resources utilities
"""
from zope import schema
from zope.interface import Interface

class IVisualizationViewResources(Interface):
    """ CSS/JS to be included by daviz-view.html
    """
    extcss = schema.List(
        title=u'External or required stylesheets',
        description=(u'List of CSS resources to be included in view mode '
                     'before CSS reources provided by css attribute'),
        value_type=schema.TextLine(title=u'ExtCSS'),
        readonly=True
    )

    css = schema.List(
        title=u'Stylesheets',
        description=u'List of CSS resources to be included by daviz-view.html',
        value_type=schema.TextLine(title=u'CSS'),
        readonly=True
    )

    extjs = schema.List(
        title=u'External or required javascripts',
        description=(u'List of JS resources to be included in view mode '
                     'before JS reources provided by js attribute'),
        value_type=schema.TextLine(title=u'ExtJS'),
        readonly=True
    )
    js = schema.List(
        title=u'Javascripts',
        description=u'List of JS resources to be included by daviz-view.html',
        value_type=schema.TextLine(title=u'JS'),
        readonly=True
    )

class IVisualizationEditResources(Interface):
    """ CSS/JS to be included by daviz-edit.html
    """
    extcss = schema.List(
        title=u'External or required stylesheets',
        description=(u'List of CSS resources to be included in edit mode '
                     'before CSS reources provided by css attribute'),
        value_type=schema.TextLine(title=u'ExtCSS'),
        readonly=True
    )

    css = schema.List(
        title=u'Stylesheets',
        description=u'List of CSS resources to be included by daviz-view.html',
        value_type=schema.TextLine(title=u'CSS'),
        readonly=True
    )
    extjs = schema.List(
            title=u'External or required javascripts',
            description=(u'List of JS resources to be included in edit mode '
                         'before JS reources provided by js attribute'),
            value_type=schema.TextLine(title=u'EXTJS'),
            readonly=True
        )
    js = schema.List(
        title=u'Javascripts',
        description=u'List of JS resources to be included by daviz-view.html',
        value_type=schema.TextLine(title=u'JS'),
        readonly=True
    )
