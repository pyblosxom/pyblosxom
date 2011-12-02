
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

==============================================
 comments - Adds comments to a blog entry.... 
==============================================

Summary
=======

Adds comments to your blog.  Supports preview, AJAX posting, SMTP
notifications, plugins for rejecting comments (and thus reducing
spam), ...

Comments are stored in a directory that parallels the data directory.
The comments themselves are stored as XML files named
entryname-datetime.suffix.  The comment system allows you to specify
the directory where the comment directory tree will stored, and the
suffix used for comment files.  You need to make sure that this
directory is writable by whatever is running Pyblosxom.

Comments are stored one or more per file in a parallel hierarchy to
the datadir hierarchy.  The filename of the comment is the filename of
the blog entry, plus the creation time of the comment as a float, plus
the comment extension.

Comments now follow the ``blog_encoding`` variable specified in
``config.py``.  If you don't include a ``blog_encoding`` variable,
this will default to utf-8.

Comments will be shown for a given page if one of the following is
true:

1. the page has only one blog entry on it and the request is for a
   specific blog entry as opposed to a category with only one entry
   in it

2. if "showcomments=yes" is in the querystring then comments will
   be shown


.. Note::

   This comments plugin does not work with static rendering.  If you
   are using static rendering to build your blog, you won't be able to
   use this plugin.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.comments`` to the ``load_plugins`` list of
   your ``config.py`` file.

   Example::

       py["load_plugins"] = ["Pyblosxom.plugins.comments"]

2. Configure as documented below in the Configuration section.

3. Add templates to your html flavour as documented in the Flavour
   templates section.


Configuration
=============

1. Set ``py['comment_dir']`` to the directory (in your data directory)
   where you want the comments to be stored.  The default value is a
   directory named "comments" in your datadir.

2. (optional) The comment system can notify you via e-mail when new
   comments/trackbacks/pingbacks are posted.  If you want to enable
   this feature, create the following config.py entries:

      py['comment_smtp_from'] - the email address sending the notification
      py['comment_smtp_to']   - the email address receiving the notification

   If you want to use an SMTP server, then set::

      py['comment_smtp_server'] - your SMTP server hostname/ip address

   **OR** if you want to use a mail command, set::

      py['comment_mta_cmd']     - the path to your MTA, e.g. /usr/bin/mail

   Example 1::

      py['comment_smtp_from']   = "joe@joe.com"
      py['comment_smtp_to']     = "joe@joe.com"
      py['comment_smtp_server'] = "localhost"

   Example 2::

      py['comment_smtp_from']   = "joe@joe.com"
      py['comment_smtp_to']     = "joe@joe.com"
      py['comment_mta_cmd']     = "/usr/bin/mail"

3. (optional) Set ``py['comment_ext']`` to the change comment file
   extension.  The default file extension is "cmt".


This module supports the following config parameters (they are not
required):

``comment_dir``

   The directory we're going to store all our comments in.  This
   defaults to datadir + "comments".

   Example::

      py["comment_dir"] = "/home/joe/blog/comments/"

``comment_ext``

   The file extension used to denote a comment file.  This defaults
   to "cmt".

``comment_draft_ext``

   The file extension used for new comments that have not been
   manually approved by you.  This defaults to the value in
   ``comment_ext``---i.e. there is no draft stage.

``comment_smtp_server``

   The smtp server to send comments notifications through.

``comment_mta_cmd``

   Alternatively, a command line to invoke your MTA (e.g.  sendmail)
   to send comment notifications through.

``comment_smtp_from``

   The email address comment notifications will be from.  If you're
   using SMTP, this should be an email address accepted by your SMTP
   server.  If you omit this, the from address will be the e-mail
   address as input in the comment form.

``comment_smtp_to``

   The email address to send comment notifications to.

``comment_nofollow``

   Set this to 1 to add ``rel="nofollow"`` attributes to links in the
   description---these attributes are embedded in the stored
   representation.

``comment_disable_after_x_days``

   Set this to a positive integer and users won't be able to leave
   comments on entries older than x days.


Related files
=============

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


This plugin has related files like flavour templates, javascript file,
shell scripts and such.  All of these files can be gotten from `here
<../_static/plugins/comments/>`_


