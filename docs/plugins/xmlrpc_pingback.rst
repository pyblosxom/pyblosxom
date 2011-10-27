=========================
 Plugin: xmlrpc_pingback 
=========================

Summary
=======

This module contains an XML-RPC extension to support pingback
http://www.hixie.ch/specs/pingback/pingback pings.


Setup
=====

You must have the comments plugin installed as well, although you
don't need to enable comments on your blog in order for trackbacks to
work.

You must add a pingback ``<link>`` element to your HTML for
auto-discovery. For example, if your site is located at
http://foo.com/bar, your header HTML should contain this in its ``<meta>``
section::

   <link rel="pingback" href="http://foo.com/bar/RPC" />

Note that the URL must be absolute.  If your ``xmlrpc_urltrigger``
config variable is set to something other than RPC, modify the
``<link>`` element accordingly.

This test blog, maintained by Ian Hickson, is useful for testing. You
can post to it, linking to a post on your site, and it will send a
pingback.

* http://www.dummy-blog.org/