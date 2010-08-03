#!/usr/bin/env python

import os.path, sys, os
from distutils.sysconfig import get_python_lib
try:
    from distribute import setup, find_packages
    print "Using distribute...."
except ImportError:
    from setuptools import setup, find_packages
    print "Using setuptools...."

version = "1.5rc2"

setup(
    name="pyblosxom",
    version=version,
    description="PyBlosxom is a file-based weblog engine.",
    long_description=open('README').read(),
    license='MIT',
    author="Will Kahn-Greene, et al",
    author_email="willg@bluesock.org",
    keywords="blog pyblosxom cgi weblog",
    url="http://pyblosxom.bluesock.org/",
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
        "License :: OSI Approved :: MIT/X Consortium License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
    ]
)
