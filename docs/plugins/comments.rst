==================
 Plugin: comments 
==================

Summary
=======

Comments support plugin.


Setup
=====

This module supports the following config parameters (they are not
required):

``comment_dir``

   the directory we're going to store all our comments in.  this
   defaults to datadir + "comments".

``comment_ext``

   the file extension used to denote a comment file.  this defaults
   to "cmt".

``comment_draft_ext``

   the file extension used for new comments that have not been
   manually approved by you.  this defaults to comment_ext
   (i.e. there is no draft stage)

``comment_smtp_server``

   the smtp server to send comments notifications through.

``comment_mta_cmd``

   alternatively, a command line to invoke your MTA (e.g.
   sendmail) to send comment notifications through.

``comment_smtp_from``

   the email address comment notifications will be from. If you're
   using SMTP, this should be an email address accepted by your
   SMTP server. If you omit this, the from address will be the
   e-mail address as input in the comment form.

``comment_smtp_to``

   the email address to send comment notifications to.

``comment_nofollow``

   set this to 1 to add rel="nofollow" attributes to links in the
   description -- these attributes are embedded in the stored
   representation.

``comment_disable_after_x_days``

   set this to a positive integer and users won't be able to leave
   comments on entries older than x days.

Comments are stored one or more per file in a parallel hierarchy to
the datadir hierarchy.  The filename of the comment is the filename of
the blog entry, plus the creation time of the comment as a float, plus
the comment extension.

This plugin always writes each comment to its own file, but as an
optimization, it supports files that contain multiple comments.  You
can use ``compact_comments.sh`` in this directory to compact comments
into a single file per entry.

Comments now follow the ``blog_encoding`` variable specified in
``config.py``.  If you don't include a ``blog_encoding`` variable,
this will default to iso-8859-1.

Comments will be shown for a given page if one of the following is
true:

1. the page has only one blog entry on it and the request is for a
   specific blog entry as opposed to a category with only one entry
   in it

2. if "showcomments=yes" is in the querystring then comments will
   be shown


Flavour templates
=================

The comments plugin requires at least the ``comment-story``,
``comment``, and ``comment-form`` templates.  The ``comment-preview``
template is optional.

The way the comments plugin assembles flavour files is like this::

    comment-story
    comment-preview (optional)
    comment (zero or more)
    comment-form

Thus if you want to have your entire comment section in a div
container, you'd start the div container at the top of comment-story
and end it at the bottom of comment-form.


comment-story
-------------

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment-story <../_static/plugins/comments/comment-story>`_

.. literalinclude:: ../_static/plugins/comments/comment-story
   :language: html


comment
-------

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment <../_static/plugins/comments/comment>`_

.. literalinclude:: ../_static/plugins/comments/comment
   :language: html


comment-preview
---------------

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment-preview <../_static/plugins/comments/comment-preview>`_

.. literalinclude:: ../_static/plugins/comments/comment-preview
   :language: html


comment-form
------------

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment-form <../_static/plugins/comments/comment-form>`_

.. literalinclude:: ../_static/plugins/comments/comment-form
   :language: html


Implementing comment preview
============================

If you would like comment previews, you need to do 2 things.

1. Add a preview button to comment-form.html like this::

      <input name="preview" type="submit" value="Preview" />

   You may change the contents of the value attribute, but the name of
   the input must be "preview".

2. Still in your ``comment-form.html`` template, you need to use the
   comment values to fill in the values of your input fields like so::

      <input name="author" type="text" value="$(cmt_author)">
      <input name="email" type="text" value="$(cmt_email)">
      <input name="url" type="text" value="$(cmt_link)">
      <textarea name="body">$(cmt_description)</textarea>

   If there is no preview available, these variables will be stripped
   from the text and cause no problem.

3. Copy ``comment.html`` to a template called
   ``comment-preview.html``. All of the available variables from the
   comment template are available for this template.


AJAX support
============

Comment previewing and posting can optionally use AJAX, as opposed to
full HTTP POST requests. This avoids a full-size roundtrip and
re-render, so commenting feels faster and more lightweight.

AJAX commenting degrades gracefully in older browsers.  If JavaScript
is disabled or not supported in the user's browser, or if it doesn't
support XmlHttpRequest, comment posting and preview will use normal
HTTP POST.  This will also happen if comment plugins that use
alternative protocols are detected, like ``comments_openid.py``.

AJAX comment support requires a few elements in the ``comment-form``
flavour template. These elements are included in default
``comment-form.html`` template that comes with this plugin.

Specifically, the comment-anchor tag must be the first thing in the
template::

   <p id="comment-anchor" />

Also, the form needs some JavaScript.  Add an onsubmit handler to the
form tag::

   <form method="post" action="$(base_url)/$(file_path)#comment-anchor"
      name="comments_form" id="comments_form" onsubmit="return false;">

If you run pyblosxom inside cgiwrap, you'll probably need to remove
``#comment-anchor`` from the URL in the action attribute.  They're
incompatible.

(Your host may even be using cgiwrap without your knowledge. If AJAX comment
previewing and posting don't work, try removing ``#comment-anchor``.)

Next, add onclick handlers to the button input tags::

  <input value="Preview" name="preview" type="button" id="preview"
       onclick="send_comment('preview');" />
  <input value="Submit" name="submit" type="button" id="post"
       onclick="send_comment('post');" />

Finally, include this script tag somewhere after the ``</form>`` closing tag::

   <script type="text/javascript" src="/comments.js"></script>

(Note the separate closing ``</script>`` tag!  It's for IE; without
it, IE won't actually run the code in ``comments.js``.)


nofollow support
================

This implements Google's nofollow support for links in the body of the
comment.  If you display the link of the comment poster in your HTML
template then you must add the ``rel="nofollow"`` attribute to your
template as well


Note to developers who are writing plugins that create comments
===============================================================

Each entry has to have the following properties in order to work with
comments:

1. ``absolute_path`` - the category of the entry.

   Example: "dev/pyblosxom" or ""

2. ``fn`` - the filename of the entry without the file extension and without
   the directory.

   Example: "staticrendering"

3. ``file_path`` - the absolute_path plus the fn.

   Example: "dev/pyblosxom/staticrendering"

Also, if you don't want comments for an entry, add::

   #nocomments 1

to the entry or set ``nocomments`` to ``1`` in the properties of the
entry.


Where to find additional material
=================================

There is a ``README`` file that comes with the contributed plugins
pack in ``plugins/comments/`` which has more information on installing
the comments plugin.

Additionally, there is a chapter in the PyBlosxom manual that covers
installing and configuring the comments plugin.  The manual is on the
PyBlosxom website: http://pyblosxom.bluesock.org/