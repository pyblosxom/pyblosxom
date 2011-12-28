#!/usr/bin/env python

#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

VERSION = "1.5"

import os.path, sys, os
from distutils.sysconfig import get_python_lib
from setuptools import setup, find_packages


setup(
    name="pyblosxom",
    version=VERSION,
    description="Pyblosxom is a file-based weblog engine.",
    long_description=open('README').read(),
    license='MIT',
    author="Will Kahn-Greene, et al",
    author_email="willg@bluesock.org",
    keywords="blog pyblosxom cgi weblog",
    url="http://pyblosxom.bluesock.org/",
    download_url="http://pyblosxom.bluesock.org/download/",
    packages=find_packages(exclude=["ez_setup"]),
    scripts=["bin/pyblosxom-cmd"],
    zip_safe=False,
    test_suite="Pyblosxom.tests.testrunner.test_suite",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
    ]
)
