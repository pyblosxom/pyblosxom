.. _hacking-chapter:

======================
 Hacking on Pyblosxom
======================

Installing PyBlosxom to hack on it is a little different since you:

1. want to be running PyBlosxom from a git clone

2. want PyBlosxom installed such that you don't have to keep running
   ``python setup.py install``

3. want Paste installed so you can test locally


This document covers installing Pyblosxom into a virtual environment
and deploying it using Paste.


Requirements
============

This requires:

* Python 2.4 or higher
* `git`_
* `virtualenv`_
* `PasteScript`_, the command-line frontend for the Python Paste web
  development utilities

.. _git: http://git-scm.com/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _PasteScript: http://pypi.python.org/pypi/PasteScript


Installation
============

To install:

1. Create a virtual environment for PyBlosxom into a directory of your
   choosing as denoted by ``<VIRTUAL-ENV-DIR>``::

      virtualenv <VIRTUAL-ENV-DIR>

   This is the virtual environment that PyBlosxom will run in.  If you
   decide to delete PyBlosxom at some point, you can just remove this
   virtual environment directory.

2. Activate the virtual environment::

      source <VIRTUAL-ENV-DIR>/bin/activate

   Remember to activate the virtual environment **every** time you do
   something with PyBlosxom.

   Additionally, if you're running PyBlosxom from CGI or a cron job,
   you want to use the ``python`` interpreter located in the ``bin``
   directory of your virtual environment--not the system one.

3. Using git, clone the PyBlosxom repository::

      git clone git://gitorious.org/pyblosxom/pyblosxom.git pyblosxom

4. Change directories into the ``pyblosxom`` directory and run::

      python setup.py develop


Running Pyblosxom
=================

When you want to run PyBlosxom from your git clone in your virtual
environment, you will:

1. Make sure the virtual environment is activated and if it isn't do::

      source <VIRTUAL-ENV-DIR>/bin/activate

2. Change directories into where you have your blog and do::

      paster serve blog.ini


Updating Pyblosxom
==================

Because you installed PyBlosxom with ``python setup.py develop``, when
you make changes to the PyBlosxom code, they'll be available in the
environment---you don't need to re-run ``python setup.py develop``.



