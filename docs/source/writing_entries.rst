===============
Writing Entries
===============

Categories
==========

Writing entries in PyBlosxom is fairly straightforward.  Each entry
is a single text file located somewhere in the directory tree of your
datadir.  The directory that the entry is in is the category the entry
is "filed under".  

For example, if my datadir was ``/home/joe/myblog/entries`` and I stored 
an entry named ``firstpost.txt`` in ``/home/joe/myblog/entries/status`` 
then the category for my entry would be ``/status``.

.. Warning::

   A warning about category names:

   Be careful when you create your categories--be sure to use characters
   that are appropriate in directory names in the file system.


Don't worry about making sure you have all the categories you need up
front--you can add them as you need them.



The Format of an Entry
======================

PyBlosxom entries consist of three parts: the title, the metadata, and
then the body of the entry.  The first line is title of the entry.  Then
comes the metadata of the entry (if any).  After the metadata comes the
body of the entry.

The title consists of a single line of plain text.  You can have whatever
characters you like in the title of your entry.  The title doesn't have
to be the same as the entry file name.

The metadata section is between the title line and the body of the entry.
It consists of a series of lines that start with the hash mark (#), then
a metadata variable name, then the metadata variable value.

The body of the entry is written in HTML and comprises the rest of the
entry file.

Here's an example first post entry::

   This is my first post!
   <p>
     This is the body of the first post to my blog.
   </p>


Here's a more complex example::

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


Here's an example of a post with metadata::

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


The metadata variables set in the metadata section of the entry are 
available in your story template.  So for the above example, the template 
variable ``$mood`` would be filled in with ``bored`` and ``$music``
would be filled in with ``The Doors - Greatest Hits Vol 1``.



Posting Date
============

The posting date of the entry file is the modification time (also known as
mtime) on the file itself as stored by your file system.  Every time you 
go to edit an entry, it changes the modification time.  You can see this
in the following example of output::

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
   editor).  The mtime of the file will be the time I last save the file 
   and exit out of vi.

2. Note that the mtime on the file is ``Mar 21 16:30``.  That's when I 
   last saved the blog entry and exited out of vi.

3. I discover that I made a spelling mistake in my entry...  So I edit
   it again in vi and fix the mistake.  The mtime of the entry has now 
   changed!

4. Now the mtime of the file is ``Mar 21 16:34``.  This is the time that 
   will show up in my blog as the posting date.


.. Warning::

   A warning about mtimes:

   There are some issues with this method for storing the posting date.  
   First, if you ever change the blog entry, the mtime will change as well.  
   That makes updating blog entries very difficult down the line.

   There's a utility that comes with the contributed plugins pack called 
   ``editfile.py``.  This will note the mtime of the file, open up your 
   favorite editor to edit the file, and when you're done, it'll reset 
   the mtime of the file back to what it was.



Entry Parsers
=============

PyBlosxom supports only one format for entry files by default.  This format
is the same format that blosxom uses.  The extension for this format is 
``.txt``.  The first line of the file is in plain text and forms the title 
of the entry.  The second line through the end of the file is in HTML and 
is the body of the entry.

A sample blog entry could look like this::

   First post
   <p>
     Here's the body of my first post.
   </p>


Some people really detest writing in HTML which is valid.  Other 
people use their entries in other places, so they need a markup format 
that's less web-oriented.  Some folks write a lot of material in a non-HTML 
markup format and would like to use that same format for blog entries.  
These are all very valid reasons to want to use other markup formats.

PyBlosxom allows you to install entry parser plugins which are PyBlosxom 
plugins that implement an entry parser.  These entry parser plugins allow 
you to use other markup formats.  Check the Plugin Registry at 
http://pyblosxom.sourceforge.net/ for which entry parsers are available.

In general, we only have entry parsers written by people who really 
wanted that markup format.  If you don't see your favorite markup format 
represented, try looking at the code for other entry parsers and implement 
it yourself.  If you need help, talk to us on the pyblosxom-users or 
pyblosxom-devel mailing lists.

Details on the various entry parsers should be at the top of the entry
parser plugin itself in the Python doc-string.



Beyond Editors
==============

There's no reason that all your entries have to come from editing blog entry
text files in your datadir.  You could rig up procmail to look for emails
that meet a certain description and convert those emails into blog entries.



weblog-add
----------

You can find the weblog-add CGI script in the Plugin Registry at
http://pyblosxom.sourceforge.net/ .  This script allows you to create
entries using a webform.  It doesn't allow you to edit entries after
the fact and it's pretty basic.  However, it does work and it does allow
you to create entries when you don't have access to the filesystem.

To setup the weblog-add script, do the following:

1. copy the ``weblog-add.py`` file into your CGI root

2. open up the ``weblog-add.py`` file in your favorite text editor 
   and change the line for ``blog_root`` to your datadir

3. set up your cgi directory so that the web-server forces the user to
   authenticate

   FIXME - how do you do that?

4. make sure the weblog-add.py file has the correct permissions so that 
   it will run as a CGI script


When you're using the ``weblog-add.py`` script, make sure you use unique 
file names.  That gets a bit hard as your blog gets so big that you 
don't remember what file names exist and what don't.


w.bloggar
---------

PyBlosxom works with w.bloggar (http://www.wbloggar.com/).  In order to 
use w.bloggar you have to do the following:

1. install the xmlrpc plugin found at http://pyblosxom.sourceforge.net/ in 
   the plugin registry

2. install the xmlrpc_bloggar plugin also in the plugin registry

3. in the **Content Management System** section of the w.bloggar account 
   settings dialog, set:

   * **Blog Tool** to ``Custom``
   
4. in the **API Server** tab section of the w.bloggar account settings 
   dialog, set:

   * **Host** to the name of your server
   * **Page** to the url of your blog with /RPC at the end.  For example, 
     mine might be "/~joe/cgi-bin/pyblosxom.cgi/RPC"

5. in the **Custom** tab section of the w.bloggar account settings dialog, 
   set:

   * **Posts** to ``Blogger API``
   * **Categories** to ``Not supported``
   * **Templates** to ``Not supported``
   * **Title Tags** should be blank
   * **Category Tags** should be blank


When you go to write a new entry, leave the title field blank and do your 
entire post in the data section with the first line being the title (just 
like blosxom entries).

One thing you should note is that pyblosxom will take the first line and use 
that to generate the file name of the entry.  So if the title of the entry is 
``How to use w.bloggar with pyblosxom``, the file name ends up being 
``How_to_use_w_bloggar_with_pyblosxom.txt`` which may get a little annoying.

FIXME - Does this still work?


Using Ecto
----------

FIXME - I need instructions for this


Other blog tools?

Does PyBlosxom work with other blog tools?  If you have such a tool, please
let us know!
