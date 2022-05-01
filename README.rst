.. image:: https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/version-0.2.0/icon/frog_icon_mirrored.svg
   :align: left
   :alt: FROG logo


fbc_curation (FROG analysis)
============================

.. image:: https://github.com/matthiaskoenig/sbmlsim/workflows/CI-CD/badge.svg
   :target: https://github.com/matthiaskoenig/fbc_curation/workflows/CI-CD
   :alt: GitHub Actions CI/CD Status

.. image:: https://img.shields.io/pypi/v/fbc-curation.svg
   :target: https://pypi.org/project/fbc_curation/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/fbc-curation.svg
   :target: https://pypi.org/project/fbc_curation/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/fbc-curation.svg
   :target: http://opensource.org/licenses/LGPL-3.0
   :alt: GNU Lesser General Public License 3

.. image:: https://readthedocs.org/projects/fbc_curation/badge/?version=latest
   :target: https://fbc-curation.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://codecov.io/gh/matthiaskoenig/fbc_curation/branch/develop/graph/badge.svg
   :target: https://codecov.io/gh/matthiaskoenig/fbc_curation
   :alt: Codecov

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3708271.svg
   :target: https://doi.org/10.5281/zenodo.3708271
   :alt: Zenodo DOI

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black


``fbc_curation``: Reproducibility of constraint-based models
available from 
`https://github.com/matthiaskoenig/fbc_curation <https://github.com/matthiaskoenig/fbc_curation>`_.

This repository implements the FROG analysis and allows to create standardized reference files for a given FBC model based on cobrapy and glpk. These files can be used in the model curation process for validating the model behavior. The format of the standardized reference files is described below. 
Currently one implementation of the reference files is included in the package:

* ``cobrapy`` based on COBRApy (Constraint-Based Reconstruction and Analysis in Python) available from `https://github.com/opencobra/cobrapy <https://github.com/opencobra/cobrapy>`_

``fbc_curation`` is a python package which can be included in python applications. In addition a command line tool is provided which allows easy usage outside of python.

The documentation is available on `https://fbc-curation.readthedocs.io <https://fbc-curation.readthedocs.io>`__.
If you have any questions or issues please `open an issue <https://github.com/matthiaskoenig/fbc_curation/issues>`__.


Documentation
==============
.. image:: https://readthedocs.org/projects/fbc_curation/badge/?version=latest
   :target: https://fbc-curation.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

The documentation is available on `https://fbc-curation.readthedocs.io <https://fbc-curation.readthedocs.io>`__.


How to cite
===========
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3708271.svg
   :target: https://doi.org/10.5281/zenodo.3597770
   :alt: Zenodo DOI

Installation
============
``fbc_curation`` is available from `pypi <https://pypi.python.org/pypi/fbc-curation>`__ and
can be installed via::

    pip install fbc-curation


Develop version
---------------
The latest develop version can be installed via::

    pip install git+https://github.com/matthiaskoenig/fbc-curation.git@develop

Or via cloning the repository and installing via::

    git clone https://github.com/matthiaskoenig/fbc_curation.git
    cd fbc_curation
    pip install -e .

To install for development use::

    pip install -e .[development]
    
Testing
--------
To run the tests clone the repository::

    git clone https://github.com/matthiaskoenig/fbc_curation.git
    cd fbc_curation
    pip install -e .
    pytest


License
=======

* Source Code: `LGPLv3 <http://opensource.org/licenses/LGPL-3.0>`__
* Documentation: `CC BY-SA 4.0 <http://creativecommons.org/licenses/by-sa/4.0/>`__

The ``fbc_curation`` source is released under both the GPL and LGPL licenses version 2 or
later. You may choose which license you choose to use the software under.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License or the GNU Lesser General Public
License as published by the Free Software Foundation, either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

Funding
=======
Matthias König is supported by the Federal Ministry of Education and Research (BMBF, Germany)
within the research network Systems Medicine of the Liver (**LiSyM**, grant number 031L0054) 
and by the German Research Foundation (DFG) within the Research Unit Programme FOR 5151 
"`QuaLiPerF <https://qualiperf.de>`__ (Quantifying Liver Perfusion-Function Relationship in Complex Resection - 
A Systems Medicine Approach)" by grant number 436883643.

© 2020-2022 Matthias König
