
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

===============================================
 xmlrpc_pingback - XMLRPC pingback support.... 
===============================================

Summary
=======

This module contains an XML-RPC extension to support pingback
http://www.hixie.ch/specs/pingback/pingback pings.


Install
=======

Requires the ``comments`` plugin, but you don't have to enable
comments on your blog for pingbacks to work.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.xmlrpc_pingback`` to the ``load_plugins``
   list of your ``config.py`` file

2. Set the ``xmlrpc_trigger`` variable in your ``config.py`` file to a
   trigger for this plugin.  For example::

      py["xmlrpc_trigger"] = "RPC"

3. Add to the ``<head>`` section of your ``head`` template::

      <link rel="pingback" href="$(base_url)/RPC" />


This test blog, maintained by Ian Hickson, is useful for testing. You
can post to it, linking to a post on your site, and it will send a
pingback.

* http://www.dummy-blog.org/


License
=======

Plugin is distributed under license: MIT
