====================
 Plugin: pyarchives 
====================

Summary
=======

Walks through your blog root figuring out all the available monthly
archives in your blogs.  It generates html with this information and
stores it in the ``$(archivelinks)`` variable which you can use in
your head and foot templates.


Install
=======

To install this plugin:

1. Add ``Pyblosxom.plugins.pyarchives`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Configure using the following configuration variables.

``archive_template``

    Let's you change the format of the output for an archive link.

    For example::

        py['archive_template'] = ('<li><a href="%(base_url)s/%(Y)s/%(b)s">'
                                  '%(m)s/%(y)s</a></li>')

    This displays the archives as list items, with a month number,
    then a slash, then the year number.

    The formatting variables available in the ``archive_template``
    are::

        b         'Jun'
        m         '6'
        Y         '1978'
        y         '78'

    These work the same as ``time.strftime`` in python.

    Additionally, you can use variables from config and data.

    .. Note::

       The syntax used here is the Python string formatting
       syntax---not the PyBlosxom template rendering syntax!


Usage
=====

Add ``$(archivelinks)`` to your head and/or foot templates.