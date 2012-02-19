
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

================================================
 pages - Allows you to include non-blog-entr... 
================================================

Summary
=======

Blogs don't always consist solely of blog entries.  Sometimes you want
to add other content to your blog that's not a blog entry.  For
example, an "about this blog" page or a page covering a list of your
development projects.

This plugin allows you to have pages served by Pyblosxom that aren't
blog entries.

Additionally, this plugin allows you to have a non-blog-entry front
page.  This makes it easier to use Pyblosxom to run your entire
website.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. add ``Pyblosxom.plugins.pages`` to the ``load_plugins`` list in
   your ``config.py`` file.

2. configure the plugin using the configuration variables below


``pagesdir``

    This is the directory that holds the pages files.

    For example, if you wanted your pages in
    ``/home/foo/blog/pages/``, then you would set it to::

        py["pagesdir"] = "/home/foo/blog/pages/"

    If you have ``blogdir`` defined in your ``config.py`` file which
    holds your ``datadir`` and ``flavourdir`` directories, then you
    could set it to::

        py["pagesdir"] = os.path.join(blogdir, "pages")


``pages_trigger`` (optional)

    Defaults to ``pages``.

    This is the url trigger that causes the pages plugin to look for
    pages.

        py["pages_trigger"] = "pages"


``pages_frontpage`` (optional)

    Defaults to False.

    If set to True, then pages will show the ``frontpage`` page for
    the front page.

    This requires you to have a ``frontpage`` file in your pages
    directory.  The extension for this file works the same way as blog
    entries.  So if your blog entries end in ``.txt``, then you would
    need a ``frontpage.txt`` file.

    Example::

        py["pages_frontpage"] = True


Usage
=====

Pages looks for urls that start with the trigger ``pages_trigger``
value as set in your ``config.py`` file.  For example, if your
``pages_trigger`` was ``pages``, then it would look for urls like
this::

    /pages/blah
    /pages/blah.html

and pulls up the file ``blah.txt`` [1]_ which is located in the path
specified in the config file as ``pagesdir``.

If the file is not there, it kicks up a 404.

.. [1] The file ending (the ``.txt`` part) can be any file ending
   that's valid for entries on your blog.  For example, if you have
   the textile entryparser installed, then ``.txtl`` is also a valid
   file ending.


Template
========

pages formats the page using the ``pages`` template.  So you need a
``pages`` template in the flavours that you want these pages to be
rendered in.  I copy my ``story`` template and remove some bits.

For example, if you're using the html flavour and that is stored in
``/home/foo/blog/flavours/html.flav/``, then you could copy the
``story`` file in that directory to ``pages`` and that would become
your ``pages`` template.


Python code blocks
==================

pages handles evaluating python code blocks.  Enclose python code in
``<%`` and ``%>``.  The assumption is that only you can edit your
pages files, so there are no restrictions (security or otherwise).

For example::

   <%
   print "testing"
   %>

   <%
   x = { "apple": 5, "banana": 6, "pear": 4 }
   for mem in x.keys():
      print "<li>%s - %s</li>" % (mem, x[mem])
   %>

The request object is available in python code blocks.  Reference it
by ``request``.  Example::

   <%
   config = request.get_configuration()
   print "your datadir is: %s" % config["datadir"]
   %>


License
=======

Plugin is distributed under license: MIT
