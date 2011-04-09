============================
Deploying PyBlosxom with CGI
============================

Dependencies
============

You need a server that can do CGI and you need to know how to run CGI
scripts with the correct permissions on your server.


Deployment
==========

Copy the ``pyblosxom.cgi`` file from the blog directory (the directory
which you created with ``pyblosxom-cmd create ./blog/``) into your CGI directory.

Edit the ``pyblosxom.cgi`` file.

The top of the file looks something like this::

    #!/usr/bin/env python

    # -u turns off character translation to allow transmission
    # of gzip compressed content on Windows and OS/2
    #!/path/to/python -u

    import os, sys

    # Uncomment this line to add the directory your config.py file is in to the
    # python path:
    #sys.path.append("/path/to/directory/")


Make sure the first line points to a valid python interpreter.  If
you're using virtualenv, then make sure it points to the python
interpreter in the virtual environment.

Uncomment the ``sys.path.append("/path/to/directory/")`` line and
make sure the path being appended is the directory that your ``config.py``
file is in.

Make sure the ``pyblosxom.cgi`` file has the correct permissions and
ownership for running a CGI script in this directory.

Make sure your blog directory has the correct permissions for being
read by the process executing your CGI script.

Run your ``pyblosxom.cgi`` script by doing::

    % ./pyblosxom.cgi test

If that doesn't work, double-check to make sure you've completed the
above steps, then check the trouble-shooting section below, then ask for
help on IRC or the users mailing list.  More details in 
:ref:`project-details-and-contact`.


If that works, then try to run the CGI script from your web-browser.
The url is dependent on where you put the ``pyblosxom.cgi`` script and
how CGI works on your web-server.


Trouble-shooting
================

We're going to try to break this down a bit into categories. Bear with
us and keep trying things. If you have problems and have gone through
this section to no avail, then come talk to us on the pyblosxom-user
list or on IRC.  Details of the mailing list are located at our
contact page.


Running ./pyblosxom.cgi doesn't work
------------------------------------

