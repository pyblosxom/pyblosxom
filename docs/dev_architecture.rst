.. highlight:: python
   :linenothreshold: 5

======================
PyBlosxom Architecture
======================

Summary
=======

PyBlosxom uses the file system for data storage allowing you to use
the text-based tools that you use for other parts of your workflow for
your blog.

PyBlosxom has a plugin system allowing users to augment and extend
PyBlosxom's behavior to meet their specific needs.

This chapter covers PyBlosxom's architecture.

The code is fairly well documented and you should always consider the
code to be the authority when the code and this manual are in
disagreement.


Parts
=====

PyBlosxom is composed of several parts:

1. ``pyblosxom.cgi`` - This is the CGI script that is executed by your
   web-server, pulls in configuration variables from ``config.py`` and
   then instantiates PyBlosxom objects to handle the request.

2. ``PyBlosxomWSGIApp`` - This is the WSGI application for PyBlosxom.

3. ``Pyblosxom`` package - This is the Python package that holds the
   PyBlosxom objects and utility functions that handle the request.

   1. the ``entries`` package - Handles the abstraction allowing
      PyBlosxom to use entries other than those solely found on the
      file system.

   2. the ``renderers`` package - PyBlosxom can handle different
      renderers.  The renderer gets a list of entries to be rendered
      and can render them using whatever means it so desires: blosxom
      templates, htmltmpl templates, Cheetah templates, hard-coded RSS
      2.0 markup, ...

      PyBlosxom comes with two renderers: blosxom and debug.

   3. the ``cache`` package - PyBlosxom allows for entry-level
      caching.  This helps in cases where your entries are stored in a
      format that requires a lot of processing to convert to HTML.


PyBlosxom's behavior and output is then augmented by:

1. plugins - Plugins allow you to augment PyBlosxom's default
   behavior.  These you can get from the plugin registry or write
   yourself.

2. flavour templates - Flavour templates allow you to create the look
   and feel of your blog.  These you can get from the flavour registry
   or write yourself.



Lifecycle of a PyBlosxom request
================================

This is the life cycle of a single PyBlosxom CGI request. It involves
the following "entities":


* ``pyblosxom.cgi`` - A script found in the ``web/`` directory.  This
  is the CGI script that handles PyBlosxom requests.

* ``config.py`` - The configuration file that defines the behavior and
  properties of your blog.

* ``PyBlosxom.pyblosxom`` - The pyblosxom module holds the default
  PyBlosxom behavior functions. It also defines the Request class and
  the PyBlosxom class.

* ``Pyblosxom.pyblosxom.Request`` - The Request object holds the state
  of the PyBlosxom request at any given time throughout the lifecycle
  of the request.  The Request object is passed to most callbacks in
  the args dict as ``request``.

* ``Pyblosxom.pyblosxom.PyBlosxom`` - The PyBlosxom object holds a
  list of registered plugins, what callbacks they're registered to,
  and the methods that handle the the actual request.


The PyBlosxom request lifecycle starts with the web-server executing
``pyblosxom.cgi``.

1. ``pyblosxom.cgi`` loads ``config.py``

2. ``pyblosxom.cgi`` instantiates a Request object

3. ``pyblosxom.cgi`` instantiates a ``Pyblosxom.pyblosxom.PyBlosxom``
   object passing it the Request object

4. ``pyblosxom.cgi`` calls ``run()`` on the PyBlosxom object

   1. PyBlosxom instance, run method: calls ``initialize``

        1. PyBlosxom instance, ``initialize`` method: calls the entry
           parser callback to get a map of all the entry types
           PyBlosxom can handle

   2. PyBlosxom instance, ``run`` method: calls the start callback to
      allow plugins to do any initialization they need to do

   3. PyBlosxom instance, ``run`` method: calls the handle callback
      allowing plugins to handle the request

      If a plugin handles the request, the plugin should return a
      ``1`` signifying it has handled the request and PyBlosxom should
      stop.  FINISHED.

      If no plugin handles the request, then we continue using the
      ``blosxom_handler``.

   4. PyBlosxom instance, ``run`` method: calls the end callback to
      allow plugins to do any cleanup they need to do.

FIXME - add lifecycle for long-running processes through WSGI---it's
slightly different.


Lifecycle of the blosxom_handler
================================

