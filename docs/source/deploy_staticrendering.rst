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
web-site.

PyBlosxom's static rendering allows for incremental building.  It can
scan your entries, figure out what's changed, and render only the
pages that need re-rendering.

Beyond that, it's not particularly sophisticated.


Configuring Static Rendering
============================

These are the instructions for configuring static rendering in PyBlosxom.

1. **Install PyBlosxom.**

   You can install PyBlosxom as a Python library like this::

      easy_install pyblosxom

   and move on to step 2.

   If you can't or don't want to do that, then just untar the pyblosxom
   .tar.gz file into a directory.

   If you're using a version of PyBlosxom prior to 1.4, when you're
   copying the ``pyblosxom.cgi`` and ``config.py`` files, you don't
   have to put them in a CGI directory---you can put them in any
   directory you have permissions in.

   For example, I created a directory ``/home/joe/pyblosxom/`` and put 
   both files in there.

   If you're using PyBlosxom 1.4 or later, copy ``bin/pyblosxom-cmd`` and
   ``web/config.py``.

2. **Add ``static_dir`` to your ``config.py`` file.**

   This is the directory we will save all the static output.  The value of 
   ``static_dir`` should be a string representing the absolute path of the 
   output directory for static rendering.

3. **Add ``static_flavours`` to your ``config.py`` file.**

   The value of ``static_flavours`` should be a list of strings representing 
   all the flavours that should be rendered.  This defaults to 
   ``[ "html" ]``.

4. **Add ``static_monthnames`` to your ``config.py`` file.**

   The value (either ``1`` or ``0``) will determine if you want month 
   names (such as ``April``) in the static pages.

5. **Add ``static_monthnumbers`` to your ``config.py`` file.**

   The value (either ``1`` or ``0``) will determine if you want month 
   numbers (such as ``04`` for ``April``) in the static pages.

6. **Set ``base_url`` in your ``config.py`` file to the base url your 
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



Running Static Rendering
========================

There are two ways to run static rendering.  The first is to render
your entire blog from scratch (see "render everything") and the second
is to render only the parts of the blog that will be different because
of new blog entries or updated blog entries (see "incremental rendering").


Render Everything
-----------------

If you're using PyBlosxom 1.4 or later, run the static renderer like
this to render all pages in your blog::

   % pyblosxom-cmd --config <config-file> staticrender


where ``<config-file>`` is replaced by the absolute full path of your
``config.py`` file.  For example::

   % pyblosxom-cmd --config /home/joe/blog/config.py staticrender


**PyBlosxom 1.4**: If you're using PyBlosxom 1.4, then the command line 
is slightly different::

   % pyblcmd --config /home/joe/blog/config.py --static


**Before PyBlosxom 1.4**: If you're using a version of PyBlosxom earlier 
than 1.4, then the ``config.py`` file must be in the same directory 
as the ``pyblosxom.cgi`` file::

   % ./pyblosxom.cgi --static


Lots of output will appear as PyBlosxom figures out all the urls that need 
to be rendered and then renders them.



Incremental Rendering
---------------------

We have incremental rendering which will find all the entries that have 
changed since we rendered them and then re-render them.  It does this by 
comparing the mtime on the entry file with the mtime on the rendered file.

In PyBlosxom 1.5 and later, incremental static rendering works like this::

   % pyblosxom-cmd --config <config-file> staticrender --incremental


**PyBlosxom 1.4**: If you're using PyBlosxom 1.4, run the static renderer 
like this to render new pages in your blog::

   % pyblcmd --config <config-file> --static incremental
   

**Before PyBlosxom 1.4**: If you're using a version of PyBlosxom earlier 
than 1.4, then run the static renderer like this::

   % ./pyblosxom.cgi --static --incremental 



Rendering Other URIs
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



Additional Thoughts
===================

Static rendering is pretty simplistic. We use the ``tools.render_url`` 
function to render each url.  Plugins that need to re-render the entry 
pages because something has changed (e.g. comments, pingbacks, ...), 
should call this function.

If you want to statically render your blog every night, you could write 
a shell script like this::

   #!/bin/bash 

   CONFIG=<path to config.py here>
   STATIC_DIR=<your static dir here>
 
   pyblosxom-cmd --config ${CONFIG} static
   find ${STATIC_DIR} -mmin +30 -exec 'rm' '{}' ';' 


That'll re-render everything, then delete any files in your static 
dir that are older than 30 minutes in case you moved entries from 
one category to another or deleted an entry or something along those
lines.


.. Note::

   A note about other files:

   If your web-site requires more files than just the ones that are rendered 
   by PyBlosxom (images, CSS, ...), then you should copy those over with 
   your shell script as well.
