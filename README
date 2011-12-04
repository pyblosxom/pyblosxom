=================
 About Pyblosxom
=================

What is Pyblosxom
=================

Pyblosxom is a lightweight blog system.  It was originally a Python
clone of `Blosxom`_ but has since evolved into a blog system of its
own reminiscent of `Blosxom`_.

.. _Blosxom: http://www.blosxom.com/

Pyblosxom focuses on three things:

**simplicity**

  Pyblosxom stores all data on the file system in plain text files.
  This allows you to use any text editor to create, update and
  manipulate entries.  You can also use existing text-manipulation
  tools, version control, scripts, grep, ...  for managing your blog.

  Pyblosxom can run as a CGI script, WSGI component or you can use it
  to statically compile your website into HTML/XML files.

  Your workflow is your workflow.

**extensibility**

  Pyblosxom has a plugin framework enabling you to augment and enhance
  Pyblosxom's default behavior.  Plugins are written in Python.  We
  maintain a list of plugins in the plugin registry on the website.

  Plugins aren't hard to write.  We're happy to help you write
  plugins.

**community**

  There are several hundred Pyblosxom users out there all of whom have
  different needs.  Pyblosxom is used on a variety of operating
  systems in a variety of environments.  We have the standard open
  source project fare: mailing lists, IRC channel, wiki, ...

Pyblosxom is built to let you use existing text-manipulation tools
without having to build the whole ecology from scratch.

Pyblosxom can be run as:

* a "static renderer" and compile your blog
* a CGI script
* a WSGI application

You can learn more about Pyblosxom on the `website`_.

.. _website: http://pyblosxom.bluesock.org/


Why you might not want to use Pyblosxom
=======================================

Pyblosxom is a small open source project and while there is a
community, it's pretty small.  Pyblosxom's features are great but make
it a niche blog system.

Pyblosxom is a *file-based* blog system.  Each blog entry is a
separate file stored in a directory hierarchy on your file system.  By
default, the hierarchy is a category tree meaning each blog entry
belongs in a single category.  By default, mtimes are used as the blog
entry timestamp.  There are plugins that change this behavior, but
require extra configuration to use.

There are a lot of other blog systems out there.  If it's apparent
that Pyblosxom won't work for you, don't force it---use something
else.


Overview of Pyblosxom
=====================

Entries, categories, storage:

* Pyblosxom stores everything as files on the file system---there is
  no database.
* Each blog entry is a file.
* Blog entry files are stored in a directory hierarchy in your *datadir*.
* Each subdirectory in your *datadir* corresponds to a category of
  your blog.

Themes:

* Themes in Pyblosxom are called *flavours*.
* A flavour consists of a set of *templates*.
* Flavours are stored in a directory called the *flavourdir*.
* Pyblosxom comes with several flavours: html, rss20, and atom.
* The `website <http://pyblosxom.bluesock.org/>`_ maintains a flavour
  registry for flavours contributed by people like you.
* .. only:: text

     There's more information on flavours and templates in
     docs/flavours_and_templates.rst.

  .. only:: html or latex

     There's more information on flavours and templates in
     :ref:`flavours-and-templates`.

Plugins:

* Pyblosxom has a plugin system.
* Plugins are written in Python.
* Plugins are loaded using the ``plugin_dirs`` and ``load_plugins``
  configuration variables.
* The `website <http://pyblosxom.bluesock.org/>`_ maintains a plugin
  registry for plugins submitted by people like you.
* .. only:: text

     For more information on using plugins, see the docs.plugins.rst.

  .. only:: html or latex

     For more information on using plugins, see the
     :ref:`using-plugins`.

* .. only:: text

     For more information on writing plugins see the
     docs/dev_writing_plugins.rst.

  .. only:: html or latex

     For more information on using plugins, see the
     :ref:`writing-plugins`.



.. _project-details-and-contact:

Project details, contact information, and where to go for help
==============================================================

See the `website <http://pyblosxom.bluesock.org/>`_ for details on
the mailing lists, IRC, source code, issue tracker, and everything
else.


Requirements
============

* Python 2.5 or higher, but not Python 3
* (optional) Sphinx for building documentation
* (optional) other things depending on what plugins you install


How to install Pyblosxom
========================

.. only:: text

   Read the ``INSTALL`` document as well as other documents in the
   ``docs/`` directory.

   If you're upgrading from a previous Pyblosxom version, read the
   ``UPGRADE`` document as well as ``CHANGELOG`` which covers what's
   new in this version and what you'll need to change in your blog.

.. only:: html

   If you're installing for the first time, read :ref:`install`.

   If you're upgrading, read :ref:`upgrading` and :ref:`whatsnew`.


How to find comprehensive documentation
=======================================

There's a series of text files in the ``docs/`` directory which
comprise the current state of the Pyblosxom manual at the time of this
release.

The most current version of the manual can be found on the `website
<http://pyblosxom.bluesock.org/>`_ .


How to join the community
=========================

Pyblosxom is written for and by people like you.  If you're using
Pyblosxom, please contribute something back whether it's reporting a
bug, fixing something, adding a new flavour, blogging about Pyblosxom,
telling your friends, writing a plugin, or hanging out with us on IRC.

Details on where we hang out and such are on the `website
<http://pyblosxom.bluesock.org/>`_.


How to report bugs, send in patches, fix problems
=================================================

If you have a problem with Pyblosxom, please report it!

There are several different ways to report a bug, but all bugs should
eventually make their way into our issue tracker.

1. Let someone know on IRC: #pyblosxom on irc.freenode.net

2. Send a mail to the pyblosxom-users or pyblosxom-devel mailing
   lists.  Details are on the `website
   <http://pyblosxom.bluesock.org/>`_.

3. Write up a bug report in the issue tracker.  Details are on the
   `website <http://pyblosxom.bluesock.org/>`_.

If you're able to fix the bug, that helps a ton!  Please attach a
patch file to the bug report or send the patch as an attachment to the
pyblosxom-devel mailing list.

When sending a patch, it helps a lot to know the details of the bug as
well as how you fixed it and whether there are outstanding issues.


How to run unit tests
=====================

Tests are written with the Python unittest module and don't require
any additional test frameworks.

To run the tests, do::

    python setup.py test

This will build Pyblosxom, then run the tests.

If you would like to add tests to the test suite, please do and send
us patches!
