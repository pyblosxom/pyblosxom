======================
Flavours and Templates
======================

.. _flavours-and-templates:


Summary
=======

This chapter covers the blosxom renderer in PyBlosxom.  There are other
renderers (like the debug renderer) that operate differently.  See
the chapter on :ref:`renderers <renderers>` for more details.

If you want your blog rendered using a different template system---say
Cheetah or htmltmpl---implement a renderer that renders the output.
This new renderer can be implemented as a PyBlosxom plugin.  See the
chapter on writing plugins for more information.

The rest of this chapter talks about the various things you can do with
the blosxom renderer which comes with PyBlosxom.



Flavours and Templates
======================

The blosxom renderer renders the output of a request with a
:term:`flavour`.

A :term:`flavour` is a group of templates for a specific output format
or style.  For example, html, xhtml, atom, rss, rdf, etc.

A flavour consists of at least the following templates:

* **content_type** - holds the content type of the flavour
* **head** - holds everything before all the entries
* **story** - holds a single entry
* **foot** - holds everything after all the entries
* **date_head** - shows at the start of a date
* **date_foot** - shows at the end of a date

.. Note::

   Many plugins require additional templates to render their output in
   addition ot the standard templates listed above.  See the
   documentation for the plugin for more information.

More on flavours, how they're stored, and such later.

A :term:`template` is one piece of a flavour that specifies a specific
portion of the output.  For example, the head template of an html
flavour would be in a file called ``head`` and might look like this::

    <html>
    <head>
       <title>$(blog_title)</title>
    </head>
    <body>

More on templates later.

PyBlosxom allows you to manage the flavours and templates for your
blog in several different ways:

1. in directories in the flavourdir, OR
2. in directories in the datadir, OR
3. in the datadir along with your entries.

.. Note::

   PyBlosxom is backwards compatible with previous versions of
   PyBlosxom.  You can put your flavour files in your datadir.  You
   can also put your flavour files in the categories of your datadir.
   However you cannot have a flavourdir and put flavour files in your
   datadir---PyBlosxom will look at **EITHER** your datadir **OR**
   your flavourdir for flavour files.


Storing flavours in the flavourdir
----------------------------------

This is the easiest way to store your flavours separately from the
entries in your blog.  This is the preferred way.

If you specify the ``flavourdir`` directory in your ``config.py`` file,
you can store each flavour in a directory in the flavourdir.

For example, Joe has this in his ``config.py``::

   py["flavourdir"] = "/home/joe/blog/flavours/"

Joe's blog directory structure would look like this::

   /home/joe/blog/
             |- entries/             <-- datadir
             |  |- work/             <-- work category of entries
             |  |- home/             <-- home category of entries
             |
             |- flavours/
                |- html.flav/        <-- html flavour
                |  |- content_type
                |  |- head
                |  |- foot
                |  |- story
                |  |- ...
                |
                |- rss.flav/         <-- rss flavour
                |  |- content_type
                |  |- head
                |  |- foot
                |  |- story
                |  |- ...

The ``flavourdir`` specifies the directory in which Joe stores his
flavours.

.. Note::

   Flavour directories must end in ``.flav``.

.. Note::

   Templates in the flavour directory don't need an extension.

This structure also makes it easier to use flavour packs found in the
flavour registry on the `PyBlosxom website`_.

.. _PyBlosxom website: http://pyblosxom.sourceforge.net/



Storing flavours in flavour directories in the datadir
------------------------------------------------------

Flavours can be stored in directories in the directory specified by
your datadir.  This works exactly the same as having a separate
flavourdir except that the flavourdir is not a separate directory
tree---it's the same tree as your datadir.

For example, Joe stores his flavours alongside his entries and his
blog directory tree looks like this::

   /home/joe/blog/
             |- entries/             <-- datadir
                |- html.flav/        <-- html flavour
                |  |- content_type
                |  |- head
                |  |- foot
                |  |- story
                |  |- ...
                |
                |- work/             <-- work category of entries
                |  |- html.flav/     <-- html flavour for the work category
                |  |- ...
                |
                |- home/             <-- home category of entries

In this way your entries are intermixed with your flavour directories.


Storing flavours in the datadir
-------------------------------

Instead of storing flavour templates in separate flavour directories
in either your datadir or your flavourdir, you can store the templates
alongside your entries.

