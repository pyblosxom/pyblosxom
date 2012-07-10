.. _hacking-chapter:

======================
 Hacking on PyBlosxom
======================

This will cover installing PyBlosxom from the git repositories in a
way that won't interfere with the packages or modules already installed on 
the system.

Installing PyBlosxom to hack on it is a little different since you:

1. want to be running PyBlosxom from a git clone

2. want PyBlosxom installed such that you don't have to keep running
   ``python setup.py install``

3. want Paste installed so you can test locally


As such, this document covers installing Pyblosxom into a virtual environment 
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

1. Create a virtual environment for Pyblosxom into a directory of your
   choosing as denoted by ``<VIRTUAL-ENV-DIR>``::

      virtualenv <VIRTUAL-ENV-DIR>

   This is the virtual environment that Pyblosxom will run in.  If you
   decide to delete Pyblosxom at some point, you can just remove this
   virtual environment directory.

2. Activate the virtual environment::

      source <VIRTUAL-ENV-DIR>/bin/activate

   Remember to activate the virtual environment **every** time you do
   something with Pyblosxom.

   Additionally, if you're running Pyblosxom from CGI or a cron job,
   you want to use the ``python`` interpreter located in the ``bin``
   directory of your virtual environment--not the system one.

3. Using git, clone the Pyblosxom repository::

      git clone https://github.com/pyblosxom/pyblosxom.git

4. Change directories into the ``pyblosxom`` directory and run::

      python setup.py develop


Running Pyblosxom
=================

When you want to run Pyblosxom from your git clone in your virtual
environment, you will:

1. Make sure the virtual environment is activated and if it isn't do::

      source <VIRTUAL-ENV-DIR>/bin/activate

2. Change directories into where you have your blog and do::

      paster serve blog.ini
	  
Note: If you get an error message about "paster" not being currently 
installed, or about the system not finding PyBlosxom, it is likely
that you have Paster and PyBlosxom installed in different places.
To ensure Paster is installed in your virtualenv, make sure it 
is activated (see step 1) and then use pip to install paste.

Note 2: Due to a bug in some linux distributions, it is recommended
to install paste in the following three steps::

	pip install paste
	pip install pastedeploy 
	pip install pastescript


Updating Pyblosxom
==================

Because you installed Pyblosxom with ``python setup.py develop``, when
you make changes to the Pyblosxom code, they'll be available in the
environment---you don't need to re-run ``python setup.py develop``.


Where to go from here
======================

Once set up, you can continue to the 
`Creating your blog <http://pyblosxom.github.com/1.5/install.html#creating-a-blog>`_. chapter
