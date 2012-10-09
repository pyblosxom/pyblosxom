.. _static-rendering:

======================================
Deploy Pyblosxom with Static Rendering
======================================

Summary
=======

Static rendering made its first appearance in Pyblosxom 1.0.  It fills
the functionality gap for people who want to use Pyblosxom, but don't
have a web server with CGI installed, don't have CGI access, or can't
run Pyblosxom for one of a myriad of other reasons.  Static rendering
allows these people to run Pyblosxom on their local machine, write
blog entries, render their entire site into HTML, and then use ftp or
some other file copy method to move the pages up to their static
website.

Pyblosxom's static rendering also allows for incremental building.  It
can scan your entries, figure out what's changed, and render only the
pages that need re-rendering.


Configuring static rendering
============================

These are the instructions for configuring static rendering in Pyblosxom.

1. Uncomment ``static_dir`` in your ``config.py`` file.

   This is the directory we will save all the static output.  The value of 
   ``static_dir`` should be a string representing the **absolute path** of the 
   output directory for static rendering.

   For example, Joe puts the output in his ``public_html`` directory of his
   account::

      py["static_dir"] = "/home/joe/public_html"


2. (optional) Uncomment ``static_flavours`` in your ``config.py`` file.

   The value of ``static_flavours`` should be a list of strings representing 
   all the flavours that should be rendered.

   Defaults to ``["html"]`` which only renders the html flavour.

   For example::

      py["static_flavours"] = ["html"]

3. (optional) Uncomment ``static_index_flavours`` in your ``config.py`` file.

   ``static_index_flavours`` is just like ``static_flavours`` except
   it's the flavours of the index files: frontpage index, category
   indexes, date indexes, ...

   Defaults to ``["html"]`` which only renders the html flavour.

   For example::

     py["static_index_flavours"] = ["html"]

   If you want your index files to also be feeds, then you should add
   a feed flavour to the list.

4. (optional) Uncomment ``static_monthnames`` in your ``config.py`` file.

   The value (either ``True`` or ``False``) will determine if you want
   month names (such as ``April``) in the static pages.

   Defaults to True.

   For example::

      py["static_monthnames"] = False

5. Uncomment ``static_monthnumbers`` in your ``config.py`` file.

   The value (either ``True`` or ``False``) will determine if you want
   month numbers (such as ``04`` for ``April``) in the static pages.

   Defaults to False.

   For example::

      py["static_monthnumbers"] = False

6. Set ``base_url`` in your ``config.py`` file to the base url your 
   blog will have.

   For example, if your ``static_dir`` were set to
   ``/home/joe/public_html`` and the url for that directory were
   ``http://example.com/~joe/``, then you probably want to set your
   base_url like this::

      py["base_url"] = "http://example.com/~joe/"


Here's an example of static rendering configuration::

   py["static_dir"] = "/home/joe/public_html/static/"
   py["static_flavours"] = ["html"]
   py["static_index_flavours"] = ["html", "atom"]
   py["static_monthnames"] = False    # I do not want month names
   py["static_monthnumbers"] = True   # I do want month numbers



Running static rendering
========================

There are two ways to run static rendering.  The first is to render
your entire blog from scratch (see :ref:`render-everything`) and the
second is to render only the parts of the blog that will be different
because of new blog entries or updated blog entries (see
:ref:`incremental-rendering`).


.. _render-everything:

Render everything
-----------------

To render all pages in your blog, ``cd`` into the directory that
contains your ``config.py`` file and run::

   % pyblosxom-cmd staticrender

Or from any directory run::

   % pyblosxom-cmd staticrender --config </path/to/blog_dir>

where ``</path/to/blog_dir>`` is replaced by the path of the directory
that contains your ``config.py`` file.  For example::

   % pyblosxom-cmd staticrender --config /home/joe/blog/

Or, if the location of your ``config.py`` file is in your
``PYTHONPATH`` (an environment variable) then you can run
``pyblosxom-cmd staticrender`` from any directory without giving the
``--config`` option.

Lots of output will appear as Pyblosxom figures out all the urls that
need to be rendered and then renders them.


.. _incremental-rendering:

Incremental rendering
---------------------

To find all the entries that have changed since you last rendered them
and then re-render just those entries, do what you did in
:ref:`render-everything`, but tack on ``--incremental`` to the end.

Incremental static rendering works by comparing the mtime of the entry
file with the mtime of the rendered file.


Rendering other URLs
====================

Some plugins provide other URLs that are part of your site, but not
really part of your blog since they're not related to entries.
Examples of this include the plugininfo plugin which provides
information about the plugins that you're running.  You can set the
static_urls property in config.py to a list of all the urls that need
to be rendered every time.  This list could include:

* RSS, FOAF, OPML, Atom or any other kind of feeds
* urls for plugins that aren't related to entries (plugininfo,
  pystaticfile, booklist, ...)
* urls for plugins that provide other kinds of indexes (index by tag,
  index by popularity, ...)


``static_urls`` takes a list of strings where each string is a url to
be rendered.

For example if I wanted to render the booklist page and the RSS feed
for my main page, I would set it like this::

   py["static_urls"] = [
       "/index.xml",            # blog feed
       "/pages/about.html",     # about this blog page
       "/booklist/index.html",  # list of books I've read
       ]


Things to note
==============

* Both rendering everything and incremental rendering *won't* remove
  outdated files.

* You probably don't want to render an rss or Atom version of every
  page, so don't include those flavours in ``static_flavours`` and
  instead specify the urls by hand in ``static_urls``.

* If your website requires more files than just the ones that are
  rendered by Pyblosxom (images, CSS, ...), then you need to copy
  those files over separately---Pyblosxom won't do it for you.


Example setup
=============

I have all my blog files located in ``/home/joe/blog/``.

My blog consists of blog entries and also a CSS file, a JavaScript
file, and a bunch of images.

My directory layout looks like::

   blog/
     |- www/
     |  |- images/
     |  |- css/
     |  \- js/
     |
     |- entries/       # all my blog entries
     |- flavourdir/    # flavours and templates
     |- plugins/       # a couple of plugins I use
     |
     |- config.py      # my config.py file
     \- compile.sh     # shell script below


I render my blog to ``/home/joe/public_html``.

I like having my blog updated nightly---that gives me time to write
entries during the day at my leisure and they all appear the next day.
I do this by having a ``compile.sh`` that gets run by cron every
night.

The script looks like this:

.. code-block:: bash

   #!/bin/bash 

   BLOGDIR=/home/joe/blog
   OUTPUTDIR=/home/joe/public_html
 
   # incrementally render entire blog
   pyblosxom-cmd staticrender --config ${BLOGDIR} --incremental

   # copy static files (images, css, ...)
   cp -ar ${BLOGDIR}/www/* ${OUTPUTDIR}