This describes what the ``blosxom_handler`` does.  This is the default
handler for PyBlosxom.  It's called by the PyBlosxom instance in the
run method if none of the plugins have handled the request already.

1. Calls the ``renderer`` callback to get a renderer instance.

   If none of the plugins return a ``Renderer`` instance, then
   PyBlosxom checks to see if the ``renderer`` property is set in
   ``config.py``.

   If there ``renderer`` is specified, PyBlosxom instantiates that.

   If there ``renderer`` is not specified, PyBlosxom uses the
   ``blosxom`` renderer in the ``renderer`` package.

2. Calls the ``pathinfo`` callback which allows all plugins to help
   figure out what to do with the HTTP URI/QUERYSTRING that's been
   requested.

3. Calls the ``filelist`` callback which returns a list of entries to
   render based on what the pathinfo is.

4. Calls the ``prepare`` callback which allows plugins to transform
   the entries and any other data in the ``Request`` object prior to
   rendering.

5. Renders the entries.



Lifecycle of the blosxom renderer
=================================

The blosxom renderer renders the entries in a similar fashion to what
Blosxom does.  The blosxom renderer uses flavour templates and
template variables.  It also has a series of callbacks allowing
plugins to modify templates and entry data at the time of rendering
that specific piece.

1. Renders the ``content_type`` template.

2. Calls the ``head`` callback and then renders the ``head`` template.

3. Calls the ``date_head`` callback and renders the ``date_head``
   template.

4. For each entry:

   1. If the date of this entry's mtime is different than the last
      entry, call the ``date_foot`` callback and render the
      ``date_foot`` template.  Then call the ``date_head`` callback
      and render the ``date_head`` template.

   2. Call the ``story`` callback and render the ``story`` template.

5. Call the ``date_foot`` callback and render the ``date_foot``
   template.

6. Call the ``foot`` callback and render the ``foot`` template.



About callbacks
===============

Callbacks allow plugins to override behavior in PyBlosxom or provide
additional behavior.  The callback mechanism actually encompasses a
series of different functions.  Callbacks can act as handlers, as
notifiers, and also as modifiers.


Types of callbacks
------------------

In the case of handler callbacks, PyBlosxom will query each plugin
implementing the callback until one of the plugins returns that it has
handled the callback.  At that point, execution of handling code
stops.  If none of the plugins handle the callback, then PyBlosxom
will run its default behavior code.

In the case of notifier callbacks, PyBlosxom will notify each plugin
implementing the callback regardless of return values.

In the case of modifier callbacks, PyBlosxom will query each plugin
implementing the callback passing in some input.  It takes the output
from the callback function and passes that in as input to the next
callback function.  In this way, each plugin has a chance to modify
and transform the data.

There's no reason you can't implement a handler-type callback and use
it for notification purposes---that's fine.  You should know that in
the case of handler callbacks and modifier callbacks, the return value
that your plugin gives will affect PyBlosxom's execution.


Callbacks that have blosxom equivalents
---------------------------------------

There are a series of callbacks in PyBlosxom that have equivalents in
blosxom 2.0.  The names are sometimes different and in most cases the
arguments the PyBlosxom versions take are different than the blosxom
2.0 versions.  Even so, the PyBlosxom versions serve the same purpose
as the blosxom 2.0 versions.

This isn't very interesting unless you're trying to implement the
functionality of a blosxom 2.0 plugin in Python for PyBlosxom.

The available blosxom renderer callbacks are:

* cb_head - corresponds to blosxom 2.0 head
* cb_date_head - corresponds to blosxom 2.0 date
* cb_story - corresponds to blosxom 2.0 story
* cb_foot - corresponds to blosoxm 2.0 foot


Additionally, we have these lifecycle callbacks available:

* the blosxom 2.0 entries callback is handled by cb_filelist
* the blosxom 2.0 filter callback is handled by cb_prepare
* the blosxom 2.0 sort callback can sort of be handled by cb_prepare 
  depending on what you're trying to do


Callbacks
=========

cb_prepare
----------

The prepare callback is called in the default blosxom handler after
we've figured out what we're rendering and before we actually go to
the renderer.

Plugins should implement ``cb_prepare`` to modify the data dict which
is in the Request.  Inside the data dict is ``entry_list`` (amongst
other things) which holds the list of entries to be renderered (in the
order they will be rendered).

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

