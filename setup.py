#!/usr/bin/env python
import os
import re
import sys
import warnings

from setuptools import setup, find_packages
from setuptools import Command

MAJOR = 0
MINOR = 6
MICRO = 1
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
QUALIFIER = ''


DISTNAME = 'xray'
LICENSE = 'Apache'
AUTHOR = 'xray Developers'
AUTHOR_EMAIL = 'xray-dev@googlegroups.com'
URL = 'https://github.com/xray/xray'
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Scientific/Engineering',
]

INSTALL_REQUIRES = ['numpy >= 1.7', 'pandas >= 0.15.0']
TESTS_REQUIRE = ['pytest >= 2.7.1']

if sys.version_info[:2] < (2, 7):
    TESTS_REQUIRE += ["unittest2 == 0.5.1"]

DESCRIPTION = "N-D labeled arrays and datasets in Python"
LONG_DESCRIPTION = """
**xray** is an open source project and Python package that aims to bring the
labeled data power of pandas_ to the physical sciences, by providing
N-dimensional variants of the core pandas data structures.

Our goal is to provide a pandas-like and pandas-compatible toolkit for
analytics on multi-dimensional arrays, rather than the tabular data for which
pandas excels. Our approach adopts the `Common Data Model`_ for self-
describing scientific data in widespread use in the Earth sciences:
``xray.Dataset`` is an in-memory representation of a netCDF file.

.. _pandas: http://pandas.pydata.org
.. _Common Data Model: http://www.unidata.ucar.edu/software/thredds/current/netcdf-java/CDM
.. _netCDF: http://www.unidata.ucar.edu/software/netcdf
.. _OPeNDAP: http://www.opendap.org/

Important links
---------------

- HTML documentation: http://xray.readthedocs.org
- Issue tracker: http://github.com/xray/xray/issues
- Source code: http://github.com/xray/xray
- SciPy2015 talk: https://www.youtube.com/watch?v=X0pAhJgySxk
"""

# code to extract and write the version copied from pandas
FULLVERSION = VERSION
write_version = True

if not ISRELEASED:
    import subprocess
    FULLVERSION += '.dev'

    pipe = None
    for cmd in ['git', 'git.cmd']:
        try:
            pipe = subprocess.Popen(
                [cmd, "describe", "--always", "--match", "v[0-9]*"],
                stdout=subprocess.PIPE)
            (so, serr) = pipe.communicate()
            if pipe.returncode == 0:
                break
        except:
            pass

    if pipe is None or pipe.returncode != 0:
        # no git, or not in git dir
        if os.path.exists('xray/version.py'):
            warnings.warn("WARNING: Couldn't get git revision, using existing xray/version.py")
            write_version = False
        else:
            warnings.warn("WARNING: Couldn't get git revision, using generic version string")
    else:
        # have git, in git dir, but may have used a shallow clone (travis does this)
        rev = so.strip()
        # makes distutils blow up on Python 2.7
        if sys.version_info[0] >= 3:
            rev = rev.decode('ascii')

        if not rev.startswith('v') and re.match("[a-zA-Z0-9]{7,9}", rev):
            # partial clone, manually construct version string
            # this is the format before we started using git-describe
            # to get an ordering on dev version strings.
            rev = "v%s.dev-%s" % (VERSION, rev)

        # Strip leading v from tags format "vx.y.z" to get th version string
        FULLVERSION = rev.lstrip('v')

else:
    FULLVERSION += QUALIFIER


def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
"""
    if not filename:
        filename = os.path.join(
            os.path.dirname(__file__), 'xray', 'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (FULLVERSION, VERSION))
    finally:
        a.close()

if write_version:
    write_version_py()

setup(name=DISTNAME,
      version=FULLVERSION,
      license=LICENSE,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      classifiers=CLASSIFIERS,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      install_requires=INSTALL_REQUIRES,
      tests_require=TESTS_REQUIRE,
      url=URL,
      packages=find_packages(),
      package_data={'xray': ['test/data/*', 'plot/default_colormap.csv']})
