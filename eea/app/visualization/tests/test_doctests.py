""" Doc tests
"""
import doctest
import unittest
from eea.app.visualization.tests.base import FUNCTIONAL_TESTING
from plone.testing import layered

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'README.txt',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/converter.txt',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/converter.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'storage/handler.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/url.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/boolean.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/latitude.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/longitude.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/latlong.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/number.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/year.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/date.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/text.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/guess.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/types/list.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'data/source.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'data/internal.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'data/external.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'converter/data.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'browser/app/download.py',
                optionflags=OPTIONFLAGS,
                package='eea.app.visualization'),
            layer=FUNCTIONAL_TESTING),
    ])
    return suite
