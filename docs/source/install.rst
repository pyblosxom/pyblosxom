====================
Installing PyBlosxom
====================

This guide walks through two different ways to install PyBlosxom: system-wide 
and individual.

If this file doesn't meet your needs, ask us on the pyblosxom-users mailing 
list or on IRC.  Information on both is on the website_.

.. _website: http://pyblosxom.sourceforge.net/

.. Note:: Note to people testing PyBlosxom
   If you're testing PyBlosxom, do an individual installation.


Requirements
============

* Python 2.3 or later to run PyBloxsxom
* other requirements depending on how you want to deploy your blog


Individual installation
=======================

1. Follow the links at http://pyblosxom.sourceforge.net/ to download PyBlosxom.

2. Extract the contents of the ``.tar.gz`` file.

When you use PyBlosxom things, you'll need to add the path to the ``pyblosxom``
to the Python path.

You can do this in Python scripts by appending the diectory to ``sys.path``::

    import sys
    sys.path.append("/path/to/pyblosxom")

You can do this by setting the ``PYTHONPATH`` environment variable, too.  For
example::

    PYTHONPATH=/home/joe/pyblosxom/ python pyblcmd --help


System-wide installation
========================

If you have easy_install installed, run::

    easy_install pyblosxom

If you don't have easy_install installed, you can install it and PyBlosxom by
downloading the script from http://peak.telecommunity.com/dist/ez_setup.py and
running::

    python ez_setup.py pyblosxom

If you want to install PyBlosxom as a library, but not system-wide, you can
use Ian Bicking's `virtualenv`_.  It's fantastic for setting up Python 
environments.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv


Deploying PyBlosxom
===================

There are a bunch of different ways to deploy PyBlosxom.  Many of these are
detailed on the `website`_.  If you can't find instructions for deploying
PyBlosxom in the manner of your choosing, ask us on the pyblosxom-devel
mailing list or on IRC.

.. _website: http://pyblosxom.sourceforge.net/


Post-install
============

After you finish installing PyBlosxom, you should sign up on the 
pyblosxom-users mailing list.

Additionally, please hop on the ``#pyblosxom`` IRC channel on ``irc.freenode.net``
and say hi.  It'll almost certainly help you get acquainted with PyBlosxom 
and it'll reduce the amount of time it takes to get your blog up and going.
