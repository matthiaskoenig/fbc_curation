.. image:: https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/docs/images/icon/frog_icon_mirror-100x80-300dpi.png
   :align: left
   :alt: FROG logo

fbc_curation: FROG analysis in Python
=====================================

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


The project :code:`fbc_curation` implements the FROG analysis for reproducibility of constraint-based models in Python.
FROG can be run 

* programmatically in python
* using the :code:`runfrog` command line tool available in this package
* via the website `https://runfrog.de <https://runfrog.de>`__
* via the REST API `https://runfrog.de/docs <https://runfrog.de/docs>`__

The FROG analysis creates standardized reference files for a given constraint-based computational model. 
The FROG files can be used in the model curation process for validating the model behavior, e.g., when
submitting the model to `BioModels <https://www.ebi.ac.uk/biomodels/curation/fbc>`__. 
The latest version supports 

.. image:: https://img.shields.io/pypi/pyversions/fbc-curation.svg
   :target: https://pypi.org/project/fbc_curation/
   :alt: Supported Python Versions

:code:`fbc_curation` provides two implementations of FROG using

* `cobrapy <https://github.com/opencobra/cobrapy>`__ based on COBRApy (Constraint-Based Reconstruction and Analysis in Python)
* `cameo <https://github.com/biosustain/cameo>`__ cameo based on Cameo (Computer Aided Metabolic Engineering and Optimization)

For more information see the following resources

* **Documentation**: `https://fbc-curation.readthedocs.io <https://fbc-curation.readthedocs.io>`__
* **Website**: `https://runfrog.de <https://runfrog.de>`__
* **REST API**: `https://runfrog.de/docs <https://runfrog.de/docs>`__
* **FROG format**: `FROG version 1 <https://fbc-curation.readthedocs.io/en/latest/reference_files.html>`__
* **FROG JSON schema**: `frog-schema-version-1.json <https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/resources/schema/frog-schema-version-1.json>`__.
* **Code**: `https://github.com/matthiaskoenig/fbc_curation <https://github.com/matthiaskoenig/fbc_curation>`_
* **FROG BioModels submission**: `https://www.ebi.ac.uk/biomodels/curation/fbc <https://www.ebi.ac.uk/biomodels/curation/fbc>`__.

If you have any questions or issues please `open an issue <https://github.com/matthiaskoenig/fbc_curation/issues>`__. 

How to cite
===========
If you use :code:`fbc_curation` or :code:`runfrog` please cite us via

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3708271.svg
   :target: https://doi.org/10.5281/zenodo.3597770
   :alt: Zenodo DOI

Installation
============
``fbc_curation`` is available from `pypi <https://pypi.python.org/pypi/fbc-curation>`__ and
can be installed via::

    pip install fbc-curation

The latest develop version can be installed via::

    pip install git+https://github.com/matthiaskoenig/fbc-curation.git@develop


Run FROG
========

Command line tool
-----------------

After installation FROG analysis can be performed using the :code:`runfrog` command line tool

