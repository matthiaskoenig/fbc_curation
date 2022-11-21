# Documentation
The documentation is hosted on `readthedocs` at https://fbc-curation.readthedocs.io.
The documentation is build using `sphinx` with the 
[sphinx-rtd-theme](https://sphinx-rtd-theme.readthedocs.io/en/latest/configuring.html).

## Update documentation
First update the documentation 


To create the documentation use
```bash
(frog) cd docs_builder
(frog) pip install -r requirements-docs.txt
(frog) python -m ipykernel install --user --name=frog
(frog) ./make_docs.sh
```


