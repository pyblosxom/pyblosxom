======================
Variables in config.py
======================

Summary
=======

This is a list of configuration variables in ``config.py``.  This list
is not comprehensive!

If you install any plugins, those plugins may ask you to set
additional variables in your ``config.py`` file--those variables will
not be documented in this file.

Additionally, any variables you set in ``config.py`` will be available
in your templates.  This is useful for allowing you to centralize any
configuration for your blog into your ``config.py`` file and use it in
templates and other places.  For example, you could move all your
media files (JPEG images, GIF images, CSS, ...) into a directory on
your server to be served by Apache and then set the variable
``$media_url`` to the directory with media files and use that in your
templates.

If there are variables that are listed here that aren't in your
``config.py`` file, you can add them yourself.  The format is::

    py["key"] = value

where *key* is the configuration property name and *value* is the
value.  If the *value* is a string, it must be enclosed in quotes.


Configuration variables
=======================

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
like this:

   py["base_url"] = "http://joesmith.net/~joe/cgi-bin/pyblosxom.cgi"

However, it's common that this can be determined by PyBlosxom by
looking at the HTTP environment variables--so if you're not doing any
url re-writing, it's possible that PyBlosxom can correctly determine
the url and you won't have to set the base_url variable at all.

If Joe got tired of that long url, Joe might set up some url
re-writing on my web-server so that the base_url looked like this:

   py["base_url"] = "http://joesmith.net/~joe/blog"


.. Note::

   Your base_url property should NOT have a trailing slash.

.. Note::

   If you use mod_rewrite rules or some other url rewriting system on
   your web-server, then you'll want to set this property.


codebase
--------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: no default set

This is the full path to where the PyBlosxom directory is on your
system.

If you have installed PyBlosxom as a Python library by running
``python setup.py install`` then you don't need to set the codebase
variable.

If you have NOT installed PyBlosxom as a Python library, then you DO
need to set the codebase variable.  Otherwise the Python interpreter
won't be able to find the PyBlosxom codebase and your blog will not
work.

For example, if you untarred PyBlosxom into
``/home/joe/pyblosxom-1.5/``, then the Pyblosxom (uppercase P and
lowercase b) directory should be in ``/home/joe/pyblosxom-1.5/`` and
you would set your codebase variable like this::

   py["codebase"] = "/home/joe/pyblosxom-1.5/"


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

   A note about datadir on Windows:

   Use ``/`` to separate directories in the datadir path even if you
   are using Windows.  Examples of valid datadirs on Windows::

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


Blog metadata variables
=======================

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

   Additionally, you can use """ ... """ and ''' ... ''' if you like.


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

FIXME - where can we find more information about what constitutes a
valid encoding value?


blog_language
-------------

**REQUIRED**: yes

**DATATYPE**: string

**DEFAULT VALUE**: no default value--you must set this

This is the primary language code for your blog.

For example, English users should use ``en``::

   py["blog_language"] = "en"


FIXME - where's a list of valid language codes?

This gets used in the RSS flavours.


blog_title
----------

**REQUIRED**: yes

**DATATYPE**: string

**DEFAULT VALUE**: no default value--you must set this

This is the title of your blog.  Typically this should be short and is
accompanied by a longer summary of your blog which is set in
``blog_description``.

For example, if Joe were writing a blog about cooking, he might title
his blog::

   py["blog_title"] = "Joe's blog about cooking"


locale
------

**REQUIRED**: no

**DATATYPE**: string

**DEFAULT VALUE**: "C"

FIXME - this needs to be verified

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

If you set the ``log_level`` to ``critical``, then ONLY critical
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


FIXME - is the channel name == plugin name done automatically by
PyBlosxom or is the channel name specified when logging?



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


Plugin variables
================

plugin_dirs
-----------

**REQUIRED**: no

**DATATYPE**: list of strings

**DEFAULT VALUE**: []

The ``plugin_dirs`` variable lists the directories in which you have
PyBlosxom plugins.

When you set this variable, be sure to set the ``load_plugins``
variable as well.

This defaults to ``[]`` which is an empty list.

For example, if you stored your PyBlosxom plugins in
``/home/joe/blog/plugins/``, then you would set ``plugin_dirs`` like
this::

   py["plugin_dirs"] = ["/home/joe/blog/plugins/"]


load_plugins
------------

**REQUIRED**: no

**DATATYPE**: list of strings

**DEFAULT VALUE**: no default value set

If the ``load_plugins`` variable is set to a list of strings, then
PyBlosxom will load the plugins specified in the order they were
specified in.  If the ``load_plugins`` variable is set to ``[]``
(i.e. an empty list), then PyBlosxom will not load any plugins.

If the ``load_plugins`` variable is not set at all, then PyBlosxom
will load all plugins that it finds in the plugin directories in
alphabetical order.

For example, if you had ``plugin_dirs`` set to
``["/home/joe/blog/plugins/"]`` and there were three plugins in that
directory ``plugin_a.py``, ``plugin_b.py``, and ``plugin_c.py`` and
you did NOT set load_plugins, then PyBlosxom will load ``plugin_a``
followed by ``plugin_b`` followed by ``plugin_c``.

If you wanted PyBlosxom to load ``plugin_a`` and ``plugin_c``, then you
would set ``load_plugins`` to::

   py["load_plugins"] = ["pluginA", "pluginC"]


.. Note::

   ``load_plugins`` should contain a list of strings where each string
   is a Python module--not a filename.  So don't add the ``.py`` to
   the end of the module name!


.. Note::

   In general, it's better to explicitly set ``load_plugins`` to the
   plugins you want to use.  This reduces the confusion about which
   plugins did what when you have problems.  It also reduces the
   potential for accidentally loading plugins you didn't intend to
   load.


.. Note::

   PyBlosxom loads plugins in the order specified by ``load_plugins``.
   This order also affects the order that callbacks are registered and
   later executed.  For example, if plugin_a and plugin_b both
   implement the handle callback and you load plugin_b first, then
   plugin_b will execute before plugin_a when the handle callback
   kicks off.

   Usually this isn't a big deal, however it's possible that some
   plugins will want to have a chance to do things before other
   plugins.  This should be specified in the documentation that comes
   with those plugins.

