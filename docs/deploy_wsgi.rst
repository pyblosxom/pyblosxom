=============================
Deploying PyBlosxom with WSGI
=============================

Summary
=======

As of PyBlosxom 1.2, PyBlosxom has support for WSGI.

As of PyBlosxom 1.4, WSGI support has been folded into the main
codebase (as opposed to being a separate wsgi_app.py file).  But it's
broken until 1.4.2.

There are a bunch of ways to set up PyBlosxom with WSGI.  These
instructions aren't as mature as other instructions.

If you find any issues, please let us know.

If you can help with the documentation efforts, please let us know.


Dependencies
============

Either:

  * Python 2.5, OR

  * Python 2.4 with the wsgiref library installed:
    http://cheeseshop.python.org/pypi/wsgiref


Setup
=====

Setup depends on what you're using.

mod_wsgi
--------

If you're using mod_wsgi from http://code.google.com/p/modwsgi/ then
do the following:

1. Make sure mod_wsgi is installed correctly and working.

2. Either:

   2.1. Add a ``WSGIScriptAlias`` to your Apache configuration that
        points to ``pyblosxom.wsgi``, OR

   2.2. Verify that your ``WSGIScriptAlias`` points to a valid
        directory on your file system that stores WSGI scripts.

3. Create a blog---see the instructions for the blog directories,
   ``config.py`` setup and other bits of **Setting up a blog** in
   ``install_cgi``.

4. Create a ``pyblosxom.wsgi`` script that looks something like this::

      # This is the pyblosxom.wsgi script that powers the _______ blog.
      import sys

      def add_to_path(d):
         if d not in sys.path:
            sys.path.insert(0, d)

      # call add_to_path with the directory that your config.py lives in.
      add_to_path("/home/joe/blog")

      # if you have PyBlosxom installed in a directory and NOT as a Python
      # library, then call add_to_path with the directory that PyBlosxom
      # lives in.  For example, if I untar'd pyblosxom-1.5.tar.gz into
      # /home/joe/, then add like this:
      # add_to_path("/home/joe/pyblosxom-1.5/")

      import Pyblosxom.pyblosxom
      application = Pyblosxom.pyblosxom.PyBlosxomWSGIApp()



mod_python
----------

FIXME - need to add instructions here


other situations
----------------

FIXME - need to add instructions here
