# TODO:

## Benchmarking
- [ ] results statistics and plots (interactive results) => Altair
- [ ] package fbc_curation (docker container & conda package) for cluster/reproducibility
  - [ ] clean logging from individual processes 
  - [ ] results/overview JSON for statistics (more fine grained); per FROG file; percentages, ....    
- [ ] deactivate internal parallelization (cobrapy), fix single core & thread (blocking resources)
- [ ] run on kubernetics/cluster

(- [ ] database of results)

## Webapp
- [ ] minimal functionality of upload and running fbc curation


# FROG Benchmark evaluation
FROG is systematically evaluated on the following model collection
https://github.com/biosustain/memote-meta-models

We are using version 1 containing overall 10591 models. The FROG analysis is implemented
as a snakemake workflow allowing clean separation of the individual FROG execution.
Currently run
- 88/10591 (~2-3 [hr], 15 cores)

# snakemake installation

sudo apt-get install graphviz graphviz-dev
pip install snakemake
pip install pygraphviz


https://snakemake.readthedocs.io/en/stable/tutorial/short.html
First, create an empty workflow in the current directory with:
```
touch Snakefile
```
Once a Snakefile is present, you can perform a dry run of Snakemake with:
```
snakemake -n
```

# linter
Snakemake (>=5.11) comes with a code quality checker (a so called linter), that analyzes your workflow and highlights issues that should be solved in order to follow best practices, achieve maximum readability, and reproducibility. The linter can be invoked with
```
snakemake --lint
```

# execution
https://snakemake.readthedocs.io/en/stable/executing/cli.html
```
snakemake --cores 1
```

## visualization
https://snakemake.readthedocs.io/en/stable/executing/cli.html#visualization
To visualize the workflow, one can use the option --dag. This creates a representation of the DAG in the graphviz dot language which has to be postprocessed by the graphviz tool dot. E.g. to visualize the DAG that would be executed, you can issue:

```
snakemake --dag | dot | display
```

## report
https://snakemake.readthedocs.io/en/stable/executing/cli.html#REPORTS

```
snakemake --cores 1 --report
```
