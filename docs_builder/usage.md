# Usage

## Create reference files
To create FBC curation files for a given SBML model use the `fbc_curation` command line tool. The reference files are created for the provided objective in the model, if no objective is provided the `active` objective or default objective is used.
```bash
$ fbc_curation
    __________  ______   ________  ______  ___  ______________  _   __
   / ____/ __ )/ ____/  / ____/ / / / __ \/   |/_  __/  _/ __ \/ | / /
  / /_  / __  / /      / /   / / / / /_/ / /| | / /  / // / / /  |/ / 
 / __/ / /_/ / /___   / /___/ /_/ / _, _/ ___ |/ / _/ // /_/ / /|  /  
/_/   /_____/\____/   \____/\____/_/ |_/_/  |_/_/ /___/\____/_/ |_/   
                                                                      

        Version 0.1.0 (https://github.com/matthiaskoenig/fbc_curation)
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
  -r REFERENCE_PATH, --reference=REFERENCE_PATH
                        (optional) directory path to reference output
                        (comparison is performed)
```
For instance to create the reference files for the `e_coli_core.xml` example use
```
fbc_curation --model ./fbc_curation/examples/models/e_coli_core.xml \
--path ./fbc_curation/examples/results/e_coli_core 
```
This creates the FBC curation files for the `model` in the output `path`.

## Compare existing reference files
In addition existing reference files can be compared with the solutions by `cobrapy` and `cameo`. The `--reference` argument can be used to provide the path to the reference files.
```
curation --model examples/models/e_coli_core.xml \
--path examples/results/e_coli_core \
--reference ../examples/results/e_coli_core/cobrapy
```
The comparison results are provided as a matrix for the various reference files with `1` being equal output and `0` if differences exist between the respective reference files. If all matrices are one matrices the results are equal.
```
========================================
Comparison of results
========================================
--- objective ---
           reference  cobrapy  cameo
reference          1        1      1
cobrapy            1        1      1
cameo              1        1      1
--- fva ---
           reference  cobrapy  cameo
reference          1        1      1
cobrapy            1        1      1
cameo              1        1      1
--- gene_deletion ---
           reference  cobrapy  cameo
reference          1        1      1
cobrapy            1        1      1
cameo              1        1      1
--- reaction_deletion ---
           reference  cobrapy  cameo
reference          1        1      1
cobrapy            1        1      1
cameo              1        1      1
========================================
Equal: True
========================================
```

## Examples
The examples can be run via
```
fbc_curation_examples
```
Example models are from the [BiGG Database](http://bigg.ucsd.edu/)

King ZA, Lu JS, Dräger A, Miller PC, Federowicz S, Lerman JA, Ebrahim A, Palsson BO, and Lewis NE. BiGG Models: A platform for integrating, standardizing, and sharing genome-scale models (2016) Nucleic Acids Research 44(D1):D515-D522. doi:10.1093/nar/gkv1049