Functions that implement this callback can return whatever they
want---it doesn't affect the callback chain.

Example of a ``cb_prepare`` function in a plugin::

   def cb_prepare(args):
       """
       This plugin shows the number of entries we are going to render and
       place the result in $entrycount
       """
       request = args['request']
       data = request.get_data()
       config = request.get_configuration()

       # Can anyone say Ternary? :)
       IF = lambda a, b, c: (a() and [b()] or [c()])[0]

       num_entry = config['num_entries']
       entries = len(data['entry_list'])

       data['entrycount'] = IF(num_entry > entries, num_entry, entries)


cb_logrequest
-------------

The logrequest callback is used to notify plugins of the current
PyBlosxom request for the purposes of logging.

Functions that implement this callback will get an args dict
containing:

``filename``
   a filename; typically a base filename

``return_code``
   an HTTP error code (e.g. 200, 404, 304, ...)

``request``
   a Request object


Functions that implement this callback can return whatever they
want---it doesn't affect the callback chain.

``cb_logrequest`` is called after rendering and will contain all the
modifications to the Request object made by the plugins.

An example input args dict is like this::

   {'filename': filename, 'return_code': '200', 'request': Request()}


cb_filelist
-----------

The filelist callback allows plugins to generate the list of entries
to be rendered.  Entries should be EntryBase derivatives---either by
instantiating EntryBase, FileEntry, or creating your own EntryBase
subclass.

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

Functions that implement this callback should return ``None`` if they
don't plan on generating the entry list or a list of entries if they do. 
When a function returns ``None``, the callback will continue to
the next function to see if it will return a list of entries.  When a
function returns a list of entries, the callback will stop.


cb_sortlist
-----------

The sortlist callback allows plugins to implement their own sorting
of entries.  This callback gets called by filelist handlers.

Functions that implement this callback will get an args dict
containing:

``request``
   A Request object

``entry_list``
   The list of entries to be sorted.

Return ``None`` if the function doesn't sort the list.  Return
the sorted list if the function does sort the list.

Example of a ``cb_sortlist`` function::

   def cb_sortlist(args):
       """Sorts the list from oldest (beginning) to newest (end)
       for a site that's less like a blog and more like a 
       journal.
       """
       entrylist = args["entry_list"]

       entrylist = [(e._mtime, e) for e in entrylist]
       entrylist.sort()
       entrylist = [e[1] for e in entrylist]

       return entrylist


cb_truncatelist
---------------

The truncatelist callback allows plugins to implement their own
truncation rules.  This callback gets called by filelist handlers.

Functions that implement this callback will get an args dict
containing:

``request``
   A Request object

``entry_list``
   The list of entries to be truncated.

Return ``None`` if the function doesn't truncate the list.  Return
the new list if the function does truncate the list.

Example of a ``cb_truncatelist`` function::

   def cb_truncatelist(args):
       request = args["request"]
       entrylist = args["entry_list"]

       data = request.data
       config = request.config

       num_entries = config.get("num_entries", 5)
       truncate = data.get("truncate", 0)
       if num_entries and truncate:
           entrylist = entrylist[:num_entries]
           return entrylist

       return None


cb_filestat
-----------

The filestat callback allows plugins to provide mtimes for entries.
Plugins may use this to override the mtime stored in the filesystem.
For example, one of the contributed plugins uses this to set the mtime
to the time specified in the entry's filename.

Plugins may also use this to provide a cheaper alternative to
filesystem stat calls---a notorious performance drag.  The
hardcodedates plugin, for example, stores mtimes in a file: it reads
the file once at startup then returns mtimes from its in-memory
database.

Functions that implement this callback will get an args dict
containing:

``filename``
   the filename of the entry

``mtime``
   the result of an ``os.stat`` on the filename of the entry

Functions that implement this callback must return the input args dict
whether or not they adjust anything in it.  The callback chain will
stop as soon as a callback modifies mtime.  If no plugin handles the
callback, PyBlosxom will fall back to calling ``os.stat()``.


cb_pathinfo
-----------

The pathinfo callback allows plugins to parse the HTTP ``PATH_INFO``
item.  This item is stored in the http dict of the Request object.
Functions would parse this as they desire, then set the following
variables in the data dict of the Request object:

