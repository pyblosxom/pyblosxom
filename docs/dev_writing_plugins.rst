.. highlight:: python
   :linenothreshold: 5

===============
Writing Plugins
===============

.. _writing-plugins:

Summary
=======

This chapter covers a bunch of useful things to know when writing
PyBlosxom plugins.  This chapter, moreso than the rest of this manual,
is very much a work in progress.

If you need help with plugin development, sign up on the devel mailing
list and/or join us on ``#pyblosxom`` on ``irc.freenode.net``.  More
details in :ref:`project-details-and-contact`.

FIXME - this needs more work


Things that all plugins should have
===================================

This section covers things that all plugins should have.  This makes
plugins easier to distribute, maintain, update, and easier for users
to use them.


Documentation
-------------

All plugins should have a docstring at the top of the file that describes
in detail:

1. what the plugin does
2. how to install it
3. how to configure it
4. the license the plugin is distributed under
5. and any copyright information you have
6. any notes about requirements (e.g. "Requires Python 2.3 or greater")

For example, this is at the top of Will's wbgpager plugin::

   """
   Quickly written plugin for paging long index pages.  

   PyBlosxom uses the num_entries configuration variable to prevent
   more than num_entries being rendered by cutting the list down
   to num_entries entries.  So if your num_entries is set to 20, you
   will only see the first 20 entries rendered.

   The wbgpager overrides this functionality and allows for paging.
   It does some dirty stuff so that PyBlosxom doesn't cut the list down
   and then wbgpager cuts it down in the prepare callback later down
   the line.

   To install wbgpager, do the following:

     1. add "wbgpager" to your load_plugins list variable in your
        config.py file---make sure it's the first thing listed so
        that it has a chance to operate on the entry list before
        other plugins.
     2. add the $page_navigation variable to your head or foot
        (or both) templates.  this is where the page navigation
        HTML will appear.


   Here are some additional configuration variables to adjust the 
   behavior:

     wbgpager_count_from
       datatype:       int
       default value:  0
       description:    Some folks like their paging to start at 1---this
                       enables you to do that.

     wbgpager_previous_text
       datatype:       string
       default value:  &lt;&lt;
       description:    Allows you to change the text for the prev link.

     wbgpager_next_text
       datatype:       string
       default value:  &gt;&gt;
       description:    Allows you to change the text for the next link.

     wbgpager_linkstyle
       datatype:       integer
       default value:  0
       description:    This allows you to change the link style of the paging.
                       style 0:  [1] 2 3 4 5 6 7 8 9 ... >>
                       style 1:  Page 1 of 4 >>


   That should be it!


   Note: This plugin doesn't work particularly well with static rendering.
   The problem is that it relies on the querystring to figure out which
   page to show and when you're static rendering, only the first page
   is rendered.  This will require a lot of thought to fix.  If you are
   someone who is passionate about fixing this issue, let me know.


   Permission is hereby granted, free of charge, to any person
   obtaining a copy of this software and associated documentation
   files (the "Software"), to deal in the Software without restriction,
   including without limitation the rights to use, copy, modify,
   merge, publish, distribute, sublicense, and/or sell copies of the
   Software, and to permit persons to whom the Software is furnished
   to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be
   included in all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
   CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.

   Copyright 2004, 2005, 2006 Will Kahn-Greene
   """

Metadata
--------

All plugins should have the following module-level variables 
defined in them just after the docstring:

* ``__author__`` - This holds your name and email address
  so that people can contact you when they have problems.

* ``__version__`` - This holds the version number and release
  date so that people know what version of the plugin they're looking 
  at.

* ``__url__`` - This holds the url where people can find information
  about your plugin and documentation and download new versions of your
  plugin.

* ``__description__`` - This is a one-sentence description of what your 
  plugin does.


For example::

   __author__      = "Will Kahn-Greene - willg at bluesock dot org"
   __version__     = "version 1.5 2006-01-15"
   __url__         = "http://www.bluesock.org/~willg/pyblosxom/"
   __description__ = "Splits long indexes into multiple pages."


