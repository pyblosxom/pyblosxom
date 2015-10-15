===========================================================
Deploying Pyblosxom with Gunicorn and Nginx on Ubuntu 14.04
===========================================================

Summary
=======

This page explains how to deploy your Pyblosxom blog on an
`Ubuntu <http://www.ubuntu.com/>`_ web server using
`Gunicorn <http://gunicorn.org/>`_ and `Nginx <http://nginx.org/>`_.

These instructions have been tested on Ubuntu 14.04, but should also work on
other versions of Ubuntu and on other Debian- and Ubuntu-based operating
systems.

.. seealso::

   If you just want to run your Pyblosxom blog locally for development or
   testing, see :doc:`/deploy_gunicorn`.

Dependencies
============

You need to install Pyblosxom and create a blog on the web server first.
See :doc:`/install`. The instructions on this page assume that you've created
your blog at ``/var/www/blog``, for example by running:

.. code-block:: bash

   pyblosxom-cmd create /var/www/blog

.. tip::

   You may need to give your user account write access to ``/var/www``:

   .. code-block:: bash

      sudo mkdir -p /var/www
      sudo chown `whoami` /var/www

You also need to install Gunicorn and Nginx. Just run this command in a
terminal:

.. code-block:: bash

   sudo apt-get install gunicorn nginx

Deployment
==========

Create a Gunicorn config file ``/etc/gunicorn.d/blog`` with the following
contents, to tell Ubuntu how to run your blog with Gunicorn automatically::

  CONFIG = {
      'working_dir': '/var/www/blog',
      'args': (
          'Pyblosxom.pyblosxom:PyblosxomWSGIApp',
      ),
  }

.. note::

   These ``/etc/gunicorn.d/`` config files and running Gunicorn using the
   service command are features of the Gunicorn Debian package, they won't work
   on non-Debian based Linux distributions.

Restart the Gunicorn service:

.. code-block:: bash

   sudo service gunicorn restart

At this point Gunicorn should be running your blog on port 8000. You can test
it by running ``curl localhost:8000``, which should print out the HTML code of
your blog's front page.

.. note::

   If you install a plugin or make a change to your config.py file, you'll
   need to restart Gunicorn with ``sudo service gunicorn restart`` for the
   change to take effect.

To serve the blog to the outside Internet we need to hook Gunicorn up to Nginx.
Create the Nginx config file ``/etc/nginx/sites-available/blog`` with the
following contents::

  server {
    listen 80;
    server_name blog.example.com;
    access_log  /var/log/nginx/blog.log;

    location / {
      proxy_pass http://127.0.0.1:8000;
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }

Replace ``blog.example.com`` with your blog's domain name.

To enable the Nginx site create a sites-enabled symlink for it:

.. code-block:: bash

   sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled

You also need to remove the sites-enabled symlink for the default Nginx site:

.. code-block:: bash

   sudo rm /etc/nginx/sites-enabled/default

Restart the Nginx service, and test the new Nginx configuration file:

.. code-block:: bash

   sudo service nginx restart
   sudo nginx -t

Your Pyblosxom blog should now be running on port 80 at your server's domain
name or IP address.

Log files
=========

If Pyblosxom crashes you can look in the Nginx and Gunicorn log files for error
messages. There are located at ``/var/log/nginx/blog.log`` and
``/var/log/gunicorn/blog.log``.

Permissions
===========

All files in ``/var/www`` need to be readable by the ``www-data user``, and
directories need to be readable and executable by this user. Otherwise
Pyblosxom can crash or fail to see blog entries. An ``HTTP 500`` error from
Pyblosxom containing ``IOError: [Errno 13] Permission denied`` is a sure sign
that you have a file in ``/var/www/blog`` that ``www-data`` can't read.

One way to make sure that ``www-data`` can read all your blog's files is to
make the files and directories world-readable so that any user on the system
can read them, but only you can write them. In the output of ``ls -l`` the
permissions of a file should be ``-rw-r--r--``, and the permissions of a
directory shoud be ``drwxr-xr-x``.

To make sure that all files and directories that you create on the server have
these permissions, set your umask to 0022. Put the line:

.. code-block:: bash

   umask 0022

in your ``~/.profile``, ``~/.bashrc``, or other shell configuration file.

.. note::

   If you create files on your local machine and then move them to the server,
   or if you create files on the server using an editor running locally that is
   capable of editing remote files, you may need to make sure that your umask
   on your local machine is 0022 as well.

Static files
============

To make static files such as image, CSS and JavaScript files available to your
blog you can setup a second site on the same web server but at a different
domain or subdomin to host them.

Create the Nginx config file ``/etc/nginx/sites-available/static`` with these
contents::

  server {
    listen 80;
    server_name static.example.com;
    root /var/www/static;
    expires 1d;  # How long should static files be cached for.
  }

Replace ``static.example.com`` with the domain name for your static files site.

Create the directory on the server where the static files will go:

.. code-block:: bash

   mkdir /var/www/static

Enable the site by creating a ``sites-enabled`` symlink for it and restarting
Nginx:

.. code-block:: bash

   sudo ln -s /etc/nginx/sites-available/static /etc/nginx/sites-enabled
   sudo service nginx restart

Now if you put, say, an image file at ``/var/www/static/image.jpeg`` then it'll
be available to web browsers at http://static.example.com/image.jpeg. To use
this image in one of your blog posts, you might put an ``img`` tag like this
in the entry file:

.. code-block:: html

   <img src="http://static.example.com/image.jpeg" />

.. note::

   As with your blog's files, all files in ``/var/www/static`` need to be
   readable by the ``www-data`` user.

.. tip::

   If your theme needs access to static files you can add a setting in your
   ``config.py`` file like this:

   .. code-block:: python

      py["static_url"] = "http://static.example.com/"

   Then you can link to static files in your flavour templates with code like:

   .. code-block:: html

      <link href="$(static_url)/mystyles.css" rel="stylesheet" type="text/css">

   This saves having to code the full URL to your static files site into your
   flavour templates.
