# Reference files
In the following the four created reference files and the metadata file are described and examples provided for the [`e_coli_core.xml`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/models/e_coli_core.xml) model. All output files are tab separated files (TSV) with the first three columns being `model`, `objective`, and `status`. The column `model` encodes the SBML model id. The column `objective` encodes the SBML objective id, which is the objective which was optimized in the respective simulation. The column `status` encodes the status of the simulation. The status can be either `optimal` (optimization worked) or `infeasible` (no solution found or problem in simulation).  

## Metadata file
A required metadata file `metadata.json` encodes information about the curation run and the used software and library.
The following fields are required or optional

- `software.name` (required): software used to create the reference files,
- `software.version` (required): software version
- `software.url` (optional): url to software
- `environment` (optional): information on operating system and environment
- `model.filename` (required): SBML model filename
- `model.md5` (required): Sha5 hash of model
- `solver.name` (required): solver used for optimization,
- `solver.version` (required): solver version

A concrete example of the metadata is shown below
```
{
  "software.name": "fbc_curation",
  "software.version": "0.1.1",
  "software.url": "https://doi.org/10.5281/zenodo.3708271",
  "environment": "posix, Linux, 5.4.0-48-generic",
  "model.filename": "e_coli_core.xml",
  "model.md5": "4574760460afe9e1b3388dc15f354706",
  "solver.name": "cobrapy (glpk)",
  "solver.version": "0.20.0"
}
```

For an example file see [`e_coli_core/metadata.json`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/metadata.json).

## 01 Objective value
The objective value file `01_objective.tsv` contains the four columns with the headers `model`, `objective`, `status`, and `value`. The `model` column stores the SBML model filename. 
The `value` is the optimal value of the respective objective function when the model is optimized. If the status is `infeasible`, no value is provided, i.e., the value is empty.
```
model	objective	status	value
e_coli_core.xml	obj	optimal	0.873922
```
For an example file see [`e_coli_core/01_objective.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/01_objective.tsv). For more information on how to simulate the FBA see [https://cobrapy.readthedocs.io/en/latest/simulating.html](https://cobrapy.readthedocs.io/en/latest/simulating.html).

## 02 Flux variability analysis (FVA)
The FVA file `02_fva.tsv` contains six columns with the headers `model`, `objective`, `reaction`, `flux`, `status`, `minimum` and `maximum`. The `model` column stores the SBML model filename. The `reaction` column stores the SBML reaction id. The `minimum` and `maximum` columns contain the minimum and maximum values of the FVA. The rows are sorted based on the SBML reaction identifier. The `status` contains the status of the optimization (`optimal` or `infeasible`). If the status is `infeasible` the value is empty.
Flux variability is calculated with `fraction_of_optimum = 1.0`, i.e. the objective of the model is set to its maximum in secondary optimization (percent of optimum is 100%). The `flux` column stores the reference flux.
```
model	objective	reaction	flux	status	minimum	maximum
e_coli_core.xml	obj	ACALD	0.0	optimal	0.0	0.0
e_coli_core.xml	obj	ACALDt	0.0	optimal	0.0	0.0
e_coli_core.xml	obj	ACKr	0.0	optimal	0.0	0.0
e_coli_core.xml	obj	ACONTa	6.00725	optimal	6.00725	6.00725
e_coli_core.xml	obj	ACONTb	6.00725	optimal	6.00725	6.00725
e_coli_core.xml	obj	ACt2r	0.0	optimal	0.0	0.0
e_coli_core.xml	obj	ADK1	0.0	optimal	0.0	0.0
e_coli_core.xml	obj	AKGDH	5.064376	optimal	5.064376	5.064376
e_coli_core.xml	obj	AKGt2r	0.0	optimal	0.0	0.0
e_coli_core.xml	obj	ALCD2x	0.0	optimal	0.0	0.0
e_coli_core.xml	obj	ATPM	8.39	optimal	8.39	8.39
e_coli_core.xml	obj	ATPS4r	45.51401	optimal	45.51401	45.51401
e_coli_core.xml	obj	BIOMASS_Ecoli_core_w_GAM	0.873922	optimal	0.873922	0.873922
e_coli_core.xml	obj	CO2t	-22.809833	optimal	-22.809833	-22.809833
...
```
See for instance: [`e_coli_core/02_fva.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/02_fva.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA](https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA)

## 03 Gene deletions 
The gene deletion file `03_gene_deletion.tsv` contains five columns with the headers `model`, `objective`, `gene`, `status` and `value`. The `model` column stores the SBML model filename.
The `gene` column contains the SBML gene identifiers. The `status` and `value` columns contain the status of the optimization (`optimal` or `infeasible`) and optimal value under the given gene deletion. If the status is `infeasible` the value is empty. The rows are sorted based on gene identifier.
```
model	objective	gene	status	value
e_coli_core.xml	obj	b0008	optimal	0.873922
e_coli_core.xml	obj	b0114	optimal	0.796696
e_coli_core.xml	obj	b0115	optimal	0.796696
e_coli_core.xml	obj	b0116	optimal	0.782351
e_coli_core.xml	obj	b0118	optimal	0.873922
e_coli_core.xml	obj	b0351	optimal	0.873922
...
e_coli_core.xml	obj	b2415	infeasible	
e_coli_core.xml	obj	b2416	infeasible	
...
```
See for instance: [`e_coli_core/03_gene_deletion.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/03_gene_deletion.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/deletions.html](https://cobrapy.readthedocs.io/en/latest/deletions.html)

## 04 Reaction deletions 
The reaction deletion file `04_reaction_deletion.tsv` contains five columns with the headers `model`, `objective`, `reaction`, `status` and `value`. The `model` column stores the SBML model filename. 
The `reaction` column contains the SBML reaction identifiers. The `status` and `value` columns contain the status of the optimization (`optimal` or `infeasible`) and optimal value under the given reaction deletion. If the status is `infeasible` the value is empty. The rows are sorted based on reaction identifier.
```
model	objective	reaction	status	value
e_coli_core.xml	obj	ACALD	optimal	0.873922
e_coli_core.xml	obj	ACALDt	optimal	0.873922
e_coli_core.xml	obj	ACKr	optimal	0.873922
e_coli_core.xml	obj	ACONTa	optimal	0.0
e_coli_core.xml	obj	ACONTb	optimal	0.0
e_coli_core.xml	obj	ACt2r	optimal	0.873922
e_coli_core.xml	obj	ADK1	optimal	0.873922
e_coli_core.xml	obj	AKGDH	optimal	0.858307
...
```
See for instance: [`e_coli_core/04_reaction_deletion.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/04_reaction_deletion.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/deletions.html](https://cobrapy.readthedocs.io/en/latest/deletions.html).
