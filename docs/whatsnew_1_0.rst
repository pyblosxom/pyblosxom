What's new in 1.0 (May 2004)
============================

Pertinent to users
------------------

1. We ditched ``blosxom_custom_flavours``---you can remove it from your
   ``config.py`` file.

2. We added static rendering---see the howto in the PyBlosxom manual.

3. Rewrote comments to use the new handler system.  You should replace
   the comments, pingbacks, trackbacks, and other comments-oriented
   plugins with the new versions from ``contrib/plugins/comments/``.

4. pingbacks plugin is now ``xmlrpc_pingbacks.py`` .

5. Adjusted the default templates for HTML and RSS.  Removed all other
   default templates.  Look at the flavour_examples directory for
   flavour examples.

6. Added an ``ignore_properties`` property to ``config.py`` which
   allows you to specify which directories in your datadir should be
   ignored.  For example::

      py["ignore_directories"] = ["CVS", ".svn"]

7. Added a template variable ``pyblosxom_version`` which points to
   ``pyblosxom/Pyblosxom/pyblosxom.VERSION_DATE`` .

8. Fixed some code in pyarchives so it worked with Python 2.1.  Thanks
   to Wilhelm.

9. Fixed template retrieving code so that you can specify templates to
   use for a given category or parent categories.  Thanks to Nathan
   for fixing this.

10. We added a ``logdir`` property to config.  PyBlosxom (and plugins)
    will create logs in this directory so the directory has to have
    write access for whatever user the webserver uses to run the
    script.


Pertinent to developers and plugin developers
---------------------------------------------

1. Rewrote the startup for PyBlosxom request handling---we ditched the
   common_start function and picked up a common initialize function.

2. Unhardcoded where contrib and web files go when doing a multi-user
   installation using ``python setup.py install``.

3. Adjusted the comments plugin so that if a given entry has a
   ``nocomments`` property, then it won't get comments.

4. Moved the Request object into ``pyblosxom/Pyblosxom/pyblosxom.py``.

5. Fixed variable parsing so that if the variable value is a function
   that takes arguments, we pass the request in as the first argument.

6. Added VERSION, VERSION_DATE, and VERSION_SPLIT.  This allows you to
   verify that your plugin works with the version of PyBlosxom the
   user is using.
