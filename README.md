[![PyPI version](https://badge.fury.io/py/fbc-curation.svg)](https://badge.fury.io/py/fbc-curation)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Ffbc_curation.svg)](https://badge.fury.io/gh/matthiaskoenig%2Ffbc_curation)
[![Build Status](https://travis-ci.org/matthiaskoenig/fbc_curation.svg?branch=develop)](https://travis-ci.org/matthiaskoenig/fbc_curation)
[![codecov](https://codecov.io/gh/matthiaskoenig/fbc_curation/branch/develop/graph/badge.svg)](https://codecov.io/gh/matthiaskoenig/fbc_curation)
[![License (LGPL version 3)](https://img.shields.io/badge/license-LGPLv3.0-blue.svg?style=flat-square)](http://opensource.org/licenses/LGPL-3.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3708271.svg)](https://doi.org/10.5281/zenodo.3708271)

# fbc_curation
<b>Matthias König</b>  
This repository creates standardized reference files for a given FBC model based on cobrapy and glpk. These files can be used in the model curation process for validating the model behavior. The format of the standardized reference files is described below. 

`fbc_curation` is a python package which can be included in python applications. In addition a command line tool is provided which allows easy usage outside of python. 

## Usage
To create FBC curation files for a given SBML model use the `fbc_curation` command line tool. The reference files are created for the provided objective in the model, if no objective is provided the `active` objective or default objective is used.
```bash
    __________  ______   ________  ______  ___  ______________  _   __
   / ____/ __ )/ ____/  / ____/ / / / __ \/   |/_  __/  _/ __ \/ | / /
  / /_  / __  / /      / /   / / / / /_/ / /| | / /  / // / / /  |/ / 
 / __/ / /_/ / /___   / /___/ /_/ / _, _/ ___ |/ / _/ // /_/ / /|  /  
/_/   /_____/\____/   \____/\____/_/ |_/_/  |_/_/ /___/\____/_/ |_/   
                                                                      

        Version 0.1.0a1 (https://github.com/matthiaskoenig/fbc_curation)
        Citation https://doi.org/10.5281/zenodo.3708271

Required argument '--model' missing
Usage: fbc_curation [options]

Options:
  -h, --help            show this help message and exit
  -m MODEL_PATH, --model=MODEL_PATH
                        (required) path to SBML model with fbc information
  -p OUTPUT_PATH, --path=OUTPUT_PATH
                        (required) directory path to write output files to
  -c CURATOR, --curator=CURATOR
                        (optional) curator tool to create reference files:
                        Select from ['cobrapy', 'cameo', 'all']
  -o OBJECTIVE, --objective=OBJECTIVE
                        (optional) objective to use in optimization, defaults
                        to active objective
```
For instance for the `e_coli_core.xml` example use
```
fbc_curation --model ./fbc_curation/examples/models/e_coli_core.xml --path ./fbc_curation/examples/results/e_coli_core 
```
This creates the FBC curation files for the model in the output folder.

## Standardized reference files
In the following the created reference output files are described and examples provided for the [`e_coli_core.xml`](examples/models/e_coli_core.xml) model. All output files are tab separated files (TSV) with the first three columns being `model`, `objective`, and `status`. The column `model` encodes the SBML model id. The column `objective` encodes the SBML objective id, which is the objective which was optimized in the respective simulation. The column `status` encodes the status of the simulation. The status can be either `optimal` (optimization worked) or `infeasible` (no solution found or problem in simulation).  

### 01 Objective value
The objective value file `01_objective.tsv` contains the four columns with the headers `model`, `objective` and `status`, `value`. The `value` is the optimal value of the respective objective function when the model is optimized with default settings. If the status is `infeasible` the value is `NA`.
```
model	objective	status	value
e_coli_core	obj	optimal	0.87392151
```
See for instance: [`e_coli_core/01_objective.tsv`](examples/results/e_coli_core/01_objective.tsv). For more information: https://cobrapy.readthedocs.io/en/latest/simulating.html

### 02 Flux variability analysis (FVA)
The FVA file `02_fva.tsv` contains five columns with the headers `model`, `objective`, `reaction`, `status`, `minimum` and `maximum`. The `minimum` and `maximum` columns contain the minimum and maximum values of the FVA. The rows are sorted based on reaction identifier. The `status` contains the status of the optimization (`optimal` or `infeasible`). If the status is `infeasible` the value is `NA`.
Flux variability is calculated with `fraction_of_optimum = 1.0`, i.e. the objective of the model is set to its maximum in the single
optimization.
```
model	objective	reaction	status	minimum	maximum
e_coli_core	obj	ACALD	optimal	0.0	0.0
e_coli_core	obj	ACALDt	optimal	0.0	0.0
e_coli_core	obj	ACKr	optimal	0.0	0.0
e_coli_core	obj	ACONTa	optimal	6.00724958	6.00724958
e_coli_core	obj	ACONTb	optimal	6.00724958	6.00724958
e_coli_core	obj	ACt2r	optimal	0.0	0.0
e_coli_core	obj	ADK1	optimal	0.0	0.0
e_coli_core	obj	AKGDH	optimal	5.06437566	5.06437566
...
```
See for instance: [`e_coli_core/02_fva.tsv`](examples/results/e_coli_core/02_fva.tsv). For more information: https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA

### 03 Gene deletions 
The gene deletion file `03_gene_deletion.tsv` contains five columns with the headers `model`, `objective`, `gene`, `status` and `value`. 
The `gene` column contains the SBML gene identifiers. The `status` and `value` columns contain the status of the optimization (`optimal` or `infeasible`) and optimal value under the given gene deletion. If the status is `infeasible` the value is `NA`. The rows are sorted based on gene identifier.
```
model	objective	gene	status	value
e_coli_core	obj	b0008	optimal	0.87392151
e_coli_core	obj	b0114	optimal	0.79669593
e_coli_core	obj	b0115	optimal	0.79669593
e_coli_core	obj	b0116	optimal	0.78235105
e_coli_core	obj	b0118	optimal	0.87392151
e_coli_core	obj	b0351	optimal	0.87392151
...
e_coli_core	obj	b2415	infeasible	NA
e_coli_core	obj	b2416	infeasible	NA
...
```
See for instance: [`e_coli_core/03_gene_deletion.tsv`](examples/results/e_coli_core/03_gene_deletion.tsv). For more information: https://cobrapy.readthedocs.io/en/latest/deletions.html

### 04 Reaction deletions 
The reaction deletion file `04_reaction_deletion.tsv` contains five columns with the headers `model`, `objective`, `reaction`, `status` and `value`. 
The `reaction` column contains the SBML reaction identifiers. The `status` and `value` columns contain the status of the optimization (`optimal` or `infeasible`) and optimal value under the given reaction deletion. If the status is `infeasible` the value is `NA`. The rows are sorted based on reaction identifier.
```
model	objective	reaction	status	value
e_coli_core	obj	ACALD	optimal	0.87392151
e_coli_core	obj	ACALDt	optimal	0.87392151
e_coli_core	obj	ACKr	optimal	0.87392151
e_coli_core	obj	ACONTa	optimal	0.0
e_coli_core	obj	ACONTb	optimal	0.0
e_coli_core	obj	ACt2r	optimal	0.87392151
e_coli_core	obj	ADK1	optimal	0.87392151
e_coli_core	obj	AKGDH	optimal	0.85830741
...
```
See for instance: [`e_coli_core/04_reaction_deletion.tsv`](examples/results/e_coli_core/04_reaction_deletion.tsv). For more information: https://cobrapy.readthedocs.io/en/latest/deletions.html

## Installation

The `fbc_curation` package can be installed via pip. 
```bash
pip install fbc_curation
```
After pip installation the `fbc_curation` command line tool is available.

To upgrade use
```bash
pip install fbc_curation --upgrade
```
To install the latest develop version use 
```bash
pip install git+https://github.com/matthiaskoenig/fbc_curation.git#egg=fbc-curation
```

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

## Example models
Example models are from the [BiGG Database](http://bigg.ucsd.edu/)

King ZA, Lu JS, Dräger A, Miller PC, Federowicz S, Lerman JA, Ebrahim A, Palsson BO, and Lewis NE. BiGG Models: A platform for integrating, standardizing, and sharing genome-scale models (2016) Nucleic Acids Research 44(D1):D515-D522. doi:10.1093/nar/gkv1049

## Changelog
### v0.1.0
- result validation against schema
- second solver implementation (cameo)
- improved user interface and documentation

### v0.0.6
- fixed fbc_curation_example bug #11
- reproducible tolerances for examples

### v0.0.5
- major refactoring
- handling solver exceptions
- improved file format & naming
- support for additional models
- minimal support for multiple objective functions

### v0.0.4
- package data fix & cleanup

### v0.0.3
- bugfixes
- example data included in package
- licenses and references added

### v0.0.2
- improved documentation
- commands added

### v0.0.1
- initial release
- create first version of files