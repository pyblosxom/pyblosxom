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
  manipulate entries.  You can use existing tools (version control,
  shell scripting, procmail, ...) for blog management.

**extensibility**

  PyBlosxom has a plugin framework allowing you to use plugins to
  augment ane enhance PyBlosxom's default behavior.  Plugins are
  written in Python.  We maintain a list of plugins in the plugin
  registry on the website.

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
community, it's pretty small.  PyBlosxom is a pretty niche weblog
engine.

PyBlosxom is a *file-based* weblog system.  Blog entries are stored as
separate files in a directory hierarchy on the filesystem.  By
default, the hierarchy is a category tree meaning each entry belongs
in a single category.  By default, mtimes are used as the entry
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


Basic overview
==============

PyBlosxom is a file-based weblog system.  Each entry is a single text
file in a directory hierarchy.  The directory tree is the category
tree for entries and is called your *datadir*.

PyBlosxom has themeing.  Themes are called *flavours*.  A flavour is a
group of templates.  PyBlosxom comes with a bunch of flavours by
default, but they're pretty basic.  For more information about
flavours, see ``flavours_and_templates``.  The `PyBlosxom web-site`_
maintains a flavour registry for flavours submitted by people like
you.

PyBlosxom allows you to change its behavior with plugins.  For more
information on plugins, see pages on plugins, writing plugins and
PyBlosxom architecture.  The `PyBlosxom web-site`_ maintains a plugin
registry for plugins submitted by people like you.

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
