=================
 Plugin: w3cdate 
=================

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

1. Add ``Pyblosxom.plugins.w3cdate`` to the beginning of the
   ``load_plugins`` list of your ``config.py`` file.

2. Add the ``$(w3cdate)`` variable to the place you need it in your head
   and/or foot templates.


Thanks
======

Thanks to Matej Cepl for the hacked iso8601 code that doesn't require
PyXML.