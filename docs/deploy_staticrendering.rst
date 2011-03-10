.. _static-rendering:

======================================
Deploy PyBlosxom with Static Rendering
======================================

Summary
=======

Static rendering made its first appearance in PyBlosxom 1.0.  It fills
the functionality gap for people who want to use PyBlosxom, but don't
have a web-server with CGI installed, don't have CGI access, or can't
run PyBlosxom for one of a myriad of other reasons.  Static rendering
allows these people to run PyBlosxom on their local machine, write
blog entries, render their entire site into HTML, and then use ftp or
some other file copy method to move the pages up to their static
website.

PyBlosxom's static rendering allows for incremental building.  It can
scan your entries, figure out what's changed, and render only the
pages that need re-rendering.

Beyond that, it's not particularly sophisticated.


Configuring static rendering
============================

These are the instructions for configuring static rendering in PyBlosxom.

1. **Uncomment ``static_dir`` in your ``config.py`` file.**

   This is the directory we will save all the static output.  The value of 
   ``static_dir`` should be a string representing the **absolute path** of the 
   output directory for static rendering.

2. **Uncomment ``static_flavours`` in your ``config.py`` file.**

   The value of ``static_flavours`` should be a list of strings representing 
   all the flavours that should be rendered.  This defaults to 
   ``[ "html" ]``.

3. **Uncomment ``static_monthnames`` in your ``config.py`` file.**

   The value (either ``1`` or ``0``) will determine if you want month 
   names (such as ``April``) in the static pages.

4. **Uncomment ``static_monthnumbers`` in your ``config.py`` file.**

   The value (either ``1`` or ``0``) will determine if you want month 
   numbers (such as ``04`` for ``April``) in the static pages.

5. **Set ``base_url`` in your ``config.py`` file to the base url your 
   blog will have.**

   For example, if your ``static_dir`` were set to ``/home/joe/public_html`` 
   and the url for that directory were ``http://www.joe.com/~joe/``, then 
   you probably want to set your base_url like this::

      py["base_url"] = "http://www.joe.com/~joe/"


Here's an example of static rendering configuration::

   py["static_dir"] = "/home/joe/public_html/static/"
   py["static_flavours"] = ["html"]
   py["static_monthnames"] = 0     # i do not want month names
   py["static_monthnumbers"] = 1   # i do want month numbers



Running static rendering
========================

There are two ways to run static rendering.  The first is to render
your entire blog from scratch (see "render everything") and the second
is to render only the parts of the blog that will be different because
of new blog entries or updated blog entries (see "incremental rendering").


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

Or, if the location of your ``config.py`` file is on your
``$PYTHONPATH`` then you can run ``pyblosxom-cmd staticrender`` from
any directory without giving the ``--config`` option.

Lots of output will appear as PyBlosxom figures out all the urls that need 
to be rendered and then renders them.


Incremental rendering
---------------------

To find all the entries that have changed since you last rendered
them and then re-render just those entries, do::

   % pyblosxom-cmd staticrender --config </path/to/blog_dir> --incremental

Again the ``</path/to/blog_dir>`` must be the path of the directory
that contains your ``config.py`` file.

Incremental static rendering works by comparing the mtime of the
entry file with the mtime of the rendered file.



Rendering other URIs
====================

Some plugins provide other URIs that are part of your site, but not 
really part of your blog since they're not related to entries.  Examples 
of this include the plugininfo plugin which provides information about 
the plugins that you're running.  You can set the static_urls property 
in config.py to a list of all the urls that need to be rendered every time. 
This list could include:

* RSS, FOAF, OPML, Atom or any other kind of feeds
* urls for plugins that aren't related to entries (plugininfo, 
  pystaticfile, booklist, ...)
* urls for plugins that provide other kinds of indexes (index by tag, 
  index by popularity, ...)


``static_urls`` takes a list of strings where each string is a url to be 
rendered. 

For example if I wanted to render the booklist page and the RSS feed 
for my main page, I would set it like this::

   py["static_urls"] = ["/booklist/index.html", "/index.xml"]

Pitfalls
============

- Both rendering everything and incremental rendering *won't* remove outdated
  files.


Additional thoughts
===================

Static rendering is pretty simplistic. We use the ``tools.render_url`` 
function to render each url.  Plugins that need to re-render the entry 
pages because something has changed (e.g. comments, pingbacks, ...), 
should call this function.

If you want to statically render your blog every night, you could write 
a shell script like this::

   #!/bin/bash 

   CONFIG=<path to directory containing config.py here>
   STATIC_DIR=<your static dir here>
 
   pyblosxom-cmd staticrender --config ${CONFIG}
   find ${STATIC_DIR} -mmin +30 -exec 'rm' '{}' ';' 


That'll re-render everything, then delete any files in your static 
dir that are older than 30 minutes in case you moved entries from 
one category to another or deleted an entry or something along those
lines.  Be careful.  If you have copied other files (CSS, images, etc)
to the ``static_dir`` manually before, you will lose them!


.. Note::

   A note about other files:

   If your website requires more files than just the ones that are rendered 
   by PyBlosxom (images, CSS, ...), then you should copy those over with 
   your shell script as well.
