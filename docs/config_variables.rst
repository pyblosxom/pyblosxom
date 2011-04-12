=====================
Configuring PyBlosxom
=====================

You configure a PyBlosxom blog by setting configuration variables in a
simple Python file, ``config.py``. Each PyBlosxom blog has its own
``config.py`` file. This chapter documents the default ``config.py``
variables. Some of these are required, others are optional.

Each configuration variable is set with a line like::

    py["blog_title"] = "Another pyblosxom blog"

where *blog_title* is the name of the configuration variable and
*"Another pyblosxom blog"* is its value. Most configuration values are
strings (and must be enclosed in quotes), but some are lists, numbers or
other types of values.

If you install any PyBlosxom plugins those plugins may ask you to set
additional variables in your ``config.py`` file. Those variables will be
documented in the documentation that comes with the plugin or at the top
of the plugin's source code file. Additional plugin variables will not
be documented here.

You can add your own personal configuration variables to ``config.py``.
You can put any ``py["name"] = value`` statements that you want in
``config.py``. You can then refer to your configuration variables
further down in your ``config.py`` file and in your flavour templates.
This is useful for allowing you to centralize any configuration for your
blog into your ``config.py`` file.

For example, you could move all your media files (JPEG images, GIF
images, CSS, ...) into a directory on your server to be served by Apache
and then set the config.py variable ``py["media_url"]`` to the directory
with media files and use ``$media_url`` to refer to this URL in your
flavour templates.

If there are any variables listed below that aren't in your
``config.py`` file, you can simply add them to the file yourself using
the ``py["key"] = value`` format.


Codebase configuration
======================

codebase
--------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: no default

If you have installed PyBlosxom on your web server using your
distribution's package manager or Python setuptools then you don't need
to set the codebase variable.

If you cannot install PyBlosxom on your web server then you can save the
PyBlosxom source code to a location on your server and use the codebase
setting instead. The codebase setting tells the Python interpreter where
to find the PyBlosxom codebase. This should be the full path to where
the PyBlosxom directory is on your system. It should be the path to the
directory that holds the "Pyblosxom" directory (note the case--uppercase
P lowercase b!).

For example, if you untarred PyBlosxom into
``/home/joe/pyblosxom-1.5/``, then the Pyblosxom (uppercase P and
lowercase b) directory should be in ``/home/joe/pyblosxom-1.5/`` and
you would set your codebase variable like this::

   py["codebase"] = "/home/joe/pyblosxom-1.5/"


Blog configuration
==================

blog_title
----------

**REQUIRED**: yes

**DATATYPE**: string

**DEFAULT VALUE**: "" (no default value--you must set this)

This is the title of your blog.  Typically this should be short and is
accompanied by a longer summary of your blog which is set in
``blog_description``.

For example, if Joe were writing a blog about cooking, he might title
his blog::

   py["blog_title"] = "Joe's blog about cooking"


blog_description
----------------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: ""

This is the description or byline of your blog.  Typically this is a
phrase or a sentence that summarizes what your blog covers.

If you were writing a blog about restaurants in the Boston area, you
might have a ``blog_description`` of::

   py["blog_description"] = "Critiques of restaurants in the Boston area"


Or if your blog covered development on PyBlosxom, your
``blog_description`` might go like this::

   py["blog_description"] = "Ruminations on the development of " + \
                            "PyBlosxom and related things"


.. Note::

   Remember that the ``config.py`` file is a Python code file just
   like any other Python code file.  Splitting long lines into shorter
   lines can be done with string concatenation and the ``\`` character
   which indicates that the next line is a continuation of the current
   one.

   Alternatively, you could wrap a multi-line string in triple quotes:
   ``""" ... """`` or ``''' ... '''``.


blog_author
-----------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: ""

This is the name of the author that you want to appear on your blog.
Very often this is your name or your pseudonym.

If Joe Smith had a blog, he might set his blog_author to "Joe Smith"::

   py["blog_author"] = "Joe Smith"


If Joe Smith had a blog, but went by the pseudonym "Magic Rocks", he
might set his blog_author to "Magic Rocks"::

   py["blog_author"] = "Magic Rocks"


blog_email
----------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: ""

This is the email address you want associated with your blog.

For example, say Joe Smith had an email address ``joe@joesmith.net``
and wanted that associated with his blog.  Then he would set the email
address as such::

   py["blog_email"] = "joe@joesmith.net"


blog_rights
-----------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: ""

These are the rights you give to others in regards to the content on
your blog. Generally this is the copyright information, for example::

    py["blog_rights"] = "Copyright 2005 Joe Bobb"

This is used in the Atom and RSS 2.0 feeds. Leaving this blank or not
filling it in correctly could result in a feed that doesn't validate.


