===============
Writing Entries
===============

.. _writing-entries:

Categories
==========

Writing entries in PyBlosxom is fairly straightforward.  Each entry is
a single text file located somewhere in the directory tree of your
datadir.  The directory that the entry is in is the category the entry
is "filed under".

For example, if my datadir was ``/home/joe/myblog/entries`` and I
stored an entry named ``firstpost.txt`` in
``/home/joe/myblog/entries/status`` then the category for my entry
would be ``/status``.

.. Warning::

   A warning about category names:

   Be careful when you create your categories---be sure to use
   characters that are appropriate in directory names for the file
   system you're using.

.. Note::

   Categories are NOT the same thing as tags.  An entry can only
   belong to ONE category.  If that's not what you want, you should
   write or install a tags plugin.


Don't worry about making sure you have all the categories you need up
front---you can add them as you need them.



The Format of an Entry
======================

PyBlosxom entries consist of three parts: the title, the metadata, and
then the body of the entry.  The first line is title of the entry.
Then comes zero or more lines of metadata.  After the metadata comes
the body of the entry.


Title
-----

The title consists of a single line of plain text.  You can have
whatever characters you like in the title of your entry.  The title
doesn't have to be the same as the entry file name.  The title is
plain-text.


Metadata
--------

The metadata section is between the title line and the body of the
entry.  It consists of a series of lines that start with the hash mark
``#``, then a metadata variable name, then a space, then the value of
the metadata item.

Example of metadata lines::

   #mood bored
   #music The Doors - Greatest Hits Vol 1


The metadata variables set in the metadata section of the entry are
available in your story template.  So for the above example, the
template variable ``$mood`` would be filled in with ``bored`` and
``$music`` would be filled in with ``The Doors - Greatest Hits Vol
1``.


Body
----

The body of the entry is written in HTML and comprises the rest of the
entry file.


Examples
--------

Here's an example first post entry with a title and a body::

   This is my first post!
   <p>
     This is the body of the first post to my blog.
   </p>


Here's a more complex example with a title and a body::

   The rain in Spain....
   <p>
     The rain
   </p>
   <p align="center">
     in Spain
   </p>
   <p align="right">
     is <font color="ff0000">mainly</font> on the plain.
   </p>


Here's an example of a post with title, metadata, and a body::

   The rain in Spain....
   #mood bored
   #music The Doors - Greatest Hits Vol 1
   <p>
     The rain
   </p>
   <p align="center">
     in Spain
   </p>
   <p align="right">
     is <font color="ff0000">mainly</font> on the plain.
   </p>


Posting Date
============

The posting date of the entry file is the modification time (also
known as mtime) of the file itself as stored by your file system.
Every time you go to edit an entry, it changes the modification time.
You can see this in the following example of output::

   willg ~/blogdata/blosxom/site: vi testpost.txt                         [1]
   willg ~/blogdata/blosxom/site: ls -l
   total 16
   -rw-r--r--  1 willg willg 764 Jul 20  2003 minoradjustments.txt
   -rw-r--r--  1 willg willg 524 Jul 24  2003 moreminoradjustments.txt
   -rw-r--r--  1 willg willg 284 Aug 15  2004 nomorecalendar.txt
   -rw-r--r--  1 willg willg  59 Mar 21 16:30 testpost.txt                [2]
   willg ~/blogdata/blosxom/site: vi testpost.txt                         [3]
   willg ~/blogdata/blosxom/site: ls -l
   total 16
   -rw-r--r--  1 willg willg 764 Jul 20  2003 minoradjustments.txt
   -rw-r--r--  1 willg willg 524 Jul 24  2003 moreminoradjustments.txt
   -rw-r--r--  1 willg willg 284 Aug 15  2004 nomorecalendar.txt
   -rw-r--r--  1 willg willg  59 Mar 21 16:34 testpost.txt                [4]


1. I create the blog entry ``testpost.txt`` using ``vi`` (vi is a text
   editor).  The mtime of the file will be the time I last save the
   file and exit out of vi.

2. Note that the mtime on the file is ``Mar 21 16:30``.  That's when I
   last saved the blog entry and exited out of vi.

3. I discover that I made a spelling mistake in my entry...  So I edit
   it again in vi and fix the mistake.  The mtime of the entry has now
   changed!

4. Now the mtime of the file is ``Mar 21 16:34``.  This is the time
   that will show up in my blog as the posting date.


.. Warning::

   A warning about mtimes:

   There are some issues with this method for storing the posting
   date.  First, if you ever change the blog entry, the mtime will
   change as well.  That makes updating blog entries very difficult
   down the line.

   There's a utility that comes with the contributed plugins pack
   called ``editfile.py``.  This will note the mtime of the file, open
   up your favorite editor to edit the file, and when you're done,
   it'll reset the mtime of the file back to what it was.



Entry Parsers
=============

PyBlosxom supports one format for entry files by default.  This format
is the same format that blosxom uses and is described in previous
sections.

A sample blog entry could look like this::

   First post
   <p>
     Here's the body of my first post.
   </p>


Some people really detest writing in HTML which is valid.  Other
people use their entries in other places, so they need a markup format
that's less web-oriented.  Some folks write a lot of material in a
non-HTML markup format and would like to use that same format for blog
entries.  These are all very valid reasons to want to use other markup
formats.

PyBlosxom allows you to install entry parser plugins which are
PyBlosxom plugins that implement an entry parser.  These entry parser
plugins allow you to use other markup formats.  Check the Plugin
Registry on the `PyBlosxom web-site`_ for other available entry
parsers.

.. _PyBlosxom web-site: http://pyblosxom.sourceforge.net/

Entry parsers can be written by anyone.  The entry parsers that
currently exist were written by people who needed that functionality.

If you don't see your favorite markup format represented, try looking
at the code for other entry parsers and implement it yourself.  If you
need help, talk to us on the pyblosxom-users or pyblosxom-devel
mailing lists.

Details on the various entry parsers should be at the top of the entry
parser plugin itself in the Python doc-string.


Beyond Editors
==============

There's no reason that all your entries have to come from editing blog
entry text files in your datadir.  Check the PyBlosxom Registry for
scripts and other utilities that generate entries from other input
sources.

