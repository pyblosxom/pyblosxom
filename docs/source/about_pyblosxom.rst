===============
About PyBlosxom
===============

PyBlosxom is a lightweight weblog system.  It was originally a Python
clone of `Blosxom`_ but has since evolved into a weblog system of its
own reminiscent of `Blosxom`_.

.. _Blosxom: http://www.blosxom.com/

PyBlosxom focuses on three things:

**simplicity**

  PyBlosxom stores all data on the file system in plain text files.
  This allows you to use any text editor to create, update and
  manipulate entries.  You can also use existing text-manipulation
  tools, version control, scripts, grep, ...  for managing your blog.

  PyBlosxom can run as a CGI script, WSGI component or you can use it
  to statically compile your web-site into HTML/XML files.

  Your workflow is your workflow.

**extensibility**

  PyBlosxom has a plugin framework enabling you to augment and enhance
  PyBlosxom's default behavior.  Plugins are written in Python.  We
  maintain a list of plugins in the plugin registry on the website.

  Plugins aren't hard to write.  We're happy to help you write
  plugins.

**community**

  There are several hundred PyBlosxom users out there all of whom have
  different needs.  PyBlosxom is used on a variety of operating
  systems in a variety of environments.  We have the standard open
  source project fare: mailing lists, IRC channel, wiki, ...

PyBlosxom is built to let you use existing text-manipulation tools
without having to build the whole ecology from scratch.


Why you wouldn't want to use PyBlosxom
======================================

PyBlosxom is a small open source project and while there is a
community, it's pretty small.  PyBlosxom's features are great
but make it a niche weblog engine.

PyBlosxom is a *file-based* weblog system.  Each blog entry is a separate
file stored in a directory hierarchy on your file system.
By default, the hierarchy is a category tree meaning each blog entry belongs
in a single category.  By default, mtimes are used as the blog entry
timestamp.  There are plugins that change this behavior, but require
extra configuration to use.

There are a lot of other weblog systems out there.  If it's apparent
that PyBlosxom won't work for you, don't force it--use something else.
Possibilities include:

**WordPress**

    http://wordpress.org/

    PHP/database based weblog system that a lot of people use.

**Zine**

    http://zine.pocoo.org/

    Python-based weblog system that's a lot like WordPress, but it's
    written in Python and supports Python plugins.

**ikiwiki**

    http://ikiwiki.info/

    ikiwiki is written in Perl and melds blogging with wiki with
    version control storage.


Overview of PyBlosxom
=====================

Entries, categories, storage:

* PyBlosxom stores everything as files on the file system--there is no
  database
* Each blog entry is a file.
* Blog entry files are stored in a directory hierarchy in your *datadir*.
* Each subdirectory in your *datadir* corresponds to a category of
  your blog.

Themes:

* Themes in PyBlosxom are called *flavours*.
* A flavour consists of a set of templates.
* Flavours are stored in a directory called the *flavourdir*.
* PyBlosxom comes with several flavours: html, rss20, and atom.
* The `PyBlosxom web-site`_ maintains a flavour registry for flavours
  contributed by people like you.
* There's more information in the chapter on
  :ref:`Flavours and Templates <flavours-and-templates>`.

Plugins:

* PyBlosxom has a plugin system.
* Plugins are written in Python.
* Plugins are loaded using the ``plugin_dirs`` and ``load_plugins``
  configuration variables.
* For more information on using plugins see
  :ref:`Plugins <using-plugins>`.
* For more information on writing plugins see
  :ref:`Writing Plugins <writing-plugins>`.
* The `PyBlosxom web-site`_ maintains a plugin registry for plugins 
  submitted by people like you.

.. _PyBlosxom web-site: http://pyblosxom.sourceforge.net/


.. _project-details-and-contact:

Project details, contact information, and where to go for help
==============================================================

**Web-site and documentation**

    http://pyblosxom.sourceforge.net/

**IRC**

    ``#pyblosxom`` on ``irc.freenode.net``

**User mailing list**

    http://lists.sourceforge.net/lists/listinfo/pyblosxom-users

**Developer mailing list**

    http://lists.sourceforge.net/lists/listinfo/pyblosxom-devel

**SVN repository**

    http://pyblosxom.svn.sourceforge.net/viewvc/pyblosxom/