``bl_type``
   ``dir`` or ``file``

``pi_bl``
   typically the same as ``PATHINFO``

``pi_yr``
   the year in yyyy format

``pi_mo``
   the month in mm or mmm format (e.g. 02, Jan, Feb, ...)

``pi_da``
   the day of the month in dd format

``root_datadir``
   full path to the entry folder or entry file on the file system

``flavour``
   the flavour gathered from this URL

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

Functions that implement this callback should make the modifications
to the data dict in place---no need to return anything.


cb_commandline
--------------

The commandline callback allows plugins to implement additional
``pyblosxom-cmd`` commands.  This allows a plugin to expose
maintenance and setup functionality to the user at the command line or
through cron.

For example. if you wrote a plugin that built an map of tags to
entries that used that tag, you'd probably want to write a command
that updates the index which the user could create a cron job for.

The ``cb_commandline`` function takes a single ``args`` argument
which is a map of command -> tuple of handler and help text.  It
then returns the args dict.

For example::

    def cb_commandline(args):
        args["printargs"] = (printargs, "prints command line arguments")

See :ref:`writing-a-command` for more details.


cb_renderer
-----------

The renderer callback allows plugins to specify a renderer to use by
returning a renderer instance to use.  If no renderer is specified, we
use the default blosxom renderer.

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

Functions that implement this callback should return ``None`` if they
don't want to specify a renderer or the renderer object instanct if
they do.  When a function returns a renderer instance, processing
stops.


cb_entryparser
--------------

The entryparser callback allows plugins to register the entryparsers
they have.  Entry parsers are linked with a filename extension.  For
example, the default blosxom text entry parser will be used for any
file ending in ``.txt``.

Functions that implement this callback will get the entryparser dict
consisting of file extension -> entry parsing function pairs.

Functions that implement this callback should return the entryparser
dict after modifying it.

Example::

    def cb_entryparser(entryparsingdict):
        entryparsingdict["txtl"] = txtl_parse
        return entryparsingdict

Then the plugin would define ``txtl_parse`` which takes a filename
and a Request and returns an entrydata dict with ``title`` and
``body`` (or whatever the templates need to render this entry).

See :ref:`writing-an-entryparser`.


cb_preformat
------------

The preformat callback acts in conjunction with the entryparser that
handled the entry to do a two-pass formatting of the entry.

Functions that implement ``cb_preformat`` are text transformation
tools.  Once one of them returns a transformed entry, then we stop
processing.

Functions that implement this callback will get an args dict
containing:

``parser``
  a string that indicates whether a preformatter should run

``story``
  the list of lines of the blog post with ``\n`` included

``request``
  a Request object

Functions that implement this callback should return None if they
didn't modify the story or a single story string.

See :ref:`writing-a-preformatter`.


cb_postformat
-------------

The postformat callback allows plugins to make further modifications
to entry text.  It typically gets called after a preformatter by the
entryparser.  It can also be used to add additional properties to
entries.  The changes from postformat functions are saved in the cache
(if the user has caching enabled).  As such, this shouldn't be used
for dynamic data like comment counts.

Examples of usage:

* adding a word count property to the entry
* using a macro replacement plugin (Radio Userland glossary)
* acronym expansion
* a 'more' text processor
* ...

Functions that implement this callback will get an args dict containing:

``entry_data``
   a dict that minimally contains ``title`` and ``story``

``request``
   a Request object

Functions that implement this callback don't need to return
anything---modifications to the ``entry_data`` dict are done in place.

See :ref:`writing-a-postformatter`.


cb_start
--------

The start callback allows plugins to execute startup/initialization
code.  Use this callback for any setup code that your plugin needs,
like:

* reading saved data from a file
* checking to make sure configuration variables are set
* allocating resources

.. Note::

   ``cb_start`` is different in PyBlosxom than in blosxom.

   The ``cb_start`` callback is slightly different than in blosxom in
   that ``cb_start`` is called for every PyBlosxom request regardless
   of whether it's handled by the default blosxom handler.  In
   general, it's better to delay allocating resources until you
   absolutely know you are going to use them.


Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

Functions that implement this callback don't need to return anything.


cb_end
------

