#!/usr/bin/env python

#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

import os
import re
from setuptools import setup, find_packages


READMEFILE = "README.rst"
VERSIONFILE = os.path.join("Pyblosxom", "_version.py")
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"


def get_version():
    verstrline = open(VERSIONFILE, "rt").read()
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError(
            "Unable to find version string in %s." % VERSIONFILE)


setup(
    name="pyblosxom",
    version=get_version(),
    description="Pyblosxom is a file-based weblog engine.",
    long_description=open(READMEFILE).read(),
    license='MIT',
    author="Will Kahn-Greene, et al",
    author_email="willg@bluesock.org",
    keywords="blog pyblosxom cgi weblog wsgi",
    url="http://pyblosxom.github.com/",
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
    ]
)
