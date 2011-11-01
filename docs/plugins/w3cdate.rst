
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

==================================================
 w3cdate - Adds a 'w3cdate' variable which is ... 
==================================================

Summary
=======

Adds a ``$(w3cdate)`` variable to the head and foot templates which has
the mtime of the first entry in the entrylist being displayed (this is
often the youngest/most-recent entry).


Install
=======

.. Note::

   If you have pyxml installed, then this will work better than if you don't.
   If you don't have it installed, it uses home-brew code to compute the
   w3cdate.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.w3cdate`` to the beginning of the
   ``load_plugins`` list of your ``config.py`` file.

2. Add the ``$(w3cdate)`` variable to the place you need it in your head
   and/or foot templates.


Thanks
======

Thanks to Matej Cepl for the hacked iso8601 code that doesn't require
PyXML.


License
=======

Plugin is distributed under license: MIT