First, you should check to see if you have the minimum requirements
for PyBlosxom on your system.  If not, then please install them.
They're listed in the :ref:`Requirements section of the Install
chapter <requirements>`.

If Python is installed on your system, make sure the first line in
``pyblosxom.cgi`` points to your Python interpreter.  By default,
``pyblosxom.cgi`` uses ``env`` to execute the Python interpreter.  But
in some rare systems, ``/usr/bin/env`` doesn't exist.  Or the
system may have odd environment settings.  In those cases, you may
edit the first line to point to your Python interpreter directly,
e.g.::

    #!/usr/bin/python

Then try running ``./pyblosxom.cgi`` again.

If Python is installed on your system and the first line of
``pyblosxom.cgi`` is correct, check for permissions issues.
``pyblosxom.cgi`` is a script, so it needs execute permission in order
to function.  If those aren't set, then fix that and try running
``./pyblosxom.cgi`` again.

Check the error logs for your web-server.


I see a HTTP 404 error when I try to bring up my blog
-----------------------------------------------------

When you try to look at your blog and you get a HTTP 404 error, then
you're using the wrong URL.  Here are some questions to ask yourself:

* Are you using an ``.htaccess`` file?
* Does your server allow you to run CGI scripts?
* Do other CGI scripts in this directory work?
* Does the URL you're trying to use to access PyBlosxom look like
  other URLs that work on your system?


I see a HTTP 500 error when I try to bring up my blog
-----------------------------------------------------

At this point, running ``./pyblosxom.cgi`` at the command prompt
should work fine.  If you haven't done that and you're busy
trouble-shooting, go back and review the deployment instructions.

If the problem is with PyBlosxom and not your web-server, then you
should see a pretty traceback that will help you figure out what the
specific problem is.

If it doesn't make any sense to you, you can copy and paste that into
an email to the pyblosxom-users mailing list and we're in a better
position to help you out.

If you don't see a traceback, then you either have a configuration
problem with your web-server or a configuration problem with Python.
The first thing you should do is check your web-server's error logs.
For Apache, look for the ``error.log`` file in a place like
``/var/logs/apache/`` or ``/var/logs/httpd/``.

Does the account your web-server runs as have execute access to your
``pyblosxom.cgi`` script?  If your web-server does not have the
permissions to read and execute your ``pyblosxom.cgi`` script, then
your blog will not work.

Do you have plugins loaded?  If you do, try unloading all your plugins
and see if the problem persists.  Sometimes there are issues with
plugins that only show up in certain situations.


I have other issues
-------------------

Try changing the renderer for your blog to the debug renderer.  You
can do this by setting the ``renderer`` property in your ``config.py``
file to ``debug``. That will show a lot more detail about your
configuration, what the web-server passes PyBlosxom in environment
variables, and other data about your blog that might help you figure
out what your problem is.


UGH! My blog looks UGLY!
------------------------

Read the documentation regarding Flavours and Templates to help you out.

If you're reading this documentation online, then it is 
:ref:`here <flavours-and-templates>`.


I hate writing in HTML!
-----------------------

That's ok.  PyBlosxom supports formatters and entry parsers which
allow you to use a variety of markups for writing blog entries.  See
the documentation on Writing Entries for more information.

If you're reading this documentation online, then it is 
:ref:`here <writing-entries>`.


Advanced installation
=====================

We encourage you not to try any of this until you've gotten a blog up
and running.

This section covers additional advanced things you can do to your blog
that will make it nicer.  However, they're not necessary and they're
advanced and we consider these things to be very much a "you're on
your own" kind of issue.

If you ever have problems with PyBlosxom and you ask us questions on
the pyblosxom-users or pyblosxom-devel mailing lists, make sure you
explicitly state what things you've done from this chapter.  It'll go
a long way in helping us to help you.


Renaming the pyblosxom.cgi script
=================================

In the default installation, the PyBlosxom script is named
``pyblosxom.cgi``.

For a typical user on an Apache installation with user folders turned
on, PyBlosxom URLs could look like this::

    http://www.joe.com/~joe/cgi-bin/pyblosxom.cgi
    http://www.joe.com/~joe/cgi-bin/pyblosxom.cgi/an_entry.html
    http://www.joe.com/~joe/cgi-bin/pyblosxom.cgi/dev/another_entry.html 


That gets pretty long and it's not very good looking.  For example,
telling the URL to your mother or best friend over the phone would be
challenging.  It would be nice if we could shorten and simplify it.

So, we have some options:

* Change the name of the ``pyblosxom.cgi`` script.

* And if that's not good enough for you, use the Apache mod_rewrite
  module to get URLs internally redirected to the ``pyblosxom.cgi``
  script.

Both methods are described here in more detail.


Change the name of the pyblosxom.cgi script
-------------------------------------------

There's no reason that ``pyblosxom.cgi`` has to be named
``pyblosxom.cgi``.  Let's try changing it ``blog``.  Now our example
URLs look like this::

    http://www.joe.com/~joe/cgi-bin/blog
    http://www.joe.com/~joe/cgi-bin/blog/an_entry.html
    http://www.joe.com/~joe/cgi-bin/blog/category1/another_entry.html 


That's better looking in the example.  In your specific circumstances,
that may be all you need.

You might have to change the ``base_url`` property in your
``config.py`` file to match the new URL.

.. Note::

    The ``base_url`` value should NOT have a trailing slash.


If you're running on Apache, you might have to tell Apache that this
is a CGI script even if it doesn't have a ``.cgi`` at the end of it.
If you can use ``.htaccess`` files to override Apache settings, you
might be able to do something like this::

    # this allows execution of CGI scripts in this directory
    Options ExecCGI 

    # if the user doesn't specify a file, then instead of doing the
    # regular directory listing, we look at "blog" (which is our
    # pyblosxom.cgi script renamed)
    DirectoryIndex blog 

    # this tells Apache that even though "blog" doesn't end in .cgi,
    # it is in fact a CGI script and should be treated as such
    <Files blog> 
    ForceType application/cgi-script  
    SetHandler cgi-script  
    </Files>


You may need to stop and restart Apache for your Apache changes to
take effect.


Hiding the .cgi with RewriteRule
--------------------------------

Apache has a module for URL rewriting which allows you to convert
incoming URLs to other URLs that can be handled internally.  You can
do URL rewriting based on all sorts of things.  See the Apache manual
for more details.

In our case, we want all incoming URLs pointing to ``blog`` to get
rewritten to ``cgi-bin/pyblosxom.cgi`` so they can be handled by
PyBlosxom.  Then all our URLs will look like this::

    http://www.joe.com/~joe/blog
    http://www.joe.com/~joe/blog/an_entry.html
    http://www.joe.com/~joe/blog/category1/another_entry.html


To do this, we create an .htaccess file (it has to be named exactly
that) in our ``public_html`` directory (or wherever it is that /~joe/
points to).  In that file we have the following code::

    RewriteEngine on
    RewriteRule   ^blog?(.*)$   /~joe/cgi-bin/pyblosxom.cgi$1   [last]


The first line turns on the Apache mod_rewrite engine so that it will
rewrite URLs.

The second line has four parts.  The first part denotes the line as a
RewriteRule.  The second part states the regular expression that
matches the part of the URL that we want to rewrite.  The third part
denotes what we're rewriting the URL to.  The fourth part states that
after this rule is applied, no future rewrite rules should be applied.

If you do URL rewriting, you may have to set the base_url property in
your ``config.py`` accordingly.  In the above example, the
``base_url`` would be ``http://www.joe.com/~joe/blog`` with no
trailing slash.

For more information on URL re-writing, see the Apache documentation
(1.3_, 2.0_, 2.2_).

.. _1.3: http://httpd.apache.org/docs/1.3/mod/mod_rewrite.html
.. _2.0: http://httpd.apache.org/docs/2.0/mod/mod_rewrite.html
.. _2.2: http://httpd.apache.org/docs/2.2/mod/mod_rewrite.html

