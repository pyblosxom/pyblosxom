===================
 Plugin: trackback 
===================

Summary
=======

This plugin allows pyblosxom to process trackback
http://www.sixapart.com/pronet/docs/trackback_spec pings.


Setup
=====

You must have the comments plugin installed as well, although you
don't need to enable comments on your blog in order for trackbacks to
work.

Add this to your ``config.py`` file::

    py['trackback_urltrigger'] = "/trackback"

These web forms are useful for testing.  You can use them to send
trackback pings with arbitrary content to the URL of your choice:

* http://kalsey.com/tools/trackback/
* http://www.reedmaniac.com/scripts/trackback_form.php

For more detailed installation, read the README file that comes with
the comments plugins.