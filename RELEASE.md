# Release information

## make release
* sort imports (`isort src/sbmlsim`)
* code formating (`black src/sbmlsim`)
* make sure all tests run (`tox --`)
* update release notes in `release-notes`
* bump version (`bumpversion patch` or `bumpversion minor`)
* `git push --tags` (triggers release)
* add release-notes for next version

* test installation in virtualenv from pypi
```
mkvirtualenv test --python=python3.7
(test) pip install fbc_curation
```