blog_language
-------------

**REQUIRED**: yes

**DATATYPE**: string

**DEFAULT VALUE**: no default value--you must set this

This is the primary language code for your blog.

For example, English users should use ``en``::

   py["blog_language"] = "en"

This gets used in the RSS flavours.

Refer to `ISO 639-2`_ for language codes.  Many systems use two-letter
ISO 639-1 codes supplemented by three-letter ISO 639-2 codes when no
two-letter code is applicable.  Often ISO 639-2 is sufficient.  If you use
very special languages, you may want to refer to `ISO 639-3`_, which is a
super set of ISO 639-2 and contains languages used thousands of years ago.

.. _ISO 639-2: http://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
.. _ISO 639-3: http://www.sil.org/iso639-3/


blog_encoding
-------------

**REQUIRED**: YES

**DATATYPE**: string

**DEFAULT VALUE**: no default value--you must set this

This is the character encoding of your blog.

For example, if your blog was encoded in utf-8, then you would set the
``blog_encoding`` to::

   py["blog_encoding"] = "utf-8"


.. Note::

   This value must be a valid character encoding value.  In general,
   if you don't know what to set your encoding to then set it to
   ``utf-8``.

This value should be in the meta section of any HTML- or XHTML-based flavours
and it's also in the header for any feed-based flavours.  An improper
encoding will gummy up some/most feed readers and web-browsers.

W3C has a nice `tutorial on encoding`_.  You may refer to
`IANA charset registry`_ for a complete list of encoding names.


.. _tutorial on encoding: http://www.w3.org/International/tutorials/tutorial-char-enc/
.. _IANA charset registry: http://www.iana.org/assignments/character-sets


locale
------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: "C"

PyBlosxom uses the locale config variable to adjust the values for
month names and dates.

In general, you don't need to set this unless you know you're not
using en_US or en_UK.

A listing of language codes is at
http://ftp.ics.uci.edu/pub/ietf/http/related/iso639.txt

A listing of country codes is at:
http://userpage.chemie.fu-berlin.de/diverse/doc/ISO_3166.html

For example, if you wanted to set the locale to the Dutch language in
the Netherlands you'd set locale to::

   py["locale"] = "nl_NL.UTF-8"


datadir
-------

**REQUIRED**: yes

**DATATYPE**: string

**DEFAULT VALUE**: no default value--you need to set this

This is the full path to where your blog entries are kept on the file
system.

For example, if you are storing your blog entries in
``/home/joe/blog/entries/``, then you would set the ``datadir`` like
this::

   py["datadir"] = "/home/joe/blog/entries/"


.. Note::

   A note about ``datadir`` on Windows:

   Use ``/`` to separate directories in the ``datadir`` path even if
   you are using Windows.  Examples of valid datadirs on Windows::

      py["datadir"] = "/blog/entries/"

   and::

      py["datadir"] = "e:/blog/entries/"


depth
-----

**REQUIRED**: no

**DATATYPE**: integer

**DEFAULT VALUE**: defaults to 0--infinite depth

The depth setting determines how many levels deep in the directory
(category) tree that PyBlosxom will display when doing indexes.

* 0 - infinite depth (aka grab everything) DEFAULT
* 1 - datadir only
* 2 - two levels
* 3 - three levels
* ...
* *n* - *n* levels deep


ignore_directories
------------------

**REQUIRED**: no

**DATATYPE**: list of strings

**DEFAULT VALUE**: [ ]

The ``ignore_directories`` variable allows you to specify which
directories in your datadir should be ignored by PyBlosxom.

This defaults to an empty list (i.e. PyBlosxom will not ignore any
directories).

For example, if you use CVS to manage the entries in your datadir, then
you would want to ignore all CVS-related directories like this::

   py["ignore_directories"] = [ "CVS" ]


If you were using CVS and you also wanted to store drafts of entries
you need to think about some more in a drafts directory in your
datadir, then you could set your ``ignore_directories`` like this::

   py["ignore_directories"] = [ "drafts", "CVS" ]


This would ignore all directories named "CVS" and "drafts" in your
datadir tree.


flavourdir
----------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: no default value set

This is the full path to where your PyBlosxom flavours are kept.

If you do not set the ``flavourdir``, then PyBlosxom will look for
your flavours and templates in the datadir alongside your entries.

.. Note::

   "flavour" is spelled using the British spelling and not the American
   one.

For example, if you want to put your entries in
``/home/joe/blog/entries/`` and your flavour templates in
``/home/joe/blog/flavours/`` you would set ``flavourdir`` and
``datadir`` like this::

   py["datadir"] = "/home/joe/blog/entries/"
   py["flavourdir"] = "/home/joe/blog/flavours/"


