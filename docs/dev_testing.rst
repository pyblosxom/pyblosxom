.. highlight:: python
   :linenothreshold: 5

=======
Testing
=======

In the pyblosxom git repository, there are two big things that have
test suites:

1. the PyBlosxom core code
2. the plugins that are in plugins/

These have two separate testing infrastructures, but both are based on
unittest which comes with Python.


PyBlosxom core code testing
===========================

These tests are located in ``Pyblosxom/tests/`` and test the PyBlosxom
core functionality and all core plugins.

Tests are executed by::

   python setup.py test

This uses the ``test_suite`` parameter to setup which is in both
distribute and setuptools.

The ``test_suite`` is ``Pyblosxom.tests.testrunner.test_suite`` which
is a function that goes through all the files in ``Pyblosxom/tests/``
and loads tests in files where the filename starts with ``test_`` and
ends in ``.py``.

The ``Pyblosxom.tests`` package defines helper functions, classes, and
other things to make testing easier.

Writing tests is pretty easy:

1. create a file in ``Pyblosxom/tests/`` with a filename that starts
   with ``test_`` and ends with ``.py``.

2. import ``UnitTestBase`` from ``Pyblosxom.tests``

3. create a subclass of ``UnitTestBase``

4. write some tests using pretty standard unittest stuff

See ``Pyblosxom/tests/`` for examples testing the core as well as core
plugins.


Summary
=======

That's about it!

Writing tests is a great way to start contributing to this project and
it will help you learn the code base.  If you're at all interested,
let us know!

Adding tests for the code we're writing helps us a TON in the quality
department.  PyBlosxom 1.5 is ten times as good as previous versions
because we've got a better testing infrastructure and we're testing
plugin functionality.

Many thanks to Ryan Barret for the awesome work he did a while back
writing tests for plugins.
