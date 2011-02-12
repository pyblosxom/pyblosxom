What's new in 1.2
=================

Pertinent to users
------------------

1. We added a ``blog_email`` item to config.py and changed
   ``blog_author`` to just the author's name.  Examples:

      py["blog_email"] = "joe@blah.com"
      py["blog_author"] = "Joe Man"

2. We no longer adjust blog_title from what you set in ``config.py``.
   Now we have a ``blog_title_with_path`` variable which is in the
   data dict which is the ``blog_title`` with the path information.
   People who want the title of their blog to be the title and not
   include the path should use ``$blog_title``.  Folks who want the
   old behavior where the path was appended to the title should use
   ``$blog_title_with_path`` .

3. We now support WSGI, mod_python, and Twisted in addition to CGI.

4. Upped our Python requirement to Python 2.2.  If you have an earlier
   version than that, you won't be able to use PyBlosxom 1.2.

5. Changed ``defaultFlavour`` to ``default_flavour``.  This property
   allows you to specify the flavour to use by default if the URI
   doesn't specify one.  It default to ``html``.

6. We moved the main PyBlosxom site to
   http://pyblosxom.sourceforge.net/ .  There's a "powered by
   pyblosxom" image at
   http://pyblosxom.sourceforge.net/images/pb_pyblosxom.gif

   You should adjust your templates accordingly.


Pertinent to developers
-----------------------

1. We now have a Request and a Response object.  See API documentation
   for more details.

2. Don't use ``os.environ`` directly---use the http dict.  For
   example, this is bad::

      path_info = os.environ["HTTP_PATHINFO"]

   This is what you should be doing::

      http = request.getHttp()
      path_info = http["HTTP_PATHINFO"]

   If you use os.environ directly, it's likely your plugin won't work
   with non-CGI installations of PyBlosxom.

3. We added __iter__, read, readline, readlines, seek, and tell to the
   Request object.  All of them access the input stream.  You should
   not use sys.stdin directly.

   Usage::

      data = request.read()
      data_part = request.read(1024)
      one_line = request.readline()
      lines = request.readlines()

4. The output stream should be accessed through the PyBlosxom Response
   object.  The following methods are implemented in the Response
   object: __iter__, close, flush, read, readline, readlines, seek,
   tell, write, writelines, setStatus, and addHeader.  You should not
   use sys.stdout directly. See the API for more details.

   Usage::

      response = request.getResponse()
      response.addHeader('Status', '200 Ok')
      response.addHeader('Content-type', 'text/html')
      response.write("Hello World")
      response.writelines(["list", "of", "data"])

5. Instead of doing::

      form = request.getHttp()["form"]

   you can now do::

      form = request.getForm()

6. Plugins should not be importing the config module and looking at
   the ``py`` dict directly.  You should instead use the Request
   getConfiguration() method to get the config py dict.


