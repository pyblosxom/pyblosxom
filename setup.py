#!/usr/bin/env python

from distutils.core import setup

setup(name="pyblosxom",
      version='CVS',
      description="pyblosxom weblog engine",
      author="Wari Wahab",
      author_email="wari@home.wari.org",
      url="http://roughingit.subtlehints.net/pyblosxom",
      packages=['Pyblosxom', 'Pyblosxom.cache', 'Pyblosxom.entries',
      		'Pyblosxom.renderers'],
      licence = 'Python',
      long_description =
"""Pyblosxom is a weblog engine that users the filesystem as the database of
your entries.
"""
     )
