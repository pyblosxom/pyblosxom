=========================
 Plugin: no_old_comments 
=========================

Summary
=======

This plugin implements the ``comment_reject`` callback of the comments
plugin.

If someone tries to comment on an entry that's older than 28 days, the
comment is rejected.


Install
=======

Requires the ``comments`` plugin.

1. Add ``Pyblosxom.plugins.no_old_comments`` to the ``load_plugins``
   list in your ``config.py`` file.


Revisions
=========

1.0 - August 5th 2006: First released.