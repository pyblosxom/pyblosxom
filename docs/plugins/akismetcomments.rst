
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

=====================================================
 akismetcomments - Rejects comments using akismet... 
=====================================================

Summary
=======

Run comments and trackbacks through `Akismet <http://akismet.com/>`_
to see whether to reject them or not.


Install
=======

Requires the ``comments`` plugin.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.akismetcomments`` to the ``load_plugins``
   list in your ``config.py`` file.

2. Install the ``akismet`` library.  You can get it at
   http://www.voidspace.org.uk/python/modules.shtml#akismet

3. Set up a Wordpress.com API key.  You can find more information from
   http://faq.wordpress.com/2005/10/19/api-key/ .

4. Use this key to put put the following line into your config.py
   file::

       py['akismet_api_key'] = 'MYKEYID'

5. Add ``$(comment_message)`` to the comment-form template if it isn't
   there already.

   When akismetcomments rejects a comment, it'll populate that
   variable with a message explaining what happened.


History
=======

This plugin merges the work done on the ``akismetComments.py`` plugin
by Blake Winton with the the ``akismet.py`` plugin by Benjamin Mako
Hill.


License
=======

Plugin is distributed under license: GPLv2
