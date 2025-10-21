# fbc_curation: FROG analysis in Python

<img src="https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/docs/images/icon/frog_icon_mirror-100x80-300dpi.png" alt="FROG logo" align="left" width="100" />

[![CI/CD](https://github.com/matthiaskoenig/sbmlsim/workflows/CI-CD/badge.svg)](https://github.com/matthiaskoenig/fbc_curation/workflows/CI-CD)
[![PyPI Version](https://img.shields.io/pypi/v/fbc-curation.svg)](https://pypi.org/project/fbc_curation/)
[![Python Versions](https://img.shields.io/pypi/pyversions/fbc-curation.svg)](https://pypi.org/project/fbc_curation/)
[![License: MIT](https://img.shields.io/pypi/l/fbc-curation.svg)](http://opensource.org/licenses/MIT)
[![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3708271.svg)](https://doi.org/10.5281/zenodo.3708271)

The project `fbc_curation` implements the FROG analysis for reproducibility of constraint-based models in Python. FROG can be run

- programmatically in Python
- using the `runfrog` command line tool available in this package
- via the website <https://runfrog.de>
- via the REST API <https://runfrog.de/docs>

The FROG analysis creates standardized reference files for a given constraint-based computational model. The FROG files can be used in the model curation process for validating model behavior, e.g., when submitting the model to [BioModels](https://www.ebi.ac.uk/biomodels/curation/fbc).

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/fbc-curation.svg)](https://pypi.org/project/fbc_curation/)

`fbc_curation` provides two implementations of FROG using

- [`cobrapy`](https://github.com/opencobra/cobrapy) — Constraint-Based Reconstruction and Analysis in Python
- [`cameo`](https://github.com/biosustain/cameo) — Computer Aided Metabolic Engineering and Optimization

For more information see the following resources:

- **Documentation**: <https://fbc-curation.readthedocs.io>
- **Website**: <https://runfrog.de>
- **REST API**: <https://runfrog.de/docs>
- **FROG format**: [FROG version 1](https://fbc-curation.readthedocs.io/en/latest/reference_files.html)
- **FROG JSON schema**: [`frog-schema-version-1.json`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/resources/schema/frog-schema-version-1.json)
- **Code**: <https://github.com/matthiaskoenig/fbc_curation>
- **FROG BioModels submission**: <https://www.ebi.ac.uk/biomodels/curation/fbc>

If you have any questions or issues please [open an issue](https://github.com/matthiaskoenig/fbc_curation/issues).

## How to cite

If you use `fbc_curation` or `runfrog` please cite us via

[![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3708271.svg)](https://doi.org/10.5281/zenodo.3597770)


## Installation

`fbc_curation` is available from [PyPI](https://pypi.python.org/pypi/fbc-curation) and can be installed via:

```bash
pip install fbc-curation
```

The latest `develop` version can be installed via:

```bash
pip install git+https://github.com/matthiaskoenig/fbc-curation.git@develop
```

## Run FROG

### Command line tool

After installation, FROG analysis can be performed using the `runfrog` command line tool:

```bash
$ runfrog

──────────────────────────────────────────────────────────────────────────────────
🐸 FBC CURATION FROG ANALYSIS 🐸
Version 0.2.1 (https://github.com/matthiaskoenig/fbc_curation)
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
```

### Website

FROG can be easily executed via the website <https://runfrog.de>.

### REST API

FROG can be executed via the REST API <https://runfrog.de/docs>.

### Python

To run FROG programmatically via Python use the `run_frog` function:

```python
from fbc_curation.worker import run_frog

run_frog(model_path, omex_path)
```

Here is a complete example with comparison of the FROG results:

```python
"""FROG example using `fbc_curation`."""
from pathlib import Path

from fbc_curation.compare import FrogComparison
from fbc_curation.worker import run_frog


def create_frog(model_path: Path, omex_path: Path) -> None:
    """Create FROG report and write OMEX for given model."""

    # create FROG and write to COMBINE archive
    run_frog(
        source_path=model_path,
        omex_path=omex_path,
    )

    # compare FROG results in created COMBINE archive
    model_reports = FrogComparison.read_reports_from_omex(omex_path=omex_path)
    for _, reports in model_reports.items():
        FrogComparison.compare_reports(reports=reports)


if __name__ == "__main__":
    base_path = Path(".")
    create_frog(
        model_path=base_path / "e_coli_core.xml",
        omex_path=base_path / "e_coli_core_FROG.omex",
    )
```

Typical output of a FROG analysis is shown below:

```bash
runfrog -i e_coli_core.xml -o e_coli_core.omex

───────────────────────────────────────────────────────────────────────────────────────
🐸 FBC CURATION FROG ANALYSIS 🐸
Version 0.2.3 (https://github.com/matthiaskoenig/fbc_curation)
Citation https://doi.org/10.5281/zenodo.3708271
───────────────────────────────────────────────────────────────────────────────────────
INFO     Loading 'e_coli_core.xml'                                         worker.py:70
WARNING  Omex path 'e_coli_core.xml' is not a zip archive.                  omex.py:500
───────────────────────────────── FROG CuratorCobrapy ────────────────────────────────
INFO     * metadata                                                      curator.py:107
INFO     * objectives                                                    curator.py:110
INFO     * fva                                                           curator.py:113
INFO     * reactiondeletions                                             curator.py:116
INFO     * genedeletions                                                 curator.py:119
INFO     FROG created in '0.977' [s]                                      worker.py:178
────────────────────────────────── FROG CuratorCameo ─────────────────────────────────
INFO     * metadata                                                      curator.py:107
INFO     * objectives                                                    curator.py:110
INFO     * fva                                                           curator.py:113
INFO     * reactiondeletions                                             curator.py:116
INFO     * genedeletions                                                 curator.py:119
INFO     FROG created in '1.219' [s]                                      worker.py:178
───────────────────────────────────── Write OMEX ─────────────────────────────────────
WARNING  Existing omex is overwritten: 'e_coli_core.omex'                   omex.py:680
INFO     Reports in omex:                                                 compare.py:60
         {'./e_coli_core.xml': ['cobrapy', 'cobrapy_tsv', 'cameo',
         'cameo_tsv']}
────────────────────────────── Comparison of FROGReports ─────────────────────────────
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
───────────────────────────────────────────────────────────────────────────────────────
Equal: True
───────────────────────────────────────────────────────────────────────────────────────
```

## License
- Source Code: [MIT](https://opensource.org/license/MIT)
- Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## Funding

Matthias König (MK) was supported by the Federal Ministry of Education and Research (BMBF, Germany) within the research network Systems Medicine of the Liver (LiSyM, grant number 031L0054). MK is supported by the Federal Ministry of Education and Research (BMBF, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA).

© 2020–2025 Matthias König
