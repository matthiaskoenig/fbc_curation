# FROG files
In the following the four created reference files and the metadata file are described and examples provided for the [`e_coli_core.xml`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/examples/models/e_coli_core.xml) model. All output files are tab separated files (TSV) with the first three columns being `model`, `objective`, and `status`. The column `model` encodes the SBML model id. The column `objective` encodes the SBML objective id, which is the objective which was optimized in the respective simulation. The column `status` encodes the status of the simulation. The status can be either `optimal` (optimization worked) or `infeasible` (no solution found or problem in simulation).  

## Metadata file
A required metadata file `metadata.json` encodes information about the curation run and the used software and library. The information is documented at the JSON schema `frog-schema-version-1.json <https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/resources/schema/frog-schema-version-1.json>`__

The following fields are required:

- `software.name` (required): software used to create the reference files,
- `software.version` (required): software version
- `model.location` (required): SBML model filename
- `solver.name` (required): solver used for optimization,
- `solver.version` (required): solver version

A concrete example of the metadata is shown below
```
{
  "model_location": "./e_coli_core.xml",
  "model_md5": "4574760460afe9e1b3388dc15f354706",
  "frog_id": "cobrapy_tsv",
  "frog_software": {
    "name": "fbc_curation",
    "version": "0.2.2",
    "url": "https://doi.org/10.5281/zenodo.3708271"
  },
  "curators": [],
  "software": {
    "name": "cobrapy",
    "version": "0.26.0",
    "url": "https://github.com/opencobra/cobrapy"
  },
  "solver": {
    "name": "glpk",
    "version": "5.0",
    "url": null
  },
  "environment": "posix, Linux, 5.15.0-53-generic"
}
```
See [`e_coli_core/metadata.json`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/examples/results/e_coli_core/cobrapy/metadata.json).

