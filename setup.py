#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
sbmlutils pip package
"""
import io
import re
import os
from setuptools import find_packages
from setuptools import setup

setup_kwargs = {}


def read(*names, **kwargs):
    """ Read file info in correct encoding. """
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


# version from file
verstrline = read('fbc_curation/_version.py')
mo = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M)
if mo:
    verstr = mo.group(1)
    setup_kwargs['version'] = verstr
else:
    raise RuntimeError("Unable to find version string")

# description from markdown
long_description = read('README.rst')
setup_kwargs['long_description'] = long_description

setup(
    name='fbc_curation',
    description='FBC reference files for SBML model curation using cobrapy',
    url='https://github.com/matthiaskoenig/fbc_curation',
    author='Matthias König',
    author_email='konigmatt@googlemail.com',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Cython',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    keywords='SBML, FBC, simulation',
    packages=find_packages(),
    # package_dir={'': ''},
    package_data={
      'fbc_curation': [
              '../requirements.txt',
               'examples/models',
               'examples/results',
          ],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    # List run-time dependencies here.  These will be installed by pip when
    install_requires=[
        "pandas",
        "cobra",
        "pytest",
        "pytest-cov"
    ],
    entry_points={
        'console_scripts':
            [
                'fbc_curation_examples=fbc_curation.examples:run_examples',
                'fbc_curation=fbc_curation.fbc_files:main',
            ],
    },
    extras_require={},
    **setup_kwargs)