.. Note::

   Use ``/`` to separate directories in the ``flavourdir`` path even
   if you are using Windows.  Examples of valid ``flavourdir`` on
   Windows::

      py["flavourdir"] = "/blog/flavours/"

   and::

      py["flavourdir"] = "e:/blog/flavours/"


default_flavour
---------------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: "html"

This specified the flavour that will be used if the user doesn't
specify a flavour in the URI.

For example, if you wanted your default flavour to be "joy", then you
would set ``default_flavour`` like this::

   py["default_flavour"] = "joy"


Doing this will cause PyBlosxom to use the "joy" flavour whenever URIs
are requested that don't specify the flavour.

For example, the following will all use the "joy" flavour::

   http://joesmith.net/blog/
   http://joesmith.net/blog/index
   http://joesmith.net/blog/movies/
   http://joesmith.net/blog/movies/supermanreturns


num_entries
-----------

**REQUIRED**: no

**DATATYPE**: int

**DEFAULT VALUE**: 5

The ``num_entries`` variable specifies the number of entries that show
up on your home page and other category index pages.  It doesn't
affect the number of entries that show up on date-based archive pages.

It defaults to 5 which means "show at most 5 entries".

If you set it to 0, then it will show all entries that it can.

For example, if you wanted to set ``num_entries`` to 10 so that 10
entries show on your category index pages, you sould set it like
this::

   py["num_entries"] = 10


truncate_frontpage
------------------

**REQUIRED**: no

**DATATYPE**: boolean

**DEFAULT VALUE**: True

Whether or not to truncate the number of entries displayed on the
front page to ``num_entries`` number of entries.

For example, this causes all entries to be displayed on your
front page (which is probably a terrible idea)::

    py["truncate_frontpage"] = False


truncate_category
-----------------

**REQUIRED**: no

**DATATYPE**: boolean

**DEFAULT VALUE**: True

Whether or not to truncate the number of entries displayed on a
category-based index page to ``num_entries`` number of entries.

For example, this causes all entries in a category to show up in all
category-based index pages::

    py["truncate_category"] = False


truncate_date
-------------

**REQUIRED**: no

**DATATYPE**: boolean

**DEFAULT VALUE**: False

Whether or not to truncate the number of entries displayed on a
date-based index page to ``num_entries`` number of entries.


base_url
--------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: calculated based on HTTP server variables

This is the base url for your blog.  If someone were to type this url
into their browser, then they would see the main index page for your
blog.

For example, if Joe Smith put his ``pyblosxom.cgi`` script into a
cgi-bin directory and he was using Apache, his base_url might look
like this::

   py["base_url"] = "http://joesmith.net/~joe/cgi-bin/pyblosxom.cgi"

However, it's common that this can be determined by PyBlosxom by
looking at the HTTP environment variables--so if you're not doing any
url re-writing, it's possible that PyBlosxom can correctly determine
the url and you won't have to set the base_url variable at all.

If Joe got tired of that long url, Joe might set up some url
re-writing on my web-server so that the base_url looked like this::

   py["base_url"] = "http://joesmith.net/~joe/blog"


.. Note::

   Your base_url property should *not* have a trailing slash.

.. Note::

   If you use mod_rewrite rules or some other url rewriting system on
   your web-server, then you'll want to set this property.


parser
------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: "plain"

The default entry parser that PyBlosxom will use to parse this blog's
entry files. See :ref:`Entry parsers`.


Logging configuration
=====================

log_file
--------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: no default value set

This specifies the file that PyBlosxom will log messages to.

If this is set to "NONE", then log messages will be silently ignored.

If PyBlosxom cannot open the file for writing, then log messages will
be sent to sys.stderr.

For example, if you wanted PyBlosxom to log messages to
``/home/joe/blog/logs/pyblosxom.log``, then you would set ``log_file``
to::

   py["log_file"] = "/home/joe/blog/logs/pyblosxom.log"

If you were on Windows, then you might set it to::

   py["log_file"] = "c:/blog/logs/pyblosxom.log"

.. Note::

   The webserver that is executing PyBlosxom must be able to write to
   the directory containing your ``pyblosxom.log`` file.


log_level
---------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: no default value set

**POSSIBLE VALUES**:

* ``critical``
* ``error``
* ``warning``
* ``info``
* ``debug``

This sets the log level for logging messages.

If you set the ``log_level`` to ``critical``, then *only* critical
messages are logged.

If you set the ``log_level`` to ``error``, then error and critical
messages are logged.

If you set the ``log_level`` to ``warning``, then warning, error, and
critical messages are logged.

So on and so forth.

For "production" blogs (i.e. you're not tinkering with configuration,
new plugins, new flavours, or anything along those lines), then this
should be set to ``warning`` or ``error``.

