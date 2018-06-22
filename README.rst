=====================
EEA App Visualization
=====================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.app.visualization/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.app.visualization/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.app.visualization/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.app.visualization/job/master/display/redirect
  :alt: Master

`EEA App Visualization`_ is the Core API for `EEA Daviz`_. This package was added
in order to be able to use `EEA Google Charts`_ without `EEA Exhibit`_ and
viceversa or any other visualization library as a standalone visualization
or as part of a bundle package (`eea.daviz`_)


.. image:: https://eea.github.io/_images/eea.daviz.layers.svg


This package as standalone is just an API, you have to either install
`eea.daviz`_ bundle, either install one of the available visualization
libraries (`eea.exhibit`_, `eea.googlecharts`_, etc) in order to have a working
Visualization Tool for your files.


.. contents::


Installation
============

If you are using `zc.buildout`_ and the `plone.recipe.zope2instance`_
recipe to manage your project, you can do this:

* Update your buildout.cfg file:

  - Add `eea.app.visualization`_ to the list of eggs to install
  - Tell the plone.recipe.zope2instance recipe to install a ZCML slug

  ::

    [instance]
    recipe = plone.recipe.zope2instance
    eggs = eea.app.visualization
    zcml = eea.app.visualization

* Re-run buildout, e.g. with

  ::

    $ ./bin/buildout


You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.


Dependencies
============

* python-dateutil
* plone.i18n
* Zope >= 2.12
* eea.jquery
* collective.js.jqueryui < 1.9 (Plone 4.0, 4.1, 4.2)
* collective.js.jqueryui > 1.9 (Plone 4.3+)
* eea.cache > 7.0 (optional)

.. image:: https://eea.github.io/_images/eea.daviz.dependencies.svg


Live demo
=========

1. http://www.simile-widgets.org/exhibit
2. Exhibit only: http://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-3/national-total-excluding-lulucf/ghg_v10_extract.csv
3. http://code.google.com/apis/chart/


Source code
===========

Latest source code (Zope 2 compatible):
- `Plone Collective on Github <https://github.com/collective/eea.app.visualization>`_
- `EEA on Github <https://github.com/eea/eea.app.visualization>`_


Copyright and license
=====================

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA App Visualization (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Links
=====

1. Simile Wiki - Exhibit 2.0: http://simile.mit.edu/wiki/Exhibit
2. Simile widgets: http://www.simile-widgets.org/exhibit
3. EEA Daviz howto: https://taskman.eionet.europa.eu/projects/zope/wiki/HowToDaviz
4. EEA Daviz backlog wiki: https://taskman.eionet.europa.eu/projects/zope/wiki/DaViz
5. Google charts: http://code.google.com/apis/chart/


Funding
=======

EEA_ - European Environment Agency (EU)


.. _EEA: https://www.eea.europa.eu/
.. _`EEA Daviz`: https://eea.github.io/docs/eea.daviz
.. _`EEA Google Charts`: https://eea.github.io/docs/eea.googlecharts
.. _`EEA Exhibit`: https://eea.github.io/docs/eea.exhibit
.. _`eea.daviz`: https://eea.github.io/docs/eea.daviz
.. _`eea.googlecharts`: https://eea.github.io/docs/eea.googlecharts
.. _`eea.exhibit`: https://eea.github.io/docs/eea.exhibit
.. _`eea.app.visualization`: https://eea.github.io/docs/eea.app.visualization
.. _`plone.recipe.zope2instance`: https://pypi.python.org/pypi/plone.recipe.zope2instance
.. _`zc.buildout`: https://pypi.python.org/pypi/zc.buildout
.. _`EEA App Visualization`: https://eea.github.io/docs/eea.app.visualization