This is not recommended---it's a pain in the ass to maintain and
everything gets all mixed up.  It's supported since this is how
PyBlosxom used to work.

The template files for a given flavour all have to have the flavour
name as the extension of the file.  For example, if you were using an
"html" flavour, the flavour itself would be composed of the following
files:

* ``content_type.html``
* ``head.html``
* ``story.html``
* ``foot.html``
* ``date_head.html``
* ``date_foot.html``

If you want to create an "atom" flavour, you would have the following
files:

* ``content_type.atom``
* ``head.atom``
* ``story.atom``
* ``foot.atom``
* ``date_head.atom``
* ``date_foot.atom``

.. Warning::

   If you intermix flavour templates with entries, make sure you don't
   have flavours that have the same name as the extension of your blog
   entries.

   For example, if ``.txt`` is the extension for entries in your blog,
   don't create a **txt** flavour!


Included flavours
=================

PyBlosxom comes with the following flavours:

* ``html`` - a basic html flavour
* ``rss`` - an RSS 2.0 flavour for syndication
* ``atom`` - an Atom 1.0 flavour for syndication

These flavours are included with PyBlosxom and they will work out of the
box with no modifications and no configuration changes.

When you run ``pyblosxom-cmd create <blog-dir>``, these get copied
into the flavourdir.

Play with them!  Modify them!  Extend them!


Overriding included flavours
============================

PyBlosxom allows you to override templates and flavours on a
category-by-category basis.

For example, Joe has a category devoted to his work on plants which he
wants branded differently than the rest of his blog.  Joe uses the
category *work* for all his plant work and has a different flavour for
this category of his blog.

Joe's blog directory looks like this::

   /home/joe/blog/
             |- entries/             <-- datadir
             |  |- work/             <-- work category of entries
             |  |- home/             <-- home category of entries
             |
             |- flavours/
                |- html.flav/        <-- html flavour
                |  |- content_type
                |  |- head
                |  |- foot
                |  |- story
                |  |- ...
                |
                |- work/
                   |- html.flav/     <-- html flavour for the work category
                   |- ...

There is a ``work`` directory in his ``flavours`` directory that
parallels the ``work`` directory in his ``entries`` directory.  In
Joe's blog, the work category has a different html flavour than the
root and home categories.

You can override individual templates, too.

For example, if you had a math category and wanted the story template
to look different, you could set up your blog like this::

   blog/
     |- entries/
     |  |- math/             <-- math category in datadir
     |
     |- flavours/
        |- html.flav/
        |  |- content_type
        |  |- head
        |  |- date_head
        |  |- story
        |  |- date_foot
        |  |- foot
        |
        |- math/             <-- math category in flavourdir
           |- html.flav/
              |- story

If the request is for an entry in the math category, then the ``story``
file will be taken from the ``flavours/math/html.flav/`` directory and
the rest of the templates will be taken from ``flavours/html.flav/``.


Finding new flavours
====================

There is a flavour registry on the `PyBlosxom website`_.  You can find
flavours here that have been created by other people and submit
flavours that you've created and want to share.

.. _PyBlosxom website: http://pyblosxom.sourceforge.net/

Additionally, you can use flavours from `Blosxom`_ and themes from
`WordPress`_ after spending some time converting them.

.. _Blosxom: http://www.blosxom.com/
.. _WordPress: http://wordpress.org/

The order of overiding works like this:

1. PyBlosxom looks for flavour files that came with PyBlosxom
2. PyBlosxom starts at the root of the flavourdir and looks for
   flavour files there.  If there are some, then these files override
   the files PyBlosxom has found so far.
3. PyBlosxom iterates through category directories in the flavourdir
   if there are any that are parallel to the datadir and looks for
   flavour directories there.  If there are some, then those files
   override the files it has so far.

This allows you to easily override specific templates in your blog
(like the header or footer) depending on what category the user is
looking at.


Template Variables
==================

This is the list of variables that are available to your templates.
Templates contain variables that are expanded when the template is
rendered.  Plugins may add additional variables---refer to plugin
documentationfor a list of which variables they add and in which
templates they're available.


Variable syntax
---------------

To use a variable in a template, prefix the variable name with a $.
For example, this would expand to the blog's title as a h2::

   <h2>$title</h2>

PyBlosxom 1.4.3 and later support parenthesized variables, too::

   <h2>$(title)</h2>

