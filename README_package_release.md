# Release information

* update schema using `src/fbc_curation/schema.py`
* rerun examples `src/fbc_curation/examples.py`
* update documentation (`README.rst` and `docs_builder`)
* make sure all tests run (`tox -p`)
* update release notes in `release-notes`
* bump version (`bumpversion [major|minor|patch]`)
* `git push --tags` (triggers release)
* `git push`
* merge `develop` in `main` after release

* test installation in virtualenv from pypi
```
mkvirtualenv test --python=python3.10
(test) pip install fbc_curation
```
