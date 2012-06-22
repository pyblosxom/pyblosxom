.. _deploy-lighttpd-mod-fastcgi:

==============================================
 Deploying Pyblosxom with Lighttpd and fastcgi
==============================================

Summary
=======

This walks through install Pyblosxom as a FastCGI application on 
a Lighttpd web server with mod_fcgi installed.

If you find any issues, please let us know.

If you can help with the documentation efforts, please let us know.


Dependencies
============

* Lighttpd
* mod_fcgi
* python-flup
* administrative privileges to the server


Deployment
==========

1. Make sure mod_fcgi is installed correctly and working.

2. Create a blog---see the instructions for the blog directories,
   ``config.py`` setup and other bits of **Setting up a blog** in
   ``install_cgi``.

3. Create a ``pyblosxom.wsgi`` script that looks something like this:

   .. code-block:: python
      :linenos:

      #!/usr/bin/env python
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

      from flup.server.fcgi import WSGIServer
      WSGIServer(application).run()

   Don't forget to make it executable by Lighttpd. I did it like this:

   ::

      chown :www-data pyblosxom.wsgi
      chmod g+x pyblosxom.wsgi

   This way you change group ownership to the group that lighty belongs
   to and give all group members execution permission.

4. Create /etc/lighttpd/conf-available/90-myblog.conf with this content:

   ::

        server.modules += ( "mod_fastcgi" )

        $HTTP["host"] =~ "(^|\.*)yourhost\.com$" {

        #### fastcgi module
        ## read fastcgi.txt for more info
        # this line may help with finding what's wrong, check out errorlog file
        fastcgi.debug=1
        fastcgi.server = (
                "/myblog" => (
                "main" => (
                "host" => "127.0.0.1",
                "port" => 3033,
                "check-local" => "disable",
                "max-procs" => 1,
                "bin-path" => "/path/to/pyblosxom.wsgi"
           )
          )
         )

        }

   You must change ``yourhost.com`` to match your domain.

   Fascgi.debug line is useful for finding out why your app doesn't work.
   Error messages go to ``/var/log/lighttpd/errors.log`` unless configured
   otherwise. When it all works, set it to 0.

   Change ``/myblog`` to the url path you want your blog to live at.
   If you want it at root node (like http://yourhost.com/ ), set it to ``/``.

   Select any not used port number.

   Checkout what ``check-local`` and ``max-procs`` mean in `Lighttpd docs`_.

   Change ``/path/to/pyblosxom.wsgi`` to be the absolute path to the
   .wsgi file set up in step 3.

5. Now you can enable and disable this part of configuration with 
   ``lighttpd-enable-mod`` and ``lighttpd-disable-mod``, so now do:

   ::

        lighttpd-enable-mod myblog
        service lighttpd force-reload

.. Note::

   Any time you make changes to Pyblosxom (update, add plugins, change
   configuration), you'll have to force-reload configuration of Lighttpd.

.. _`Lighttpd docs`: http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ConfigurationOptions#mod_fastcgi-fastcgi