This reduced ambiguity.

PyBlosxom 1.5 also supports variables that expand into functions which
are evaluated::

   <h2>$(escape(title))</h2>


Getting a complete list of variables
------------------------------------

To get a complete list of what variables are available in your blog,
use the debug renderer by changing the value of the ``renderer``
property in your ``config.py`` file to ``debug`` like this::

   py["renderer"] = "debug"


That will tell you all kinds of stuff about the data structures
involved in the request.  Don't forget to change it back when you're
done!


URL Encoding and Escaping of Template Variables
-----------------------------------------------

PyBlosxom 1.5 and later has two filters allowing for escaped and
urlencoded values:

* ``$escape(title)`` - escapes ``$title``
* ``$urlencode(title)`` - urlencoded ``$title``


Plugins can add additional filters.

.. Note::

   PyBlosxom versions 1.3 and 1.4 escaped and urlencoded variables
   that ended with ``_escaped`` and ``_urlencoded``.

   Deprecated in PyBlosxom 1.5.


Variables from config.py
------------------------

Anything in your ``config.py`` file is a variable available to all of
your templates.  For example, these standard properties in your
``config.py`` file are available:

* ``blog_description``
* ``blog_title``
* ``blog_language``
* ``blog_encoding``
* ``blog_author``
* ``blog_email``
* ``base_url`` (if you provided it)
* ...


Additionally, any other properties you set in ``config.py`` are
available in your templates.  If you wanted to create a
``blog_images`` variable holding the base url of the directory with
all your images in it::

   py["blog_images"] = "http://www.joe.com/~joe/images/"


to your ``config.py`` file and it would be available in all your
templates.


Calculated template variables
-----------------------------

These template variables are available to all templates as well.  They
are calculated based on the request.

``root_datadir``
   The root datadir of this page?

   Example: ``/home/subtle/blosxom/weblogs/tools/pyblosxom``

``url``
   The PATH_INFO to this page.

   Example: ``pyblosxom/weblogs/tools/pyblosxom``

``flavour``
   The flavour that's being used to render this page.

   Example: ``html``

``latest_date``
   The date of the most recent entry that is going to be rendered.

   Example: ``Tue, 15 Nov 2005``

``latest_w3cdate``
   The date of the most recent entry that is going to be rendered in 
   w3cdate format.

   Example: ``2005-11-13T17:50:02Z``

``latest_rfc822date``
   The date of the most recent entry that is going to show in RFC 822 
   format.

   Example: ``Sun, 13 Nov 2005 17:50 GMT``

``pi_yr``
   The four-digit year if the request indicated a year.

   Example: ``2002``

``pi_mo``
   The month name if the request indicated a month.

   Example: ``Sep``

``pi_da``
   The day of the month if the request indicated a day of the month.

   Example: ``15``

``pi_bl``
   The entry the user requested to see if the request indicated a
   specific entry.

   Example: ``weblogs/tools/pyblosxom``

``pyblosxom_version``
   The version number and release date of the pyblosxom version you're
   using.

   Example: ``1.2 3/25/2005``


Template variables only available in the date_head and date_foot templates
--------------------------------------------------------------------------

``date_head`` and ``date_foot`` templates have these additional
variables:

``date``
   The date string of this day. 

   Example: ``Sun, 23 May 2004``


Template variables only available in the story template
-------------------------------------------------------

These template variables are only available in your story template.

``title``
   The title of the entry.

   Example: ``First Post!``

``filename``
   The absolute path of the file that the entry is stored in.

   Example: ``/home/subtle/blosxom/weblogs/tools/pyblosxom/firstpost.txt``

``file_path``
   The filename and extension of the file that the entry is stored in.

   Example: ``firstpost.txt``

``fn``
   The filename with no extension of the file that the entry is stored
   in.

   Example: ``firstpost``

``absolute_path``
   The category/path of the entry (from the perspective of the url).

   Example: ``weblogs/tools/pyblosxom``

``body``
   The text of the entry.

   Example: ``<p>This is my first post!</p>``

``tb_id``
   The trackback id of the entry.

   Example: ``_firstpost``

``path``
   The category/path of the entry.

   Example: ``weblogs/tools/pyblosxom``

``yr``
   The four-digit year of the mtime of this entry.

   Example: ``2004``

