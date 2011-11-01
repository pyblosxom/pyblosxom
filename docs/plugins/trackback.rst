
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

===================================
 trackback - Trackback support.... 
===================================

Summary
=======

This plugin allows pyblosxom to process trackback
http://www.sixapart.com/pronet/docs/trackback_spec pings.


Install
=======

Requires the ``comments`` plugin.  Though you don't need to have
comments enabled on your blog in order for trackbacks to work.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.trackback`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Add this to your ``config.py`` file::

       py['trackback_urltrigger'] = "/trackback"

   These web forms are useful for testing.  You can use them to send
   trackback pings with arbitrary content to the URL of your choice:

   * http://kalsey.com/tools/trackback/
   * http://www.reedmaniac.com/scripts/trackback_form.php

3. Now you need to advertise the trackback ping link.  Add this to your
   ``story`` template::

       <a href="$(base_url)/trackback/$(file_path)" title="Trackback">TB</a>

4. You can supply an embedded RDF description of the trackback ping, too.
   Add this to your ``story`` or ``comment-story`` template::

       <!--
       <rdf:RDF
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:trackback="http://madskills.com/public/xml/rss/module/trackback/">
       <rdf:Description
            about="$(base_url)/$(file_path)"
            dc:title="$(title)"
            dc:identifier="$(base_url)/$(file_path)"
            trackback:ping="$(base_url)/trackback/$(file_path)"
       />
       </rdf:RDF>
       -->


License
=======

Plugin is distributed under license: MIT
