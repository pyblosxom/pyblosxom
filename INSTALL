====================
Installing PyBlosxom
====================

This guide walks through two different ways to install PyBlosxom:
site-wide and individual.

If this file doesn't meet your needs, ask us on the pyblosxom-users
mailing list or on IRC.  Information on both is on the website_.

.. _website: http://pyblosxom.sourceforge.net/

.. Note::

   If you're testing PyBlosxom, use ``virtualenv`` and deploy with
   Paste.  It'll save you a lot of time and it's easy to clean up
   afterwards.

.. Note::

   If you're upgrading from a previous version, make sure to read
   the Changelog.

Requirements
============

Minimally, PyBlosxom requires Python 2.3 to install.

PyBlosxom is well supported on GNU/Linux, probably works on Mac OSX,
and might work on Windows.

PyBlosxom works with any web-server as a CGI application, works as a
WSGI application, and might work in other contexts.


Install
=======

Install
-------

Single user install
-------------------

If you want to install PyBlosxom for a single user or want to install
it in a virtual environment where it can't get naughty with anything
else, use `virtualenv`_.

First build a virtual environment::

   virtualenv --no-site-packages <dest_dir>

Then activate the virtual environment::

   <dest_dir>/usr/bin/activate

Then install PyBlosxom using one of the instructions below.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv


Installation
------------

If you have `distribute`_ and `pip`_ installed and want to do a
site-wide installation, do::

   pip install pyblosxom

.. _distribute: http://pypi.python.org/pypi/distribute
.. _pip: http://pypi.python.org/pypi/pip

If you have `setuptools`_ installed and want to do a site-wide
installation, do::

   easy_install pyblosxom

.. _setuptools: http://pypi.python.org/pypi/setuptools

You can download the tarball.  Tarballs are at
http://sourceforge.net/project/showfiles.php?group_id=67445 .  Extract
the ``tar.gz`` file and run::

   python setup.py install

Lastly, you can do an svn checkout.  Instructions are at
http://sourceforge.net/scm/?type=svn&group_id=67445 .  Generally,
*trunk* is unstable but any of the tags are stable.  Then run::

   python setup.py install

If none of those methods works for you, then you might want to
reconsider using PyBlosxom.


Creating a blog
===============

To create a blog, do::

   pyblosxom-cmd create ./blog/

That generates the directory structure, required files, and a first
post in the ``./blog/`` directory.


Deploying
=========

There are a bunch of ways to deploy your blog.  See the chapters on
deployment for documented options.


Post-install
============

After you finish installing PyBlosxom, you should sign up on the
*pyblosxom-users* mailing list.

Additionally, please hop on the ``#pyblosxom`` IRC channel on
``irc.freenode.net`` and say hi.  It'll almost certainly help you get
acquainted with PyBlosxom and it'll reduce the amount of time it takes
to get your blog up and going.