.. code:: bash

    $ runfrog
    
    ──────────────────────────────────────────────────────────────────────────────────
    🐸 FBC CURATION FROG ANALYSIS 🐸
    Version 0.2.0 (https://github.com/matthiaskoenig/fbc_curation)
    Citation https://doi.org/10.5281/zenodo.3708271
    ──────────────────────────────────────────────────────────────────────────────────
    Usage: runfrog [options]
    
    Options:
      -h, --help            show this help message and exit
      -i INPUT_PATH, --input=INPUT_PATH
                            (required) path to COMBINE archive (OMEX) with SBML
                            model or an SBML model
      -o OUTPUT_PATH, --output=OUTPUT_PATH
                            (required) omex output path to write FROG
    ──────────────────────────────────────────────────────────────────────────────────

Website
-------
FROG can be easily executed via the website `https://runfrog.de <https://runfrog.de>`__

REST API
--------
FROG can be execute via the REST API `https://runfrog.de/docs <https://runfrog.de/docs>`__

Python
------
To run FROG programmatically via python see the following example

.. code:: python

    """FROG example using `fbc_curation`."""
    from pathlib import Path
    
    from fbc_curation.compare import FrogComparison
    from fbc_curation.worker import frog_task
    
    
    def create_frog(model_path: Path, omex_path: Path) -> None:
        """Creates FROG report and writes OMEX for given model."""
    
        # create FROG in OMEX
        frog_task(
            source_path_str=str(model_path),
            input_is_temporary=False,
            omex_path_str=str(omex_path),
        )
    
        # compare FROG results in OMEX
        model_reports = FrogComparison.read_reports_from_omex(omex_path=omex_path)
        for _, reports in model_reports.items():
            FrogComparison.compare_reports(reports=reports)
    
    
    if __name__ == "__main__":
        base_path = Path(".")
        create_frog(
            model_path=base_path / "e_coli_core.xml",
            omex_path=base_path / "e_coli_core_FROG.omex"
        )

The typically output of a FROG analyis is depicted below

.. code:: bash

    INFO     Loading 'e_coli_core.xml'                                    worker.py:44
    WARNING  Omex path 'e_coli_core.xml' is not a zip archive.             omex.py:487
    ────────────────────────────── FROG CuratorCobrapy ───────────────────────────────
    INFO     * metadata                                                 curator.py:107
    INFO     * objectives                                               curator.py:110
    Scaling...
     A: min|aij| =  1.000e+00  max|aij| =  1.000e+00  ratio =  1.000e+00
    Problem data seem to be well scaled
    INFO     * fva                                                      curator.py:113
    INFO     * reactiondeletions                                        curator.py:116
    INFO     * genedeletions                                            curator.py:119
    INFO     FROG created in '0.86' [s]                                  worker.py:144
    ─────────────────────────────── FROG CuratorCameo ────────────────────────────────
    INFO     * metadata                                                 curator.py:107
    INFO     * objectives                                               curator.py:110
    INFO     * fva                                                      curator.py:113
    INFO     * reactiondeletions                                        curator.py:116
    INFO     * genedeletions                                            curator.py:119
    INFO     FROG created in '1.14' [s]                                  worker.py:144
    ─────────────────────────────────── Write OMEX ───────────────────────────────────
    WARNING  Existing omex is overwritten: 'e_coli_core_FROG.omex'         omex.py:667
    INFO     Reports in omex:                                            compare.py:60
             {'./model.xml': ['cobrapy', 'cobrapy_tsv', 'cameo',                      
             'cameo_tsv']}                                                            
    ─────────────────────────── Comparison of FROGReports ────────────────────────────
    --- objective ---
                 cobrapy  cobrapy_tsv  cameo  cameo_tsv
    cobrapy            1            1      1          1
    cobrapy_tsv        1            1      1          1
    cameo              1            1      1          1
    cameo_tsv          1            1      1          1
    --- fva ---
                 cobrapy  cobrapy_tsv  cameo  cameo_tsv
    cobrapy            1            1      1          1
    cobrapy_tsv        1            1      1          1
    cameo              1            1      1          1
    cameo_tsv          1            1      1          1
    --- reaction_deletion ---
                 cobrapy  cobrapy_tsv  cameo  cameo_tsv
    cobrapy            1            1      1          1
    cobrapy_tsv        1            1      1          1
    cameo              1            1      1          1
    cameo_tsv          1            1      1          1
    --- gene_deletion ---
                 cobrapy  cobrapy_tsv  cameo  cameo_tsv
    cobrapy            1            1      1          1
    cobrapy_tsv        1            1      1          1
    cameo              1            1      1          1
    cameo_tsv          1            1      1          1
    ──────────────────────────────────────────────────────────────────────────────────
    Equal: True
    ──────────────────────────────────────────────────────────────────────────────────

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
A Systems Medicine Approach)" by grant number 436883643 and by grant number 465194077 
(Priority Programme SPP 2311, Subproject SimLivA). 

© 2020-2022 Matthias König
