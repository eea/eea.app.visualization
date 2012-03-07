=============================
EEA App Visualisation product
=============================
EEA App Visualisation is the Core API for EEA Daviz. This package was added
in order to be able to use EEA Google Charts without EEA Exhibit and viceversa or
any other visualization library as a standalone visualization or as part of a
bundle package (eea.daviz)


The following graph show the arhitecture of EEA Visualisation::

  -------------------------------------------------------------------------
 |                           eea.daviz                                     | - Bundle
  -------------------------------------------------------------------------
       /                          |                           \
  -------------+------------------+----------------------------------------
 | eea.exhibit | eea.googlecharts | ...more custom visualization libraries | - Pluggable visualization libraries
  -------------+------------------+----------------------------------------
       \                          |                           /
  -------------------------------------------------------------------------
 |                       eea.app.visualization                             | - API
  -------------------------------------------------------------------------


This package as standalone is just an API, you have to either install
eea.daviz bundle, either install one of the available visualization
libraries (eea.exhibit, eea.googlecharts, etc) in order to have a working
Visualization Tool for your files.


Contents
========

.. contents::


Installation
============

If you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

  * Add ``eea.app.visualization`` to the list of eggs to install, e.g.::

      [buildout]
      eggs = eea.app.visualization

  * Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

      [instance]
      recipe = plone.recipe.zope2instance
      zcml = eea.app.visualization

  * Re-run buildout, e.g. with::

      $ ./bin/buildout

You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.


Dependecies
===========

  1. Plone 4.x

Live demo
=========

  1. http://www.simile-widgets.org/exhibit
  2. Exhibit only: http://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-3/national-total-excluding-lulucf/ghg_v10_extract.csv
  3. http://code.google.com/apis/chart/


Source code
===========

Latest source code (Plone 4 compatible):
   https://svn.eionet.europa.eu/repositories/Zope/trunk/eea.app.visualization/trunk


Copyright and license
=====================

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA App Visualisation (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Links
=====

  1. Simile Wiki - Exhibit 2.0: http://simile.mit.edu/wiki/Exhibit
  2. Simile widgets: http://www.simile-widgets.org/exhibit
  3. EEA Daviz howto: https://svn.eionet.europa.eu/projects/Zope/wiki/HowToDaviz
  4. EEA Daviz backlog wiki: https://svn.eionet.europa.eu/projects/Zope/wiki/DaViz
  5. Google charts: http://code.google.com/apis/chart/

Funding
=======

  EEA_ - European Enviroment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
