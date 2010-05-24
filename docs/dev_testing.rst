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
core functionality.

Tests are executed by::

   python setup.py test

This uses the ``test_suite`` parameter to setup which is in both
distribute and setuptools.

The ``test_suite`` is ``Pyblosxom.tests.testrunner.test_suite`` which
is a function that goes through all the files in ``Pyblosxom/tests/``
and loads tests in files where the filename starts with ``test_`` and
ends in ``.py``.

There's a helper module which has a UnitTestBase derived from
``unittest.TestCase`` which has some helper functions for building a
blog setup, tearing it down, building a ``Request`` object, and
comparing two dicts where one must be a subset the other.

Writing tests for the core is pretty easy:

1. create a file in ``Pyblosxom/tests/`` with a filename that starts with
   ``test_`` and ends with ``.py``.

2. import ``UnitTestBase`` from ``Pyblosxom.tests.helpers``

3. create a subclass of ``UnitTestBase``

4. write some tests using pretty standard unittest stuff

There are a bunch of existing examples in the directory.


Testing plugins
===============

Plugins are a lot harder because we want to make sure they remain
modular and easy to install.  "Easy to install" really means that a
plugin is a single monolithic file.  I didn't want to have a ton of
testing code in the modules, so I wrote the test harness to allow for
plugins to have tests in the plugin as well as tests in a parallel tests
directory.

To run all the plugin tests, I do something like this::

    PYTHONPATH=. python plugins/testrunner.py


Tests in the plugin file
------------------------

Testing inside a plugin is pretty limited because you can't take
advantage of the helper infrastructure--you're limited to what you can
load from Python and PyBlosxom core.

1. import ``unittest``

2. create a class that extends ``unittest.TestCase``

3. write your tests in that

4. create a function at the module level called ``get_test_suite``
   that returns the tests loaded from the test class(es)

For an example, look at ``plugins/date/w3cdate.py``.


Tests in the parallel directory
-------------------------------

Writing tests in the parallel directory has the benefit of being able to
use helper infrastructure, but the cost of being separate from the
actual plugin.  I think this is ok, but it's something that we have to
keep in mind when we make plugin fixes.

Tests are located in ``plugins/tests/`` and are in a parallel
directory structure to the plugins in ``plugins/`` .

For example, the test_acronyms.py test file is in
``plugins/tests/text/test_acronyms.py`` and the plugin is in
``plugins/text/acronyms.py``.

Test files should import ``PluginTest`` from
``plugins.test.test_base``.  This class has a bunch of helper
functions for dealing with request objects, creating blog data,
flavours, ...

1. import ``PluginTest`` from ``plugins.test.test_base``

2. create a class that extends ``PluginTest``

3. write your tests in that

4. edit ``plugins/tests/__init__.py`` and add a line to import things
   from your new test module


For examples, see files in ``plugins/test/``.

Summary
=======

I think that's it.  It definitely seems more complicated than it is.
Generally speaking, the test infrastructure is ok, but not
fantastically amazing.  It'll evolve over time as we need it to do
more.

Speaking of doing more, there are parts of PyBlosxom that could use
better testing.  Help on this front would be fantastic.

Having said that, adding tests for the code we're writing helps us a
TON in the quality department.  PyBlosxom 1.5 is ten times as good as
previous versions because we've got a better testing infrastructure 
and we're testing plugin functionality.

Many thanks to Ryan Barret for the awesome work he did a while back.
The infrastructure we have now is based largely on his efforts.