For example, if you're done tinkering with your blog, you might set
the ``log_level`` to ``info`` allowing you to see how requests are
being processed::

   py['log_level'] = "info"


log_filter
----------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: no default value specified

This let's you specify which channels should be logged.

If ``log_filter`` is set, then ONLY messages from the specified channels
are logged.  Everything else is silently ignored.

Each plugin can log messages on its own channel.  Therefore channel
name == plugin name.

PyBlosxom logs its messages to a channel named "root".

.. Warning::

   A warning about omitting root:

   If you use ``log_filter`` and don't include "root", then PyBlosxom
   messages will be silently ignored!

For example, if you wanted to filter log messages to "root" and
messages from the "comments" plugin, then you would set ``log_filter``
like this::

   py["log_filter"] = ["root", "comments"]


Plugin Configuration
====================

plugin_dirs
-----------

**REQUIRED**: no

**DATATYPE**: list of strings

**DEFAULT VALUE**: [] (an empty list, do not load any plugins)

The ``plugin_dirs`` variable tells PyBlosxom which directories to look
in for plugin files to load. You can list as many plugin directories as
you want.

For example, if you stored your PyBlosxom plugins in
``/home/joe/blog/plugins/``, then you would set ``plugin_dirs`` like
this::

   py["plugin_dirs"] = ["/home/joe/blog/plugins/"]

.. Note::

   Plugin directories are not searched recursively for plugins.  If you
   have a tree of plugin directories that have plugins in them, you'll
   need to specify each directory in the tree.


load_plugins
------------

**REQUIRED**: no

**DATATYPE**: list of strings

**DEFAULT VALUE**: no default value set

If there is no ``load_plugins`` setting in ``config.py`` PyBlosxom loads
all plugins it finds in the directories specified by ``plugins_dir`` in
alphanumeric order by filename. Specifying ``load_plugins`` causes
PyBlosxom to load only the plugins you name and in in the order you name
them.

The value of ``load_plugins`` should be a list of strings where each
string is the name of a plugin module (i.e. the filename without the .py
at the end).

If you specify an empty list no plugins will be loaded.

For example, if you had::

   py["plugin_dirs"] = ["/home/joe/blog/plugins/"]
   # py["load_plugins"] = []

in your ``config.py`` file and there were three plugins in 
``/home/joe/blog/plugins/``::

   /home/
   +- joe/
      +- blog/
         +- plugins/
            +- plugin_a.py
            +- plugin_b.py
            +- plugin_c.py

then PyBlosxom would load all three plugins in alphabetical order by 
filename: ``plugin_a``, then ``plugin_b``, then ``plugin_c``.

If you wanted PyBlosxom to only load ``plugin_a`` and ``plugin_c``, then you
would set ``load_plugins`` to::

   py["load_plugins"] = ["plugin_a", "plugin_c"]

.. Note::

   In general, it's better to explicitly set ``load_plugins`` to the
   plugins you want to use.  This reduces the confusion about which
   plugins did what when you have problems.  It also reduces the
   potential for accidentally loading plugins you didn't intend to
   load.

.. Note::

   PyBlosxom loads plugins in the order specified by ``load_plugins``.
   This order also affects the order that callbacks are registered and
   later executed.  For example, if ``plugin_a`` and ``plugin_b`` both
   implement the ``handle`` callback and you load ``plugin_b`` first, then
   ``plugin_b`` will execute before ``plugin_a`` when the ``handle`` callback
   kicks off.

   Usually this isn't a big deal, however it's possible that some
   plugins will want to have a chance to do things before other
   plugins.  This should be specified in the documentation that comes
   with those plugins.


Caching Configuration
=====================

Enabling caching by setting the ``cacheDriver`` and ``cacheConfig``
variables in ``config.py`` speeds up rendering of your PyBlosxom pages.

cacheDriver
-----------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: ""

PyBlosxom has multiple cache mechanisms. Look at the source files in
``Pyblosxom/cache`` to see what mechanisms are available, then set
``cacheDriver`` to the cache mechanism that you want. For example::

    py["cacheDriver"] = "entrypickle"


cacheConfig
-----------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: ""

Read the top of the source code file in ``Pyblosxom/cache`` for your
selected cache driver (e.g. ``entrypickle.py``) to see how to set the
``cacheConfig`` variable for it. For example:

    py["cacheConfig"] = "/path/to/a/cache/directory"

.. Note::

   ``load_plugins`` should contain a list of strings where each string
   is a Python module--not a filename.  So don't add the ``.py`` to
   the end of the module name!


Static Rendering Configuration
==============================

If you are using static rendering to deploy your PyBlosxom blog you need
to set some additional configuration variables in your ``config.py``
file, see :ref:`static-rendering`.
