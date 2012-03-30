""" Installer
"""
from setuptools import setup, find_packages
import os
from os.path import join

NAME = 'eea.app.visualization'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="Visualization API",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords=('eea app visualization daviz exhibit googlecharts'
                'sparql rdf zope plone'),
      author='European Environment Agency',
      author_email="webadmin@eea.europa.eu",
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea', 'eea.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          "python-dateutil",
          'p4a.z2utils',
          'collective.js.jqueryui',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing',]
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
