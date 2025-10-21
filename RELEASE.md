# Release information

* update schema using `src/fbc_curation/schema.py` and update `docs_builder/schema.rst`
* rerun examples `src/fbc_curation/examples.py`
* update documentation with latest results (`README.md`)
* update release notes in `release-notes`
* make sure all tests run (`tox -p`)
* check formating and linting (`ruff check`)
* test bump version (`uvx bump-my-version bump [major|minor|patch] --dry-run -vv`)
* bump version (`uvx bump-my-version bump [major|minor|patch]`)
* `git push --tags` (triggers release)
* `git push`
* merge `develop` in `main` after release

* test installation in virtualenv from pypi
```bash
uv venv --python 3.13
uv pip install fbc-curation
```

# Install dev dependencies:
```bash
# install core dependencies
uv sync
# install dev dependencies
uv pip install -r pyproject.toml --extra dev
```

## Testing
See information on https://github.com/tox-dev/tox-uv
```bash
uv tool install tox --with tox-uv
```
Run single tox target
```bash
tox r -e py313
```
Run all tests in parallel
```bash
tox run-parallel
```

# Setup pre-commit
```bash
uv pip install pre-commit
pre-commit install
pre-commit run
```

# Documentation
## Setup docs
```bash
uv pip install -r pyproject.toml --extra docs
```

## Serve docs
```bash
mkdocs serve -a localhost:3456
```
