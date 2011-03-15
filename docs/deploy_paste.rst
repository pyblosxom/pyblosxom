==============================
Deploying PyBlosxom with Paste
==============================

Summary
=======

PyBlosxom 1.4 and later support Paste.  This document covers
installing and using PyBlosxom with Paste.

This installation assumes you have some understanding of Python Paste.
If this doesn't sound like you, then you can read up on Paste on
the `Paste website`_ or the `Wikipedia page`_.


.. _Paste website: http://pythonpaste.org/
.. _Wikipedia page: http://en.wikipedia.org/wiki/Python_Paste

Dependencies
============

* Python Paste which can be found at http://pythonpaste.org/

Additionally, if you're using an earlier version of Python than
Python 2.5, then you'll also need:

* wsgiref library from http://svn.eby-sarna.com/wsgiref/


Deployment for testing
======================

Create a new blog by doing::

    pyblosxom-cmd create <BLOG-DIR>

Then do::

    cd <BLOG-DIR>
    paster serve blog.ini

The ``paster`` script will print the URL for your blog on the command
line and your blog is now available on your local machine to a
browser on your local machine.

This allows you to test your blog and make sure it works.


Deployment with mod_wsgi
========================

Paste makes it really easy to use with ``mod_wsgi``.

1. Create a file named ``something.wsgi`` like this one::

       # If you're using a virtualenv, uncomment the next two lines and
       # change '/path/to/activate_this.py'.
       # activate_this = '/path/to/activate_this.py'
       # execfile(activate_this, dict(__file__=activate_this))

       from Pyblosxom.pyblosxom import pyblosxom_app_factory
       from paste.deploy import loadapp

       # Fill in path to Paste .ini config file here
       application = loadapp('config:/path/to/wsgi.ini')

2. In the Apache httpd.conf file::

       WSGIScriptAlias /myblog /path/to/something.wsgi

       <Directory /path/to>
           Order deny,allow
           Allow from all
       </Directory>


For more details, consult the ``mod_wsgi`` documentation at
http://code.google.com/p/modwsgi/ .


Paste .ini file configuration
=============================

Paste configuration is done in an ``.ini`` file.

Edit the ``blog.ini`` file that ``pyblosxom-cmd`` created for you.

The ``[server:main]`` section dictates how Paste is serving your
blog.  See the `Paste documentation`_ for more details on this
section.

.. _Paste documentation: http://pythonpaste.org/


The ``[app:main]`` section specifies the PyBlosxom WSGI application
function and the directory your ``config.py`` file is in.  A
sample is here::

    [app:main]
    paste.app_factory = Pyblosxom.pyblosxom:pyblosxom_app_factory
    configpydir = /home/joe/blog/

Additionally, you can override ``config.py`` values in your
``blog.ini``.  For example, this overrides the ``blog_title``
value::

    [app:main]
    paste.app_factory = Pyblosxom.pyblosxom:pyblosxom_app_factory
    configpydir = /home/joe/blog/

    # PyBlosxom config here
    blog_title = Joe's Blog

This is really handy for testing changes to your blog infrastructure.