## 01 Objective value
The objective value file `01_objective.tsv` contains the four columns with the headers `model`, `objective`, `status`, and `value`. The `model` column stores the SBML model filename. 
The `value` is the optimal value of the respective objective function when the model is optimized. If the status is `infeasible`, no value is provided, i.e., the value is empty.
```
model	objective	status	value
./e_coli_core.xml	obj	optimal	0.8739215069684295
```
For an example file see [`e_coli_core/01_objective.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/examples/results/e_coli_core/cobrapy/01_objective.tsv). For more information on how to simulate the FBA see [https://cobrapy.readthedocs.io/en/latest/simulating.html](https://cobrapy.readthedocs.io/en/latest/simulating.html).

## 02 Flux variability analysis (FVA)
The FVA file `02_fva.tsv` contains six columns with the headers `model`, `objective`, `reaction`, `flux`, `status`, `minimum` and `maximum`. The `model` column stores the SBML model filename. The `reaction` column stores the SBML reaction id. The `minimum` and `maximum` columns contain the minimum and maximum values of the FVA. The rows are sorted based on the SBML reaction identifier. The `status` contains the status of the optimization (`optimal` or `infeasible`). If the status is `infeasible` the value is empty.
Flux variability is calculated with `fraction_optimum = 1.0`, i.e. the objective of the model is set to its maximum in secondary optimization (percent of optimum is 100%). The `flux` column stores the reference flux through the objective reaction which is `objective_value * fraction_optimum`. In case of `fraction_optimum = 1.0` this is identical to the `value` in `01_objective.tsv
```
model	objective	reaction	flux	status	minimum	maximum	fraction_optimum
./e_coli_core.xml	obj	R_ACALD	0.8739215069684295	optimal	1.1348525979450152e-14	0.0	1.0
./e_coli_core.xml	obj	R_ACALDt	0.8739215069684295	optimal	3.662182303830574e-15	0.0	1.0
./e_coli_core.xml	obj	R_ACKr	0.8739215069684295	optimal	0.0	0.0	1.0
./e_coli_core.xml	obj	R_ACONTa	0.8739215069684295	optimal	6.007249575350388	6.007249575350355	1.0
./e_coli_core.xml	obj	R_ACONTb	0.8739215069684295	optimal	6.007249575350388	6.007249575350264	1.0
./e_coli_core.xml	obj	R_ACt2r	0.8739215069684295	optimal	1.772023695401875e-14	0.0	1.0
./e_coli_core.xml	obj	R_ADK1	0.8739215069684295	optimal	0.0	-3.4583850794047745e-14	1.0
./e_coli_core.xml	obj	R_AKGDH	0.8739215069684295	optimal	5.064375661482467	5.0643756614820665	1.0
./e_coli_core.xml	obj	R_AKGt2r	0.8739215069684295	optimal	0.0	0.0	1.0
./e_coli_core.xml	obj	R_ALCD2x	0.8739215069684295	optimal	9.884200046617872e-15	0.0	1.0
./e_coli_core.xml	obj	R_ATPM	0.8739215069684295	optimal	8.39	8.389999999999924	1.0
./e_coli_core.xml	obj	R_ATPS4r	0.8739215069684295	optimal	45.51400977451763	45.514009774517376	1.0
./e_coli_core.xml	obj	R_BIOMASS_Ecoli_core_w_GAM	0.8739215069684295	optimal	0.873921506968431	0.8739215069684305	1.0
./e_coli_core.xml	obj	R_CO2t	0.8739215069684295	optimal	-22.80983331020497	-22.80983331020505	1.0
...
```
See for instance: [`e_coli_core/02_fva.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/examples/results/e_coli_core/cobrapy/02_fva.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA](https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA)

## 03 Gene deletions 
The gene deletion file `03_gene_deletion.tsv` contains five columns with the headers `model`, `objective`, `gene`, `status` and `value`. The `model` column stores the SBML model filename.
The `gene` column contains the SBML gene identifiers. The `status` and `value` columns contain the status of the optimization (`optimal` or `infeasible`) and optimal value under the given gene deletion. If the status is `infeasible` the value is empty. The rows are sorted based on gene identifier.
```
model	objective	gene	status	value
./e_coli_core.xml	obj	G_b0008	optimal	0.873921506968431
./e_coli_core.xml	obj	G_b0114	optimal	0.7966959254309566
./e_coli_core.xml	obj	G_b0115	optimal	0.7966959254309566
./e_coli_core.xml	obj	G_b0116	optimal	0.7823510529477393
./e_coli_core.xml	obj	G_b0118	optimal	0.8739215069684314
./e_coli_core.xml	obj	G_b0351	optimal	0.8739215069684306
./e_coli_core.xml	obj	G_b0356	optimal	0.873921506968431
...
./e_coli_core.xml	obj	G_b2415	infeasible	NaN
./e_coli_core.xml	obj	G_b2416	infeasible	NaN
...
```
See for instance: [`e_coli_core/03_gene_deletion.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/examples/results/e_coli_core/cobrapy/03_gene_deletion.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/deletions.html](https://cobrapy.readthedocs.io/en/latest/deletions.html)

## 04 Reaction deletions 
The reaction deletion file `04_reaction_deletion.tsv` contains five columns with the headers `model`, `objective`, `reaction`, `status` and `value`. The `model` column stores the SBML model filename. 
The `reaction` column contains the SBML reaction identifiers. The `status` and `value` columns contain the status of the optimization (`optimal` or `infeasible`) and optimal value under the given reaction deletion. If the status is `infeasible` the value is empty. The rows are sorted based on reaction identifier.
```
model	objective	reaction	status	value
./e_coli_core.xml	obj	R_ACALD	optimal	0.873921506968431
./e_coli_core.xml	obj	R_ACALDt	optimal	0.873921506968431
./e_coli_core.xml	obj	R_ACKr	optimal	0.8739215069684305
./e_coli_core.xml	obj	R_ACONTa	optimal	-3.2790312837402413e-15
./e_coli_core.xml	obj	R_ACONTb	optimal	-4.655434573658402e-15
./e_coli_core.xml	obj	R_ACt2r	optimal	0.8739215069684313
./e_coli_core.xml	obj	R_ADK1	optimal	0.873921506968431
./e_coli_core.xml	obj	R_AKGDH	optimal	0.8583074080226888
...
```
See for instance: [`e_coli_core/04_reaction_deletion.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/src/fbc_curation/examples/results/e_coli_core/cobrapy/04_reaction_deletion.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/deletions.html](https://cobrapy.readthedocs.io/en/latest/deletions.html).
