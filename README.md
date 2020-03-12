[![PyPI version](https://badge.fury.io/py/fbc-curation.svg)](https://badge.fury.io/py/fbc-curation)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Ffbc_curation.svg)](https://badge.fury.io/gh/matthiaskoenig%2Ffbc_curation)
[![Build Status](https://travis-ci.org/matthiaskoenig/fbc_curation.svg?branch=develop)](https://travis-ci.org/matthiaskoenig/fbc_curation)
[![codecov](https://codecov.io/gh/matthiaskoenig/fbc_curation/branch/develop/graph/badge.svg)](https://codecov.io/gh/matthiaskoenig/fbc_curation)
[![License (LGPL version 3)](https://img.shields.io/badge/license-LGPLv3.0-blue.svg?style=flat-square)](http://opensource.org/licenses/LGPL-3.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3708271.svg)](https://doi.org/10.5281/zenodo.3708271)

# fbc_curation
<b>Matthias König</b>  
This repository creates standard files for FBC curation based on cobrapy.

## Reference output
In the following the reference outputs are described for the [`e_coli_core.xml`](../examples/e_coli_core.xml) model.

### 01 Objective value
The objective value file contains the objective value if the model is optimized with the default settings. The file only contains the objective value.
```
0.873921507
```
See for instance: [`e_coli_core_01_objective.tsv`](../results/e_coli_core_01_objective.tsv)

### 02 Flux variability analysis (FVA)
The flux variability analysis results contain the SBML reaction identifiers and the minimum and maximum values of the FVA. The file is a tab separated file (TSV) with the three columns `reaction`, `minimum` and `maximum`.
```
reaction	minimum	maximum
ACALD	0.0	0.0
ACALDt	0.0	0.0
ACKr	0.0	0.0
ACONTa	6.0072495754	6.0072495754
ACONTb	6.0072495754	6.0072495754
ACt2r	0.0	0.0
ADK1	0.0	0.0
AKGDH	5.0643756615	5.0643756615
...
```
See for instance: [`e_coli_core_02_fva.tsv`](../results/e_coli_core_02_fva.tsv)

### 03 Gene deletions 
The gene deletions results contain the SBML reaction identifiers, the optimal value under the given gene deletion and the status of the optimization. The file is a tab separated file (TSV) with the three columns `gene`, `value` and `status`. The status can be either `optimal` or `infeasible`. In case of an `infeasible` status no solution could be found and no optimal value is provided.
```
gene	value	status
b0008	0.873921507	optimal
b0114	0.7966959254	optimal
b0115	0.7966959254	optimal
b0116	0.7823510529	optimal
b0118	0.873921507	optimal
b0351	0.873921507	optimal
b2415		infeasible
b2416		infeasible
b2417	0.873921507	optimal
b2458	0.873921507	optimal
...
```
See for instance: [`e_coli_core_03_gene_deletion.tsv`](../results/03_gene_deletion.tsv)

### 04 Reaction deletions 
The gene deletions results contain the SBML reaction identifiers, the optimal value under the given gene deletion and the status of the optimization. The file is a tab separated file (TSV) with the three columns `reaction`, `value` and `status`. In case of an `infeasible` status no solution could be found and no optimal value is provided.
```
reaction	value	status
ACALD	0.873921507	optimal
ACALDt	0.873921507	optimal
ACKr	0.873921507	optimal
ACONTa	0.0	optimal
ACONTb	0.0	optimal
ACt2r	0.873921507	optimal
ADK1	0.873921507	optimal
AKGDH	0.858307408	optimal
...
```
See for instance: [`e_coli_core_04_reaction_deletion.tsv`](../results/04_reaction_deletion.tsv)

## Installation

The `fbc_curation` package can be installed via pip. 
```bash
pip install fbc_curation
```
To upgrade use
```bash
pip install fbc_curation --upgrade
```
To install the latest develop version use 
```bash
pip install git+https://github.com/matthiaskoenig/fbc_curation.git#egg=fbc-curation
```

## Usage
To create FBC curation files for a given SBML model use the `fbc_curation` command line tool:
```bash
Usage: fbc_curation [options]

Options:
  -h, --help            show this help message and exit
  -m MODEL_PATH, --model=MODEL_PATH
                        path to SBML model with fbc information
  -o OUTPUT_PATH, --out=OUTPUT_PATH
                        path to write the output to

```
For instance for the `e_coli_core.xml` example use
```
fbc_curation --model ./examples/models/e_coli_core.xml --out ./examples/results 
```
This creates the FBC curation files for the model in the output folder.

## Examples
The examples can be run via
```
fbc_curation_examples
```

## Testing
To run the tests clone the repository
```
git clone https://github.com/matthiaskoenig/fbc_curation.git
cd fbc_curation
pip install -e .
pytest
```

## License
* Source Code: [LGPLv3](http://opensource.org/licenses/LGPL-3.0)
* Documentation: [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)

## Funding
Matthias König is supported by the Federal Ministry of Education and Research (BMBF, Germany)
within the research network Systems Medicine of the Liver (**LiSyM**, grant number 031L0054).

## Changelog
### v0.0.2
- improved documentation
- commands added

### v0.0.1
- initial release
- create first version of files