#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
# 2011 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Usage
=====

A blog consists of blog entries, plus a bunch of pages that exist outside
of the blog structure.  For example, an "About me" page or a "Guestbook"
page.  These last two shouldn't be blog entries.  Well, if they're not
blog entries, then how can you have them in your blog?

This plugin solves that problem.  It allows you to have pages in your
website that aren't blog entries that are served up by PyBlosxom.  These
pages can also have plugins.

It looks for urls like::

   /pages/blah

and pulls up the file ``blah.txt`` [1]_ which is located in the path specified
in the config file as ``pagesdir``.  If no pagesdir is specified, then we
use the datadir.

If the file is not there, it kicks up a 404.

.. [1] The file ending (the ``.txt`` part) can be any file ending that's 
   valid for entries on your blog.  For example, if you have the textile
   entryparser installed, then ``.txtl`` is also a valid file ending.

pages formats the page using the ``pages`` template.
So you need to add a ``pages.html`` file to your datadir (assuming
you're using the ``html`` flavour).  I tend to copy my story flavour
templates over and remove the date/time-related bits.

pages handles evaluating python code blocks.  Enclose python
code in ``<%`` and ``%>``.  The assumption is that only you can edit your 
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


Configuration
=============

``pagesdir``

    This is the directory that holds the pages files.

    For example, if you wanted your pages in ``/home/foo/blog/pages/``, then
    you would set it to::

        py["pagesdir"] = "/home/foo/blog/pages/"

    If you have ``blogdir`` defined in your ``config.py`` file which holds
    your ``datadir`` and ``flavourdir`` directories, then you could set it
    to::

        py["pagesdir"] = os.path.join(blogdir, "pages")

``pages_trigger``

    Optional.  Defaults to ``pages``.

    This is the url trigger that causes the pages plugin to look for pages.

``pages_frontpage``

    Optional.  Defaults to False.

    If set to True, then pages will show the ``frontpage`` page for the 
    front page.

    This requires you to have a ``frontpage`` file in your pages directory.
    The extension for this file works the same way as blog entries.  So if
    your blog entries end in ``.txt``, then you would need a ``frontpage.txt``
    file.
"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2011-01-13"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "Allows you to include non-blog-entry files in your site."
__category__ = "content"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


import os
import StringIO
import sys
import os.path
from Pyblosxom.entries.fileentry import FileEntry
from Pyblosxom import tools


TRIGGER = "pages"
INIT_KEY = "pages_pages_file_initiated"

def verify_installation(req):
    config = req.get_configuration()

    retval = 1

    if not config.has_key("pagesdir"):
        print "'pagesdir' property is not set in the config file."
        retval = 0
    elif not os.path.isdir(config["pagesdir"]):
        print "'pagesdir' directory does not exist. %s" % config["pagesdir"]
        retval = 0

    return retval
 
def cb_date_head(args):
    req = args["request"]
    data = req.get_data()
    if data.has_key(INIT_KEY):
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
                codeblock = body[start+2:end].lstrip()

                sys.stdout = StringIO.StringIO()
                sys.stderr = StringIO.StringIO()

                try:
                    exec codeblock in localsdict, globalsdict
                except Exception, e:
                    print "ERROR in processing: %s" % e

                output = sys.stdout.getvalue() + sys.stderr.getvalue()
                body = body[:start] + output + body[end+2:]

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return body
 
def is_frontpage(pyhttp, config):
    return pyhttp["PATH_INFO"].startswith("/index") and config.get("pages_frontpage", False)

def is_trigger(pyhttp, config):
    return pyhttp["PATH_INFO"].startswith("/" + config.get("pages_trigger", TRIGGER))

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
    pagesdir = config.get("pagesdir", config['datadir'])

    pagesdir = pagesdir.replace("/", os.sep)
    if not pagesdir[-1] == os.sep:
        pagesdir = pagesdir + os.sep

    if pyhttp["PATH_INFO"].startswith("/index"):
        page_name = "frontpage"
    else:
        page_name = pyhttp["PATH_INFO"][len("/" + TRIGGER)+1:]

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
    # we default to the static flavour
    page_name, flavour = os.path.splitext(page_name)
    if flavour:
        data["flavour"] = flavour[1:]

    # we build our own config dict for the fileentry to kind of
    # fake it into loading this file correctly rather than
    # one of the entries.
    # newdatadir = pagesdir
    # config["datadir"] = newdatadir

    ext = tools.what_ext(data["extensions"].keys(), pagesdir + page_name)

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
    body = "<!-- PAGES PAGE START -->\n\n" + body + "<!-- PAGES PAGE END -->\n"
    fe.set_data(body)

    fe["absolute_path"] = TRIGGER
    fe["fn"] = page_name
    fe["file_path"] = TRIGGER + "/" + page_name
    fe["template_name"] = "static"

    data['blog_title_with_path'] = (config.get("blog_title", "") + 
                                    " : " + fe.get("title", ""))

    # set the datadir back
    config["datadir"] = datadir

    return [fe]
