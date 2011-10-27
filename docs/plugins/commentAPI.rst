====================
 Plugin: commentAPI 
====================

Summary
=======

CommentAPI provides support for Joe Gregario's CommentAPI
http://wellformedweb.org/story/9 .


Setup
=====

To use it, place it your plugins directory and make sure that you
define ``py['commentAPI_urltrigger']``, which is the URI to be used
for talking to the commentAPI.  Be sure that you have comments.py
installed

You must also add the commentAPI tags to your RSS 2.0 feed.  The best
way to do this is to add an XML namespace declaration to the rss
element::

    xmlns:wfw="http://wellformedweb.org/CommentAPI"
    

Then inside your RSS items you need to add a wfw:comment element::

    <wfw:comment>$base_url/###commentAPI###/$file_path</wfw:comment>
    
    where ``commentAPI`` is the value of ``commentAPI_urltrigger``


For example::

    py['commentAPI_urltrigger'] = "/commentAPI"