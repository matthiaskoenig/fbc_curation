# Standardized reference files
In the following the four created reference files are described and examples provided for the [`e_coli_core.xml`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/models/e_coli_core.xml) model. All output files are tab separated files (TSV) with the first three columns being `model`, `objective`, and `status`. The column `model` encodes the SBML model id. The column `objective` encodes the SBML objective id, which is the objective which was optimized in the respective simulation. The column `status` encodes the status of the simulation. The status can be either `optimal` (optimization worked) or `infeasible` (no solution found or problem in simulation).  

## 01 Objective value
The objective value file `01_objective.tsv` contains the four columns with the headers `model`, `objective`, `status`, and `value`. The `value` is the optimal value of the respective objective function when the model is optimized. If the status is `infeasible`, no value is provided, i.e., the value is empty.
```
model	objective	status	value
e_coli_core	obj	optimal	0.873922
```
For an example file see [`e_coli_core/01_objective.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/01_objective.tsv). For more information on how to simulate the FBA see [https://cobrapy.readthedocs.io/en/latest/simulating.html](https://cobrapy.readthedocs.io/en/latest/simulating.html).

## 02 Flux variability analysis (FVA)
The FVA file `02_fva.tsv` contains five columns with the headers `model`, `objective`, `reaction`, `status`, `minimum` and `maximum`. The `reaction` column stores the SBML reaction id. The `minimum` and `maximum` columns contain the minimum and maximum values of the FVA. The rows are sorted based on the SBML reaction identifier. The `status` contains the status of the optimization (`optimal` or `infeasible`). If the status is `infeasible` the value is empty.
Flux variability is calculated with `fraction_of_optimum = 1.0`, i.e. the objective of the model is set to its maximum in secondary optimization.
```
model	objective	reaction	status	minimum	maximum
e_coli_core	obj	ACALD	optimal	0.0	0.0
e_coli_core	obj	ACALDt	optimal	0.0	0.0
e_coli_core	obj	ACKr	optimal	0.0	0.0
e_coli_core	obj	ACONTa	optimal	6.00725	6.00725
e_coli_core	obj	ACONTb	optimal	6.00725	6.00725
e_coli_core	obj	ACt2r	optimal	0.0	0.0
e_coli_core	obj	ADK1	optimal	0.0	0.0
e_coli_core	obj	AKGDH	optimal	5.064376	5.064376
...
```
See for instance: [`e_coli_core/02_fva.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/02_fva.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA](https://cobrapy.readthedocs.io/en/latest/simulating.html#Running-FVA)

## 03 Gene deletions 
The gene deletion file `03_gene_deletion.tsv` contains five columns with the headers `model`, `objective`, `gene`, `status` and `value`. 
The `gene` column contains the SBML gene identifiers. The `status` and `value` columns contain the status of the optimization (`optimal` or `infeasible`) and optimal value under the given gene deletion. If the status is `infeasible` the value is empty. The rows are sorted based on gene identifier.
```
model	objective	gene	status	value
e_coli_core	obj	b0008	optimal	0.873922
e_coli_core	obj	b0114	optimal	0.796696
e_coli_core	obj	b0115	optimal	0.796696
e_coli_core	obj	b0116	optimal	0.782351
e_coli_core	obj	b0118	optimal	0.873922
e_coli_core	obj	b0351	optimal	0.873922
...
e_coli_core	obj	b2415	infeasible	
e_coli_core	obj	b2416	infeasible	
...
```
See for instance: [`e_coli_core/03_gene_deletion.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/03_gene_deletion.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/deletions.html](https://cobrapy.readthedocs.io/en/latest/deletions.html)

## 04 Reaction deletions 
The reaction deletion file `04_reaction_deletion.tsv` contains five columns with the headers `model`, `objective`, `reaction`, `status` and `value`. 
The `reaction` column contains the SBML reaction identifiers. The `status` and `value` columns contain the status of the optimization (`optimal` or `infeasible`) and optimal value under the given reaction deletion. If the status is `infeasible` the value is empty. The rows are sorted based on reaction identifier.
```
model	objective	reaction	status	value
e_coli_core	obj	ACALD	optimal	0.873922
e_coli_core	obj	ACALDt	optimal	0.873922
e_coli_core	obj	ACKr	optimal	0.873922
e_coli_core	obj	ACONTa	optimal	0.0
e_coli_core	obj	ACONTb	optimal	0.0
e_coli_core	obj	ACt2r	optimal	0.873922
e_coli_core	obj	ADK1	optimal	0.873922
e_coli_core	obj	AKGDH	optimal	0.858307
...
```
See for instance: [`e_coli_core/04_reaction_deletion.tsv`](https://raw.githubusercontent.com/matthiaskoenig/fbc_curation/develop/examples/results/e_coli_core/cobrapy/04_reaction_deletion.tsv). For more information: [https://cobrapy.readthedocs.io/en/latest/deletions.html](https://cobrapy.readthedocs.io/en/latest/deletions.html).
