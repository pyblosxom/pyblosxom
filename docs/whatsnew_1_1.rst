What's new in 1.1 (January 2005)
================================

Pertinent to users
------------------

1. We no longer include contributed plugins and flavours.  To find
   plugins and flavours, go to the PyBlosxom registry located at
   http://pyblosxom.sourceforge.net/ .

2. We changed how ``num_entries`` is handled internally.  If
   ``num_entries`` is set to 0, the blosxom default file handler will
   display all the entries.  If ``num_entries`` is set to a positive
   number, then the blosxom default file handler will display at most
   that many entries.


Pertinent to developers
-----------------------

1. Plugins that implement cb_filelist are now in charge of adjusting
   the number of entries to be displayed based on the ``num_entries``
   configuration variable.  This is no longer done in the renderer.

2. We added HTTP_COOKIE to the list of things that get added to the
   http dict in the Request object.
