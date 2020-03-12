[![PyPI version](https://badge.fury.io/py/fbc_curation.svg)](https://badge.fury.io/py/fbc_curation)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Ffbc_curation.svg)](https://badge.fury.io/gh/matthiaskoenig%2Ffbc_curation)
[![Build Status](https://travis-ci.org/matthiaskoenig/fbc_curation.svg?branch=develop)](https://travis-ci.org/matthiaskoenig/fbc_curation)
[![codecov](https://codecov.io/gh/matthiaskoenig/fbc_curation/branch/develop/graph/badge.svg)](https://codecov.io/gh/matthiaskoenig/fbc_curation)
[![License (LGPL version 3)](https://img.shields.io/badge/license-LGPLv3.0-blue.svg?style=flat-square)](http://opensource.org/licenses/LGPL-3.0)

# fbc_curation
<b>Matthias König</b>  
This repository creates standard files for FBC curation based on cobrapy.

## Reference output
### 01 Objective value
The objective value file contains the objective value if the model is optimized with the default settings. The file only contains the objective value.
```
0.873921507
```

### 02 Flux variability analysis (FVA)
The flux variability analysis results contain the SBML reaction identifiers and the minimum and maximum values of the FVA. The file is a tab separated file (TSV) with the columns `reaction`, `minimum` and `maximum`.
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

### 03 Gene deletions 
The gene deletions results contain the SBML reaction identifiers and the minimum and maximum values of the FVA. The file is a tab separated file (TSV) with the columns `gene`, `value` and `status`. The status is either `optimal` or `infeasible`. In case of `infeasible` solution no value is provided.
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

### 04 Reaction deletions 
The gene deletions results contain the SBML reaction identifiers and the minimum and maximum values of the FVA. The file is a tab separated file (TSV) with the columns `reaction`, `value` and `status`. The status is either `optimal` or `infeasible`. In case of `infeasible` solution no value is provided.
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

## Installation

Create virtual environment
```bash
pip install virtualenv virtualenvwrapper
mkvirtualenv fbc_curation --python=python3.7
```

Install `fbc_curation` package
```
git clone https://github.com/matthiaskoenig/fbc_curation.git
cd fbc_curation
pip install -e .
```

## Testing
To run the tests use
```
pytest
```

## Examples
To run the examples use
```
python fbc_curation/examples.py
```

## Curation files
To create FBC curation for a new model use:
```
python fbc_curation/fbc_files.py --model ./examples/models/e_coli_core.xml --out ./examples/results 
```
This creates the FBC curation files for the model in the output folder.

### License
* Source Code: [LGPLv3](http://opensource.org/licenses/LGPL-3.0)
* Documentation: [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)

### Funding
Matthias König is supported by the Federal Ministry of Education and Research (BMBF, Germany)
within the research network Systems Medicine of the Liver (**LiSyM**, grant number 031L0054).

