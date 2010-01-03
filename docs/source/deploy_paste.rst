==============================
Deploying PyBlosxom with Paste
==============================

Summary
=======

PyBlosxom 1.4 and later supports Paste.  This document covers
installing and using PyBlosxom with Paste.

This installation assumes you have some understanding of Python Paste.
If this doesn't sound like you, then you can read up on Paste on
the `Paste web-site`_.

.. _Paste web-site: http://pythonpaste.org/


Dependencies
============

You will need:

* Pyblosxom 1.4 or later
* Python Paste which can be found at http://pythonpaste.org/

Additionally, if you're using an earlier version of Python than
Python 2.5, then you'll also need:

* wsgiref library from http://svn.eby-sarna.com/wsgiref/


Deployment
==========

Create a new blog by doing::

    pyblosxom-cmd create ./blog

Then do::

    cd ./blog/
    paster serve blog.ini

The ``paster`` script will print the URL for your blog on the command
line and your blog is now available on your local machine to your
local machine.


Configuration
=============

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
