# Release info
Steps for release are
## github release
* github: close and update issues/milestone
* update version number in develop branch
* make sure all tests run (`pytest`)
* add changes to README changelog section
* github: merge all develop changes to master via pull request
* github: create release from master branch

## pypi
* release on [pypi](https://pypi.python.org/pypi/fbc_curation)
```
git branch master
git pull
rm -rf dist
python setup.py sdist
twine upload dist/*
```
* test installation in virtualenv from pypi
```
mkvirtualenv test --python=python3.7
(test) pip install fbc_curation
```

## version bump
* switch to develop branch and increase version number