.. _deploy-apache-mod-wsgi:

==============================================
 Deploying Pyblosxom with Apache and mod_wsgi
==============================================

Summary
=======

This walks through install Pyblosxom as an WSGI application on an
Apache web server with mod_wsgi installed.

If you find any issues, please let us know.

If you can help with the documentation efforts, please let us know.


Dependencies
============

* Apache
* mod_wsgi
* administrative priveliges to the server


Deployment
==========

1. Make sure mod_wsgi is installed correctly and working.

2. Create a blog---see the instructions for the blog directories,
   ``config.py`` setup and other bits of **Setting up a blog** in
   ``install_cgi``.

3. Create a ``pyblosxom.wsgi`` script that looks something like this:

   .. code-block:: python
      :linenos:

      # This is the pyblosxom.wsgi script that powers the _______
      # blog.

      import sys

      def add_to_path(d):
         if d not in sys.path:
            sys.path.insert(0, d)

      # call add_to_path with the directory that your config.py lives in.
      add_to_path("/home/joe/blog")

      # if you have Pyblosxom installed in a directory and NOT as a
      # Python library, then call add_to_path with the directory that
      # Pyblosxom lives in.  For example, if I untar'd
      # pyblosxom-1.5.tar.gz into /home/joe/, then add like this:
      # add_to_path("/home/joe/pyblosxom-1.5/")

      import Pyblosxom.pyblosxom
      application = Pyblosxom.pyblosxom.PyblosxomWSGIApp()

4. In the Apache conf file, add:

   ::

       WSGIScriptAlias /myblog /path/to/something.wsgi

       <Directory /path/to>
           Order deny,allow
           Allow from all
       </Directory>

   Change ``/myblog`` to the url path you want your blog to live at.

   Change ``/path/to/something.wsgi`` to be the absolute path to the
   .wsgi file set up in step 3.

   Change ``/path/to`` to the directory of the .wsgi file.

5. Restart the Apache web server.


.. Note::

   Any time you make changes to Pyblosxom (update, add plugins, change
   configuration), you'll have to restart Apache.
