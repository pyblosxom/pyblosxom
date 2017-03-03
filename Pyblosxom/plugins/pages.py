#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2002-2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
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

"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2011-10-22"
__url__ = "http://pyblosxom.github.com/"
__description__ = (
    "Allows you to include non-blog-entry files in your site and have a "
    "non-blog-entry front page.")
__category__ = "content"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


import os
import io
import sys
import os.path
from Pyblosxom.entries.fileentry import FileEntry
from Pyblosxom import tools
from Pyblosxom.tools import pwrap_error


TRIGGER = "pages"
INIT_KEY = "pages_pages_file_initiated"


def verify_installation(req):
    config = req.get_configuration()

    retval = True

    if not 'pagesdir' in config:
        pwrap_error("'pagesdir' property is not set in the config file.")
        retval = False
    elif not os.path.isdir(config["pagesdir"]):
        pwrap_error(
            "'pagesdir' directory does not exist. %s" % config["pagesdir"])
        retval = False

    return retval


def cb_date_head(args):
    req = args["request"]
    data = req.get_data()
    if INIT_KEY in data:
        args["template"] = ""
    return args


def cb_date_foot(args):
    return cb_date_head(args)


def eval_python_blocks(req, body):
    localsdict = {"request": req}
    globalsdict = {}

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    try:
        start = 0
        while body.find("<%", start) != -1:
            start = body.find("<%")
            end = body.find("%>", start)

            if start != -1 and end != -1:
                codeblock = body[start + 2:end].lstrip()

                sys.stdout = io.StringIO()
                sys.stderr = io.StringIO()

                try:
                    exec(codeblock, localsdict, globalsdict)
                except Exception as e:
                    print("ERROR in processing: %s" % e)

                output = sys.stdout.getvalue() + sys.stderr.getvalue()
                body = body[:start] + output + body[end + 2:]

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return body


def is_frontpage(pyhttp, config):
    if not config.get("pages_frontpage"):
        return False
    pathinfo = pyhttp.get("PATH_INFO", "")
    if pathinfo == "/":
        return True
    path, ext = os.path.splitext(pathinfo)
    if path == "/index" and not ext in [".rss20", ".atom", ".rss"]:
        return True
    return False


def is_trigger(pyhttp, config):
    trigger = config.get("pages_trigger", TRIGGER)
    if not trigger.startswith("/"):
        trigger = "/" + trigger

    return pyhttp["PATH_INFO"].startswith(trigger)


def cb_filelist(args):
    req = args["request"]

    pyhttp = req.get_http()
    data = req.get_data()
    config = req.get_configuration()
    page_name = None

    if not (is_trigger(pyhttp, config) or is_frontpage(pyhttp, config)):
        return

    data[INIT_KEY] = 1
    datadir = config["datadir"]
    data['root_datadir'] = config['datadir']
    pagesdir = config["pagesdir"]

    pagesdir = pagesdir.replace("/", os.sep)
    if not pagesdir[-1] == os.sep:
        pagesdir = pagesdir + os.sep

    pathinfo = pyhttp.get("PATH_INFO", "")
    path, ext = os.path.splitext(pathinfo)
    if pathinfo == "/" or path == "/index":
        page_name = "frontpage"
    else:
        page_name = pyhttp["PATH_INFO"][len("/" + TRIGGER) + 1:]

    if not page_name:
        return

    # FIXME - need to do a better job of sanitizing
    page_name = page_name.replace(os.sep, "/")

    if not page_name:
        return

    if page_name[-1] == os.sep:
        page_name = page_name[:-1]
    if page_name.find("/") > 0:
        page_name = page_name[page_name.rfind("/"):]

    # if the page has a flavour, we use that.  otherwise
    # we default to the default flavour.
    page_name, flavour = os.path.splitext(page_name)
    if flavour:
        data["flavour"] = flavour[1:]

    ext = tools.what_ext(list(data["extensions"].keys()), pagesdir + page_name)

    if not ext:
        return []

    data['root_datadir'] = page_name + '.' + ext
    data['bl_type'] = 'file'
    filename = pagesdir + page_name + "." + ext

    if not os.path.isfile(filename):
        return []

    fe = FileEntry(req, filename, pagesdir)
    # now we evaluate python code blocks
    body = fe.get_data()
    body = eval_python_blocks(req, body)
    body = ("<!-- PAGES PAGE START -->\n\n" +
            body +
            "<!-- PAGES PAGE END -->\n")
    fe.set_data(body)

    fe["absolute_path"] = TRIGGER
    fe["fn"] = page_name
    fe["file_path"] = TRIGGER + "/" + page_name
    fe["template_name"] = "pages"

    data['blog_title_with_path'] = (
        config.get("blog_title", "") + " : " + fe.get("title", ""))

    # set the datadir back
    config["datadir"] = datadir

    return [fe]
