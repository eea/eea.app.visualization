""" Installer
"""
import os
from setuptools import setup, find_packages

NAME = 'eea.app.visualization'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="Visualization API",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
        ],
      keywords=('eea app visualization daviz exhibit googlecharts '
                'sparql rdf zope plone'),
      author='European Environment Agency',
      author_email="webadmin@eea.europa.eu",
      maintainer='Alin Voinea (Eau de Web)',
      maintainer_email='alin@eaudeweb.ro',
      download_url="http://pypi.python.org/pypi/eea.app.visualization",
      url='http://eea.github.com/docs/eea.app.visualization',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea', 'eea.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          "python-dateutil",
          'plone.i18n',
          'z3c.autoinclude',
          'eea.jquery >= 6.3',
          'eventlet',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              ],
          'zope2': [
              #'plone.i18n',
              #'z3c.autoinclude',
          ]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