Configuration, installation and verification
--------------------------------------------

After that, you should have a ``verify_installation`` section that
verifies that the plugin is configured correctly.  As of PyBlosxom 0.9, 
PyBlosxom allows users to test their configuration and installation from
the console.

You can test using either the ``pyblosxom.cgi``
script or the ``pyblosxom-cmd`` script::

    % ./pyblosxom.cgi test

or::

    $ ./pyblcmd_dev.sh test --config ./newblog/
    pyblosxom-cmd version 1.5 dev
    Adding ./newblog/ to sys.path....
    Trying to import the config module....
    System Information
    ==================
    
    - pyblosxom:    1.5 dev
    - sys.version:  2.6.4 (r264:75706, Dec  7 2009, 18:45:15)  [GCC 4.4.1]
    - os.name:      posix
    - codebase:     /home/willg/projects/pyblosxom/trunk/pyblosxom

    Checking config.py file
    =======================
    - properties set: 21
    - datadir '/home/willg/projects/pyblosxom/testing/newblog/entries' exists.

    Checking plugin configuration
    =============================
    ....


This goes through and verifies the properties in the ``config.py``
file as best as it can.  It also prints out diagnostic information
which is useful when things don't work.  It also loads and initializes
all the plugins and asks them to verify their configurations as best
they can.

As a plugin developer, you should add a ``verify_installation``
function to your plugin module.  Something like this (taken from
pycategories)::

    def verify_installation(request):
        config = request.get_configuration()

        if not config.has_key("category_flavour"):
            print "missing optional config property 'category_flavour' "
            print "which allows you to specify the flavour for the category "
            print "link.  refer to pycategory plugin documentation for more "
            print "details."
        return 1


This gives you (the plugin developer) the opportunity to walk the user
through configuring your highly complex, quantum-charged, turbo plugin
in small baby steps without having to hunt for where their logs might
be.

So check the things you need to check, print out error messages
(informative ones) using ``print``, and then return a 1 if the plugin
is configured correctly or a 0 if it's not configured correctly.

.. Note::

    This is not a substitute for the user to read the installation
    instructions.  It should be a really easy way to catch a lot of
    potential problems without involving the web server's error logs and
    debugging information being sent to a web-browser and things of that
    nature.

Here's an example of ``verify_installation`` from Will's wbgpager
plugin::

    def verify_installation(request):
        config = request.get_configuration()
        if config.get("num_entries", 0) == 0:
            print "missing config property 'num_entries'.  wbgpager won't do "
            print "anything without num_entries set.  either set num_entries "
            print "to a positive integer, or disable the wbgpager plugin."
            print "see the documentation at the top of the wbgpager plugin "
            print "code file for more details."
            return 0

        return 1



How to log messages to a log file
=================================

First you need to get the logger instance.  After that, you can call
debug, info, warning, error and critical on the logger instance.  For
example::

    from pyblosxom import tools

    def cb_prepare(args):
        # ...
        logger = tools.get_logger()
        logger.info("blah blah blah...")

        try:
            pass
            # ...
        except ValueError, e:
            logger.error(e)



How to store plugin state between callbacks
===========================================

The easiest way to store state between callbacks is to store the data
in the data dict of the Request object.  For example::

    STATE_KEY = "myplugin_state"

    def cb_date_head(args):
        request = args["request"]
        data = request.get_data()

        if ((data.has_key(STATE_KEY) 
             and data[STATE_KEY]["blah"] == "blahblah")):
            pass
            # ...


    def cb_filelist(args):
        request = args["request"]
        data = request.get_data()

        data[STATE_KEY] = {}
        data[STATE_KEY]["blah"] = "blahblah"


How to implement a callback
===========================

If you want to implement a callback, you add a function corresponding
to the callback name to your plugin module.  For example, if you
wanted to modify the Request object just before rendering, you'd
implement ``cb_prepare`` like this::

    def cb_prepare(args):
        pass


