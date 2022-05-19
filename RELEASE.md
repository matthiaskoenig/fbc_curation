# Release information

* update schema using `schema.py`
* make sure all tests run (`tox -p`)
* update release notes in `release-notes`
* bump version (`bumpversion [major|minor|patch]`)
* `git push --tags` (triggers release)
* `git push`
* merge `develop` in `main` after release

* test installation in virtualenv from pypi
```
mkvirtualenv test --python=python3.9
(test) pip install fbc_curation
```
