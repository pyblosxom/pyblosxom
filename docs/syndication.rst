===========
Syndication
===========

Summary
=======

Syndicating your blog is very important as it provides a mechanism for
readers of your blog to keep up to date.  Typically this is done with
newsreader software.  Additionally, there are websites that post blog
entries from a variety of blogs that have similar content.  Both
newsreaders and planet-type websites need a semantically marked up
version of your blog.

Most newsreaders read most of the syndication formats.  So you
shouldn't feel that you have to implement each one of them in your
blog---you can most assuredly get away with implementing RSS 2.0 or
Atom and be just fine.

The syndication flavours that come with Pyblosxom should be fine for
most blogs.  When pointing people to your syndication feed, just use
one of the syndication flavours.

Examples:

* ``http://example.com/blog/index.rss``
* ``http://example.com/~willg/blog/index.rss20``
* ``http://example.com/index.atom``



Feed formats that come with Pyblosxom
=====================================

Pyblosxom comes with a few default flavours, three of which are feed
formats.


RSS 0.9.1
---------

Pyblosxom comes with an rss flavour that produces RSS 0.9.1 output.
Here's a sample of what it produces::

   <?xml version="1.0" encoding="utf-8"?>
   <!-- name="generator" content="pyblosxom/1.2 3/25/2005" -->
   <!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN"
   "http://my.netscape.com/publish/formats/rss-0.91.dtd">

   <rss version="0.91">
   <channel>
   <title>My Blog</title>
   <link>http://www.joe.com/blog/index.rss</link>
   <description>This is my blog about trivial things</description>
   <language>en</language>
   <item>
       <title>Example of an entry post</title>

       <link>http://www.joe.com/blog/entries/example1.html</link>
       <description>&lt;p&gt;
     Here's an example of an entry in my blog.  This is the body of the entry.
   &lt;/p&gt;
   </description>
     </item>
   </channel>
   </rss>


This example only has one entry in it.  The number of entries the rss
flavour will display is determined by the ``num_entries` property in
your ``config.py`` file.

.. Note::

   Probably better not to use RSS 0.9.1:

   RSS 0.9.1 format lacks dates in the data for the items.  Unless you
   include the date for the entry somewhere in the description block,
   people looking at your RSS 0.9.1 feed won't know what the date the
   entry was created on was.
 
   Unless you have some reason to use RSS 0.9.1 as your syndication
   format, you should look at using RSS 2.0 or Atom both of which
   also come with Pyblosxom.


For more information, look at the `RSS 0.9.1 spec`_.

.. _RSS 0.9.1 spec: http://my.netscape.com/publish/formats/rss-spec-0.91.html



RSS 2.0
-------

Pyblosxom 1.3 comes with an RSS 2.0 flavour called "rss20".  If it's
missing features that you want (for example, some folks are doing
podcasting with their blog), then override the individual templates
you need to adjust.

For more information on RSS 2.0, see the `RSS 2.0 spec`_.

.. _RSS 2.0 spec: http://blogs.law.harvard.edu/tech/rss



Atom
----

Starting with 1.3, Pyblosxom comes with an Atom flavour called "atom".
If it's missing features that you want, then override the individual
templates you need to adjust.

For more information on Atom, see the `Atom spec`_.

.. _Atom spec: http://atomenabled.org/



Debugging your feeds
====================

`FeedValidator`_ is a useful tool for figuring out whether your
feed is valid and fixing bugs in your feed content.

.. _FeedValidator: http://feedvalidator.org/

Additionally, feel free to ask on the pyblosxom-users mailing list.
