#!/bin/bash
###############################################################
# Build script for tellurium documentation from rst files and
# python docstrings in the tellurium package
#
# execute this script in the docs folder i.e., after
# 	cd tellurium/docs
#
# Usage:
#	./make_docs.sh 2>&1 | tee ./make_docs.log
#
# The documentation is written in docs/_build
###############################################################
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

date
echo "--------------------------------------"
echo "remove old documentation"
echo "--------------------------------------"
rm -rf _built

echo "--------------------------------------"
echo "create html docs"
echo "--------------------------------------"
cd $DIR
# make html
sphinx-build -b html . _build/html

# open documentation
firefox _build/html/index.html