Flavour templates
=================

The comments plugin requires at least the ``comment-story``,
``comment``, and ``comment-form`` templates.  The ``comment-preview``
template is optional.

The way the comments plugin assembles flavour files is like this::

    comment-story
    comment (zero or more)
    comment-preview (optional)
    comment-form

Thus if you want to have your entire comment section in a div
container, you'd start the div container at the top of comment-story
and end it at the bottom of comment-form.


comment-story
-------------

The ``comment-story`` template comes at the beginning of the comment
section before the comments and the comment form.


Variables available:

   $num_comments - Contains an integer count of the number of comments
                   associated with this entry


.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment-story <../_static/plugins/comments/comment-story>`_

.. literalinclude:: ../_static/plugins/comments/comment-story
   :language: html


comment
-------

The ``comment`` template is used to format a single entry that has
comments.

Variables available::

   $cmt_title - the title of the comment
   $cmt_description - the content of the comment or excerpt of the
                      trackback/pingback
   $cmt_link - the pingback link referring to this entry
   $cmt_author - the author of the comment or trackback
   $cmt_optionally_linked_author - the author, wrapped in an <a href> tag
                                   to their link if one was provided
   $cmt_pubDate - the date and time of the comment/trackback/pingback
   $cmt_source - the source of the trackback


.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment <../_static/plugins/comments/comment>`_

.. literalinclude:: ../_static/plugins/comments/comment
   :language: html


comment-preview
---------------

The ``comment-preview`` template shows a comment that is being
previewed, but hasn't been posted to the blog, yet.

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment-preview <../_static/plugins/comments/comment-preview>`_

.. literalinclude:: ../_static/plugins/comments/comment-preview
   :language: html


comment-form
------------

The ``comment-form`` comes at the end of all the comments.  It has the
comment form used to enter new comments.

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.bluesock.org/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment-form <../_static/plugins/comments/comment-form>`_

.. literalinclude:: ../_static/plugins/comments/comment-form
   :language: html


Dealing with comment spam
=========================

You'll probably have comment spam.  There are a bunch of core plugins
that will help you reduce the comment spam that come with Pyblosxom as
well as ones that don't.

Best to check the core plugins first.


Compacting comments
===================

This plugin always writes each comment to its own file, but as an
optimization, it supports files that contain multiple comments.  You
can use ``compact_comments.sh`` to compact comments into a single file
per entry.

.. only:: text

   compact_comments.sh is located in docs/_static/plugins/comments/


You can find ``compact_comments.sh`` `here
<../_static/plugins/comments/>`_.


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

To add AJAX support, you need to make the following modifications to your
``comment-form`` template:

1. The comment-anchor tag must be the first thing in the
   ``comment-form`` template::

      <p id="comment-anchor" />

2. Change the ``<form...>`` tag to something like this::

      <form method="post" action="$(base_url)/$(file_path)#comment-anchor"
         name="comments_form" id="comments_form" onsubmit="return false;">

   .. Note::

      If you run pyblosxom inside cgiwrap, you'll probably need to
      remove ``#comment-anchor`` from the URL in the action attribute.
      They're incompatible.

      Your host may even be using cgiwrap without your knowledge. If
      AJAX comment previewing and posting don't work, try removing
      ``#comment-anchor``.

3. Add ``onclick`` handlers to the button input tags::

      <input value="Preview" name="preview" type="button" id="preview"
          onclick="send_comment('preview');" />
      <input value="Submit" name="submit" type="button" id="post"
          onclick="send_comment('post');" />

4. Copy ``comments.js`` file to a location on your server that's
   servable by your web server.

   You can find this file `here <../_static/plugins/comments/>`_.

   .. only:: text

      You can find comments.js in docs/_static/plugins/comments/.

5. Include this script tag somewhere after the ``</form>`` closing tag::

      <script type="text/javascript" src="/comments.js"></script>

   Set the url for ``comments.js`` to the url for where
   ``comments.js`` is located on your server from step 4.

   .. Note::

      Note the separate closing ``</script>`` tag!  It's for IE;
      without it, IE won't actually run the code in ``comments.js``.


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


License
=======

Plugin is distributed under license: MIT