``mo``
   The month abbreviation of the mtime of this entry.

   Example: ``Jan``

``mo_num``
   The zero-padded month number of the mtime of this entry.

   Example: ``01``

``ti``
   The 24-hour hour and minute of the mtime of this entry.

   Example: ``16:40``

``date``
   The date string of the mtime of this entry.

   Example: ``Sun, 23 May 2004``

``w3cdate``
   The date in w3cdate format of the mtime of this entry.

   Example: ``2005-11-13T17:50:02Z``

``rfc822date``
   The date in RFC 822 format of the mtime of this entry.

   Example: ``Sun, 13 Nov 2005 17:50 GMT``

``fulltime``
   The date in YYYYMMDDHHMMSS format of the mtime of this entry.

   Example: ``20040523164000``

``timetuple``
   The time tuple (year, month, month-day, hour, minute, second,
   week-day, year-day, isdst) of the mtime of this entry.

   Example: ``(2004, 5, 23, 16, 40, 0, 6, 144, 1)``

``mtime``
   The mtime of this entry measured in seconds since the epoch.

   Example: ``1085348400.0``

``dw``
   The day of the week of the mtime of this entry.

   Example: ``Sunday``

``da``
   The day of the month of the mtime of this entry.

   Example: ``23``


Also, any variables created by plugins that are entry-centric and any
variables that come from metadata in the entry are available.  See
those sections in this document for more details.


Template Variables from Plugins
-------------------------------

Many plugins will create additional variables that are available in
templates.  Refer to the documentation of the plugins that you have
installed to see what variables are available and what they do.


Template Variables from Entry Metadata
--------------------------------------

You can add metadata to your entries on an individual basis and this
metadata is available to your story templates.

For example, if I had a blog entry like this::

   First Post!
   #mood happy
   #music The Doors - Break on Through to the Other Side
   <p>
     This is the first post to my new PyBlosxom blog.  I've
     also got two metadata items in it which will be available
     as variables!
   </p>


You'll have two variables ``$mood`` and ``$music`` that will also be
available in your story templates.



Invoking a Flavour
==================

The flavour for a given page is specified in the extension of the file
being requested.  For example:

* ``http://some.blog.org/`` - 
  brings up the index in the default flavour which is "html"

* ``http://some.blog.org/index.html`` - 
  brings up the index in the "html" flavour

* ``http://some.blog.org/index.rss`` -
  brings up the index in the "rss" flavour (which by default is RSS 0.9.1)

* ``http://some.blog.org/2004/05/index.joy`` -
  brings up the index for May of 2004 in the "joy" flavour


Additionally, you can specify the flavour by adding a ``flav``
variable in the query-string.  Examples:

* ``http://some.blog.org/`` -
  brings up the index in the default flavour which is "html"

* ``http://some.blog.org/?flav=rss`` -
  brings up the index in the "rss" flavour

* ``http://some.blog.org/2004/05/index?flav=joy`` -
  brings up the index for May of 2004 in the "joy" flavour


Setting Default Flavour
=======================

You can change the default flavour from ``html`` to some other flavour
in your ``config.py`` file with the ``default_flavour`` property::

   py["default_flavour"] = "joy"


Doing this will set the default flavour to use when the URI the user
has used doesn't specify which flavour to use.

This url doesn't specify the flavour to use, so it will be rendered
with the default flavour::

   http://www.joe.com/cgi-bin/pyblosxom.cgi/2005/03

This url specifies the flavour, so it will be rendered with that
flavour::

   http://www.joe.com/cgi-bin/pyblosxom.cgi/2005/03/?flav=html


Order of Operations to Figure Out Which Flavour to Use
======================================================

We know that you can specify the default flavour to use in the
``config.py`` file with the ``default_flavour`` property.  We know
that the user can specify which flavour to use by the file extension
of the URI.  We also know that the user can specify which flavour to
use by using the ``flav`` variable in the query string.

The order in which we figure out which flavour to use is this:

1. look at the URI extension: if the URI has one, then we use that.
2. look at the ``flav`` querystring variable: if there is one, 
   then we use that.
3. look at the ``default_flavour`` property in the ``config.py`` 
   file: if there is one, then we use that.
4. use the ``html`` flavour.


Examples of Templates
=====================

For examples of templates and flavours, see the included flavours that
come with your PyBlosxom installation.
