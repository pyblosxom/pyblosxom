=================================
Deploying Pyblosxom with Gunicorn
=================================

Summary
=======

If you want to run your Pyblosxom blog locally for development or testing you
can run it in a terminal using `Gunicorn <http://gunicorn.org/>`_.

.. seealso::

   If you want to deploy Pyblosxom with Gunicorn on a web server for a
   production website, see :doc:`/deploy_gunicorn_nginx`.

Dependencies
============

You need to install Pyblosxom and create a blog first. See :doc:`/install`.

You also need to install Gunicorn. If you're running Debian or Ubuntu then just
run this command in a terminal:

.. code-block:: bash

   sudo apt-get install gunicorn

If you're on a different operating system, see the
`Gunicorn <http://gunicorn.org/>`_ website for install instructions.

Deployment
==========

To run your Pyblosxom blog with Gunicorn, simply run this command in a
terminal:

.. code-block:: bash

   gunicorn --log-file - --pythonpath ~/blog Pyblosxom.pyblosxom:PyblosxomWSGIApp

Replace ``~/blog`` with the path to your blog's directory.

Open http://127.0.0.1:8000/ in a web browser to see your blog, it's that easy!

The ``--log-file -`` makes Gunicorn print any errors from Pyblosxom to the
terminal.
