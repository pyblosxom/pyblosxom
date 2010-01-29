#!/usr/bin/env python

import os.path, sys, os
from distutils.sysconfig import get_python_lib
try:
    from distribute import setup, find_packages
    print "Using distribute...."
except ImportError:
    from setuptools import setup, find_packages
    print "Using setuptools...."

version = "1.5-rc1"

DESC = """PyBlosxom
=========

Summary
-------

PyBlosxom is a file-based weblog engine originally inspired by
Blosxom.  It supports user-created plugins to augment and extend the
default behavior.  It supports Paste, WSGI, and CGI and can run in a
variety of environments.


Download and installation
-------------------------

To download and install PyBlosxom you can get the .tar.gz file at::

   http://pyblosxom.sourceforge.net/

Or you can use pip (http://pypi.python.org/pypi/pip)::

   pip install pyblosxom

If you have easy_install, but don't have pip, you can do::

   easy_install pyblosxom
"""

setup(
    name="pyblosxom",
    version=version,
    description="PyBlosxom is a file-based weblog engine.",
    long_description=DESC,
    license='MIT',
    author="Will Kahn-Greene, et al",
    author_email="willg@bluesock.org",
    keywords="blog pyblosxom cgi weblog",
    url="http://pyblosxom.sourceforge.net/",
    packages=find_packages(exclude=["ez_setup"]),
    scripts=["bin/pyblosxom-cmd"],
    zip_safe=False,
    test_suite="Pyblosxom.tests.testrunner.test_suite",
    include_package_data=True,
    install_requires=[], # FIXME
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT/X Consortium License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
    ]
)
