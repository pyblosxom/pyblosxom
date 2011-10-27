=========================
 Plugin: akismetcomments 
=========================

Summary
=======

Run comments and trackbacks through Akismet (http://akismet.com/) to
see whether to reject them or not.


Setup
=====

To use this plugin, you must also install ``akismet.py`` in your
python path (in the PyBlosxom plugin directory is fine).  You can get
it at http://www.voidspace.org.uk/python/modules.shtml#akismet .

Additionally, you will need to get a Wordpress.com API key.  You can
find more information from
http://faq.wordpress.com/2005/10/19/api-key/ .

Then, use this key to put put the following line into your config.py
file::

   py['akismet_api_key'] = 'MYKEYID'

If a comment is rejected, a message explaining this will saved in a
variable. You can place this into your template using the standard
``$(comment_message)`` variable.


History
=======

This plugin merges the work done on the ``akismetComments.py`` plugin
by Blake Winton with the the ``akismet.py`` plugin by Benjamin Mako
Hill.