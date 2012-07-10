.. _dev-contributing:

==============
 Contributing
==============

This covers the basics you need to know for contributing to
PyBlosxom.


How to clone the project
========================

`PyBlosxom is on GitHub <https://github.com/pyblosxom/pyblosxom>`_.


If you have a GitHub account [Recommended]
-------------------------------------------

This is the ideal way to contribute because GitHub makes things simple
and convenient .

Go to the project page (https://github.com/pyblosxom/pyblosxom) and click on
"Fork" at the top right on the screen. GitHub will create a copy of the 
PyBlosxom repository in your account for you to work on.

Create a new branch off of master for any new work that you do.

When you want to send it upstream, create a pull request.

If you need help with this process, `see the GitHub documentation
<http://help.github.com/>`_.


If you don't have a GitHub account
----------------------------------

Clone the project using git::

    git clone https://github.com/pyblosxom/pyblosxom.git

Set ``user.name`` and ``user.email`` git configuration::

    git config user.name "your name"
    git config user.email "your@email.address"

Create a new branch off of master for any new work that you do.

When you want to send it upstream, do::

    git format-patch --stdout origin/master > NAME_OF_PATCH_FILE.patch

where ``NAME_OF_PATCH_FILE`` is a nice name that's short and
descriptive of what the patch holds and master should be replaced with your 
branch name

Then attach that ``.patch`` file and send it to pyblosxom-devel
mailing list.


Code conventions
================

Follow `PEP-8 <http://www.python.org/dev/peps/pep-0008/>`_.


Tests
=====

Please add tests for changes you make. In general, it's best to write
a test, verify that it fails, then fix the code which should make the
test pass.

Tests go in ``Pyblosxom/tests/``.


Documentation
=============

New features should come with appropriate changes to the documentation.

Documentation is in the ``docs/`` directory, written using
`restructured text <http://docutils.sourceforge.net/rst.html>`_, and
built with `Sphinx <http://sphinx.pocoo.org/>`_.