Obviously, since we have ``pass`` we're not actually doing anything
here, but when the user sends a request and PyBlosxom handles it, this
function in your plugin will get called when PyBlosxom runs the
prepare callback.

Each callback passes in arguments through a single dictionary.  Each
callback passes in different arguments and expects different return
values.  Check the doc:`dev_architecture <architecture>` chapter
for a list of all the callbacks that are available, their arguments,
and return values.


.. _writing-an-entryparser:

Writing an entryparser
======================

Entry parsing functions take in a filename and the Request object.
They then open the file and parse it out.  They can call
``cb_preformat`` and ``cb_postformat`` as they see fit.  They should
return a dict containing at least ``"title"`` and ``"body"`` keys.
The "title" should be a single string.  The ``"body"`` should be a
single string and should be formatted in HTML.

Here's an example code that reads ``.plain`` files which have the
title as the first line, metadata lines that start with ``#`` and then
after all the metadata the body of the entry::

    import os

    def cb_entryparser(entryparsingdict):
        """
        Register self as plain file handler
        """
        entryparsingdict["plain"] = parse
        return entryparsingdict

    def parse(filename, request):
        """
        We just read everything off the file here, using the filename
        as the title.
        """
        entrydata = {}

        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        entrydata["title"] = filename
        entrydata["body"] = "<pre>" + "".join(lines) + "</pre>"

        return entrydata


You can also specify the template to use by setting the
``"template_name"`` variable in the returned dict.  If the template
specified doesn't exist, PyBlosxom will use the ``story`` template for
the specified flavour.

For example, if you were creating a tumblelog and the file parsed was
a image entry and you want image entries to be displayed on your blog
with an image and then a caption below it and that's it, then you
would create a template for that and set ``"template_name"`` to the
name of the template::

    def cb_entryparser(entryparsingdict):
        """
        Register self as plain file handler
        """
        entryparsingdict['image'] = parse_image
        return entryparsingdict

    def parse_image(filename, request):
        """
        An image entry consists of an image file name followed by
        the caption.  Like this::

            cimg_8229.jpg
            This is a picture of me standing on my head.

        Note that there's no title, no metadata, ...
        """
        entrydata = {}

        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        # we do this for RSS purposes
        entrydata['title'] = "image %s" % lines[0]
        entrydata['body'] = "\n".join([
            "<img src=\"/images/%s\">",
            "<p>%s</p>" % "".join(lines[1:])
            ])

        entrydata["template_name"] = "image_post"

        return entrydata


.. _writing-a-preformatter:

Writing a preformatter plugin
=============================

FIXME - need more about preformatters here

A typical preformatter plugin looks like this::

    def cb_preformat(args):
        if args['parser'] == 'linebreaks':
            return parse(''.join(args['story']))

    def parse(text):
        # A preformatter to convert linebreak to its HTML counterpart
        text = re.sub('\\n\\n+','</p><p>',text)
        text = re.sub('\\n','<br />',text)
        return '<p>%s</p>' % text


.. _writing-a-postformatter:

Writing a postformatter plugin
==============================

FIXME - write this section


.. _writing-a-renderer:

Writing a renderer
==================

FIXME - write this section


.. _writing-a-command:

Writing a plugin that adds a commandline command
================================================

*New in PyBlosxom 1.5*

The ``pyblosxom-cmd`` command allows for plugin-defined commands.
This allows your plugin to do maintenance tasks (updating an index,
statistics, generating content, ...) and allows the user to schedule
command execution through cron or some similar system.

To write a new command, you must:

1. implement the ``commandline`` callback which adds the command,
   handler, and command summary
2. implement the command function

For example, this adds a command to print command line arguments::

    def printargs(command, argv):
        print argv
        return 0

    def cb_commandline(args):
        args["printargs"] = (printargs, "prints arguments")
        return args


.. Note::

   The plugin must be in a directory specified by ``load_plugins`` in
   the user's ``config.py`` file.

Executing the command looks like this::

    % pyblosxom-cmd printargs --config /path/to/config.py/dir a b c
    pyblosxom-cmd version 1.5
    a b c