The start callback allows plugins to execute teardown/cleanup code,
save any data that hasn't been saved, clean up temporary files, and
otherwise return the system to a normal state.

Examples of usage:

* save data to a file
* clean up any temporary files
* ...

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

Functions that implement this callback don't need to return anything.

.. Note::

   ``cb_end`` is different in PyBlosxom than in blosxom

   The ``cb_end`` callback is called for every PyBlosxom request
   regardless of whether it's handled by the default blosxom handler
   or not.  This is slightly different than blosxom.


cb_staticrender_filelist
------------------------

Gives plugins a chance to modify the list of (url, query) tuples that
are about to be rendered statically.  Plugins can add additional
tuples, remove tuples, modify tuples, ...

Functions that implement this callback will get an args dict
containing:

``request``
    a request object

``filelist``
    list of (url, query) tuples of all urls to be rendered

``flavours``
    list of flavours to be rendered

Functions that implement this callback can modify the filelist
in-place and don't have to return anything.

Example in which the plugin adds the search page url so that the
search page gets rendered::

   def cb_staticrender_filelist(args):
       filelist = args["filelist"]
       filelist.append(("/search", ""))


cb_head
-------

The head callback is called before a head flavour template is
rendered.

``cb_head`` is called before the variables in the entry are
substituted into the template.  This is the place to modify the head
template based on the entry content.  You can also set variables on
the entry that will be used by the ``cb_story`` or ``cb_foot``
templates.  You have access to all the content variables via entry.

Blosxom 2.0 calls this callback ``head``.

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

``renderer``
   the ``BlosxomRenderer`` instance that called the callback

``entry``
   the entry to be rendered

``template``
   a string containing the flavour template to be processed

Functions that implement this callback must return the input args dict
whether or not they adjust anything in it.

Example in which we add the number of entries being rendered to the
``$blog_title`` variable::

   def cb_head(args):
       request = args["request"]
       config = request.get_configuration()
       data = request.get_data()

       num_entries = len(data.get("entry_list", []))
       bt = config.get("blog_title", "")
       config["blog_title"] = bt + ": %d entries" % num_entries

       return args



cb_date_head
------------

The ``date_head`` callback is called before a ``date_head`` flavour
template is rendered.

``cb_date_head`` is called before the variables in the entry are
substituted into the template.  This is the place to modify the
``date_head`` template based on the entry content.  You have access to
all the content variables via entry.

Blosxom 2.0 calls this callback ``date``.

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

``renderer``
   the ``BlosxomRenderer`` instance that called the callback

``entry``
   the entry to be rendered

``template``
   a string containing the flavour template to be processed

Functions that implement this callback must return the input args dict
whether or not they adjust anything in it.



cb_story
--------

The ``story`` callback gets called before the entry is rendered.

The template used is typically the ``story`` template, but we allow
entries to override this if they have a ``template`` property.  If
they have the ``template`` property, then we'll use the template of
that name instead.

``cb_story`` is called before the variables in the entry are
substituted into the template.  This is the place to modify the
``story`` template based on the entry content.  You have access to all
the content variables via entry.

Blosxom 2.0 calls this callback ``story``.

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

``renderer``
   the ``BlosxomRenderer`` that called the callback

``entry``
   the entry to be rendered

``template``
   a string containing the flavour template to be processed

Functions that implement this callback must return the input args dict
whether or not they adjust anything in it.



cb_story_end
------------

The ``story_end`` callback is is called after the variables in the
entry are substituted into the template.  You have access to all the
content variables via entry.

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

``renderer``
   the ``BlosxomRenderer`` instance that called the callback

``entry``
   the entry object to be rendered

``template``
   a string containing the flavour template to be processed

Functions that implement this callback must return the input args dict
whether or not they adjust anything in it.


cb_foot
-------

The ``foot`` callback is called before the variables in the entry are
substituted into the foot template.  This is the place to modify the
``foot`` template based on the entry content.  You have access to all
the content variables via entry.

Blosxom 2.0 calls this callback ``foot``.

Functions that implement this callback will get an args dict
containing:

``request``
   a Request object

``renderer``
   the ``BlosxomRenderer`` instance that called the callback

``entry``
   the entry to be rendered

``template``
   a string containing the flavour template to be processed

Functions that implement this callback must return the input args dict
whether or not they adjust anything in it.
