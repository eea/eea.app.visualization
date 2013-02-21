""" Handler module containing configure logic

    >>> from zope.interface import alsoProvides
    >>> from eea.app.visualization.interfaces import IVisualizationEnabled
    >>> portal = layer['portal']
    >>> sandbox = portal.invokeFactory('File', 'sandbox')
    >>> sandbox = portal._getOb(sandbox)
    >>> alsoProvides(sandbox, IVisualizationEnabled)
    >>> sandbox = portal._getOb('sandbox')

"""
from zope.interface import implements
from eea.app.visualization.interfaces import IVisualizationConfig
from zope.annotation.interfaces import IAnnotations

from persistent.dict import PersistentDict
from persistent.list import PersistentList
from eea.app.visualization.config import (
    ANNO_VIEWS, ANNO_FACETS, ANNO_JSON, ANNO_SOURCES
)

class Configure(object):
    """ Get visualization configuration

    >>> from eea.app.visualization.interfaces import IVisualizationConfig
    >>> visualization = IVisualizationConfig(sandbox)
    >>> visualization
    <eea.app.visualization.storage.handler.Configure object...>

    """
    implements(IVisualizationConfig)

    def __init__(self, context):
        self.context = context

    def _views(self):
        """ Returns views from ANNO_VIEWS config
        """
        anno = IAnnotations(self.context)
        views = anno.get(ANNO_VIEWS, None)
        if views is None:
            views = anno[ANNO_VIEWS] = PersistentList()
        return views

    def _facets(self):
        """ Returns facets from ANNO_FACETS config
        """
        anno = IAnnotations(self.context)
        facets = anno.get(ANNO_FACETS, None)
        if facets is None:
            facets = anno[ANNO_FACETS] = PersistentList()
        return facets

    def _sources(self):
        """ External sources
        """
        anno = IAnnotations(self.context)
        sources = anno.get(ANNO_SOURCES, None)
        if sources is None:
            sources = anno[ANNO_SOURCES] = PersistentList()
        return sources

    def _json(self):
        """ Returns json from ANNO_JSON config
        """
        anno = IAnnotations(self.context)
        json = anno.get(ANNO_JSON, None)
        if json is None:
            json = anno[ANNO_JSON] = PersistentDict()
        return json
    #
    # Accessors
    #
    @property
    def views(self):
        """ Return enabled views

            >>> visualization.views
            []

        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_VIEWS, [])

    @property
    def facets(self):
        """ Return enabled facets

            >>> visualization.facets
            []

        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_FACETS, [])

    @property
    def sources(self):
        """ Return external sources

            >>> visualization.sources
            []

        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_SOURCES, [])

    def set_json(self, value):
        """ Set json dict

        Items are not persisted within annotations, they should be
        dynamically generated each time according with JSON['properties']

            >>> visualization.json = {
            ...   'items': [1, 2, 3],
            ...   'properties': {'a': 'b'}}
            >>> visualization.json
            {'items': [], 'properties': {'a': 'b'}}

        """

        value['items'] = []
        value.setdefault('properties', {})
        anno = IAnnotations(self.context)
        anno[ANNO_JSON] = PersistentDict(value)

    def get_json(self):
        """ Return json from annotations

            >>> visualization.json
            {'items': [], 'properties': {'a': 'b'}}

        """
        anno = IAnnotations(self.context)
        json = anno.get(ANNO_JSON, {})
        return json

    json = property(get_json, set_json)

    def view(self, key, default=None):
        """ Return view by given key

            >>> visualization.view('eea.daviz.tabular', 'Not found')
            'Not found'

        """
        for view in self.views:
            if view.get('name', None) != key:
                continue
            return view
        return default

    def facet(self, key, default=None):
        """ Return facet by given key

            >>> visualization.facet('country', 'Not found')
            'Not found'

        """
        for facet in self.facets:
            if facet.get('name') != key:
                continue
            config = self.json.get('properties', {}).get(key, {})
            label = config.get('label', '')
            if isinstance(label, str):
                label = label.decode('utf-8')
            if label and facet.get('label', '') != label:
                facet['label'] = label
            facet.setdefault('label', key)
            return facet
        return default

    def source(self, key, default=None):
        """ Return source by given key

            >>> visualization.source('http://google.com', 'Not found')
            'Not found'

        """
        for source in self.sources:
            if source.get('name') != key:
                continue
            return source
        return default
    #
    # View mutators
    #
    def add_view(self, name, order=None, **kwargs):
        """ Add view

            >>> _ = visualization.add_view(name='daviz.map',
            ...                     lat='latitude', long='longitude')
            >>> view = visualization.view('daviz.map')
            >>> sorted(view.items())
            [('lat', 'latitude'), ('long', 'longitude'), ('name', 'daviz.map')]

        """
        config = self._views()
        kwargs.update({'name': name})
        view = PersistentDict(kwargs)
        if isinstance(order, int):
            config.insert(order, view)
        else:
            config.append(view)
        return view.get('name', '')

    def edit_view(self, key, **kwargs):
        """ Edit view properties

            >>> visualization.edit_view('daviz.map', lat='lat')
            >>> view = visualization.view('daviz.map')
            >>> sorted(view.items())
            [('lat', 'lat'), ('long', 'longitude'), ('name', 'daviz.map')]

        """
        view = self.view(key)
        if not view:
            raise KeyError, key
        view.update(kwargs)

    def delete_view(self, key):
        """ Delete view by given key

            >>> visualization.delete_view('daviz.map')
            >>> visualization.views
            []

        """
        config = self._views()
        for index, view in enumerate(config):
            if view.get('name', '') == key:
                config.pop(index)
                return
        raise KeyError, key

    def delete_views(self):
        """ Reset views

            >>> _ = visualization.add_view('xxx')
            >>> visualization.views
            [{'name': 'xxx'}]

            >>> visualization.delete_views()
            >>> visualization.views
            []

        """
        anno = IAnnotations(self.context)
        anno[ANNO_VIEWS] = PersistentList()
    #
    # Facet mutators
    #
    def add_facet(self, name, **kwargs):
        """ Add facet

            >>> _ = visualization.add_facet('country', a=1, b=2)
            >>> facet = visualization.facet('country')
            >>> sorted(facet.items())
            [('a', 1), ('b', 2), ('label', 'country'), ('name', ...]

        """
        config = self._facets()
        kwargs.update({'name': name})
        kwargs.setdefault('type', u'daviz.list.facet')
        facet = PersistentDict(kwargs)
        config.append(facet)
        return facet.get('name', '')

    def edit_facet(self, key, **kwargs):
        """ Edit facet properties

            >>> visualization.edit_facet('country', label='One', a=2)
            >>> facet = visualization.facet('country')
            >>> sorted(facet.items())
            [('a', 2), ('b', 2), ('label', 'One'), ('name', ...]

        """
        facet = self.facet(key)
        if not facet:
            raise KeyError, key

        if 'label' in kwargs:
            data = self.json
            properties = data.get('properties', {})
            properties.setdefault(key, {})
            properties[key]['label'] = kwargs.get('label')
        facet.update(kwargs)

    def delete_facet(self, key):
        """ Delete facet by given key

            >>> visualization.delete_facet('country')
            >>> visualization.facets
            []

        """
        config = self._facets()
        for index, facet in enumerate(config):
            if facet.get('name', '') == key:
                config.pop(index)
                return
        raise KeyError, key

    def delete_facets(self):
        """ Remove all facets

            >>> _ = visualization.add_facet('xxx')
            >>> visualization.facets
            [...'name': 'xxx'...]

            >>> visualization.delete_facets()
            >>> visualization.facets
            []

        """
        anno = IAnnotations(self.context)
        anno[ANNO_FACETS] = PersistentList()
    #
    # Source mutators
    #
    def add_source(self, name, **kwargs):
        """ Add source

            >>> _ = visualization.add_source('http://bit.ly/rdf', type='rdf')
            >>> source = visualization.source('http://bit.ly/rdf')
            >>> sorted(source.items())
            [('name', 'http://bit.ly/rdf'), ('type', 'rdf')]

        """
        config = self._sources()
        kwargs.update({'name': name})
        kwargs.setdefault('type', u'json')
        source = PersistentDict(kwargs)
        config.append(source)
        return source.get('name', '')

    def edit_source(self, key, **kwargs):
        """ Edit source properties

            >>> visualization.edit_source('http://bit.ly/rdf', a=23, b=45)
            >>> source = visualization.source('http://bit.ly/rdf')
            >>> sorted(source.items())
            [('a', 23), ('b', 45), ('name', 'http://bit.ly/rdf'), ('type'...]

        """
        source = self.source(key)
        if not source:
            raise KeyError, key
        source.update(kwargs)

    def delete_source(self, key):
        """ Delete source by given key

            >>> visualization.delete_source('http://bit.ly/rdf')
            >>> visualization.sources
            []

        """
        config = self._sources()
        for index, source in enumerate(config):
            if source.get('name', '') == key:
                config.pop(index)
                return
        raise KeyError, key

    def delete_sources(self):
        """ Remove all sources

            >>> _ = visualization.add_source('xxx')
            >>> visualization.sources
            [...'name': 'xxx'...]

            >>> visualization.delete_sources()
            >>> visualization.sources
            []

        """
        anno = IAnnotations(self.context)
        anno[ANNO_SOURCES] = PersistentList()
