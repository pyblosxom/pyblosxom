#!/usr/bin/env python

import os.path, sys, os
from distutils.sysconfig import get_python_lib

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

version = "1.5"

DESC = """PyBlosxom
=========

Summary
-------

PyBlosxom is a file-based weblog engine originally inspired by Blosxom.  
It supports user-created plugins to augment and extend the default 
behavior.  It supports Paste, WSGI, and CGI and can run in a variety of 
environments.


Download and installation
-------------------------

To download and install PyBlosxom you can get the .tar.gz file at::

   http://pyblosxom.sourceforge.net/

Or you can use easy_install::

   easy_install PyBlosxom
"""

setup(name="pyblosxom",
    version=version,
    description="PyBlosxom is a file-based weblog engine.",
    long_description=DESC,
    license='MIT',
    author="Will Kahn-Greene, et al",
    author_email="pyblosxom-devel@lists.sourceforge.net",
    keywords="blog pyblosxom cgi weblog",
    url="http://pyblosxom.sourceforge.net/",
    packages=find_packages(exclude=["ez_setup"]),
    scripts=["bin/pyblosxom-cmd"],
    zip_safe=False,
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
