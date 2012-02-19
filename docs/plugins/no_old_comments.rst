
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

==========================================================
 no_old_comments - Prevent comments on entries older t... 
==========================================================

Summary
=======

This plugin implements the ``comment_reject`` callback of the comments
plugin.

If someone tries to comment on an entry that's older than 28 days, the
comment is rejected.


Install
=======

Requires the ``comments`` plugin.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.no_old_comments`` to the ``load_plugins``
   list in your ``config.py`` file.


Revisions
=========

1.0 - August 5th 2006: First released.


License
=======

Plugin is distributed under license: Public Domain
