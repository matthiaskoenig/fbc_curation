fbc_curation
=============

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
available from https://github.com/matthiaskoenig/fbc_curation.

How to cite
===========
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3708271.svg
   :target: https://doi.org/10.5281/zenodo.3597770
   :alt: Zenodo DOI

License
=======

* Source Code: `LGPLv3 <http://opensource.org/licenses/LGPL-3.0>`__
* Documentation: `CC BY-SA 4.0 <http://creativecommons.org/licenses/by-sa/4.0/>`__

The sbmlsim source is released under both the GPL and LGPL licenses version 2 or
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
within the research network Systems Medicine of the Liver (**LiSyM**, grant number 031L0054).

Installation
============
`sbmlsim` is available from `pypi <https://pypi.python.org/pypi/sbmlsim>`__ and
can be installed via::

    pip install sbmlsim

Requirements
------------

HDF5 support is required which can be installed on linux via::

    sudo apt-get install -y libhdf5-serial-dev

Develop version
---------------
The latest develop version can be installed via::

    pip install git+https://github.com/matthiaskoenig/sbmlsim.git@develop

Or via cloning the repository and installing via::

    git clone https://github.com/matthiaskoenig/sbmlsim.git
    cd sbmlsim
    pip install -e .

To install for development use::

    pip install -e .[development]
    


© 2020 Matthias König
