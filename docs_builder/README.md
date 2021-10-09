# Documentation

To create the documentation use
```bash
(fbc_curation) pip install -r requirements-docs.txt
(fbc_curation) python -m ipykernel install --user --name=sbmlsim
```

```bash
(fbc_curation) cd docs
(fbc_curation) ./make_docs.sh
```

The documentation is build using `sphinx` with the 
[sphinx-rtd-theme](https://sphinx-rtd-theme.readthedocs.io/en/latest/configuring.html) 
