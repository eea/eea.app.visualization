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
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='EEA app visualization Add-ons Plone Zope',
      author='European Environment Agency: IDM2 A-Team',
      author_email="eea-edw-a-team-alerts@googlegroups.com",
      download_url="https://pypi.python.org/pypi/eea.app.visualization",
      url='https://github.com/collective/eea.app.visualization',
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
              'zope.formlib',
          ]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
