
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

==========================================================
 pyfilenamemtime - Allows you to codify the mtime in t... 
==========================================================

Summary
=======

Allows you to specify the mtime for a file in the file name.

If a filename contains a timestamp in the form of
``YYYY-MM-DD-hh-mm``, change the mtime to be the timestamp instead of
the one kept by the filesystem.

For example, a valid filename would be ``foo-2002-04-01-00-00.txt``
for April fools day on the year 2002.  It is also possible to use
timestamps in the form of ``YYYY-MM-DD``.

http://www.probo.com/timr/blog/


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.pyfilenamemtime`` to the ``load_plugins``
   list of your ``config.py`` file.

2. Use date stamps in your entry filenames.


License
=======

Plugin is distributed under license: MIT
