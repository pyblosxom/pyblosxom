========
Comments
========

This chapter briefly walks you through installing the comments,
trackback, pingback, and CommentAPI plugins.

FIXME - September 27th, 2009 - This needs to be updated. Srsly.


Summary
=======

PyBlosxom does not come with comments functionality built-in.  There are 
several ways you can add comments functionality to your blog.  This chapter
talks about those.


Disqus
======

Disqus is a comments platform web service that allows you to add comments to
your blog.

Pros:

* it's easy to install
* it handles spam for you
* supports notifications and replies

Cons:

* it's a web-service that you have no control over
* it might be difficult to move your comments over to a new system

If this is interesting to you, `sign up for a Disqus account`_.

.. _sign up for a Disqus account: http://disqus.com/


Writing your own comments plugin
================================

PyBlosxom allows for plugins allowing you to write a plugin to add comments
to your website.  This isn't for the feint of heart--there are a lot of bits
to think about.

Pros:

* you're in complete control over how comments work on your site

Cons:

* not for the feint of heart


Comments plugin
===============

There's a comments plugin that many PyBlosxom users use and which is sort
of supported, but needs a lot of work.

Pros:

* it's entirely in your control
* you can extend and modify it to meet your needs
* a lot of PyBlosxom users use it

Cons:

* many people find it difficult to install
* it's missing common comment system features like replies, threads, ...
* you have to implement and maintain your own anti-spam measures
* it hasn't been well maintained in the last couple of years

The comments plugin comes in the ``.tar.gz`` file alongside PyBlosxom as
of PyBlosxom 1.5.  Prior to that, you can get the latest stable version 
of the comments plugin from the `contributed plugins pack`_. Alternatively, 
you can get the latest version `from Git`_, which is even more recent but 
may be broken.  Caveat hacker!

.. _contributed plugins pack: http://pyblosxom.bluesock.org/download/
.. _from Git: http://gitorious.org/pyblosxom/pyblosxom/trees/master/plugins/comments

.. Note::

   The comments plugin also has a `README file`_ that has more
   information on installing comments, traceback, pingback, and the
   comment API.

.. _README file: http://gitorious.org/pyblosxom/pyblosxom/blobs/master/plugins/comments/README


Installing the comments plugin
------------------------------

Requirements:

1. A directory the web-server has writable permissions to.
2. Time and patience.


After making sure you have the requirements, do the following:

1. Copy ``plugins/comments/plugins/comments.py`` to your
   plugins directory.  Then add ``"comments"`` to the ``load_plugins``
   property in your ``config.py`` file.

2. Comments are stored in a directory tree which will parallel the
   data directory tree.  The comments themselves are stored as XML
   files named ``entryname-datetime.suffix``.  For example::

      video_audio_podcast_enhancements_in_firefox_3-1244176234.0.cmt

   The comment system allows you to specify the directory where the comment 
   directory tree will stored, and the suffix used for comment files.  You 
   need to make sure that this directory is writable by PyBlosxom however
   you have it installed.

   Set ``comment_dir`` to the directory (in your data directory) where
   you want the comments to be stored.  The default value is a
   directory named ``comments`` in your data directory.

   Set ``comment_ext`` to the change comment file extension.  The
   default file extension is ``cmt``.

3. Copy the flavour files from the ``plugins/comments/flavours``
   directory to the appropriate places alongside your flavour files.

   ``comment-story`` template is used to format a single entry that has 
   comments.

   ``comment`` template is used to format a single comment/trackback/pingback.

   ``comment-form`` template provides the form used to enter new comments.

4. Edit the ``comment-story``, ``comment``, and ``comment-form``
   templates if you need to.  Variables that are available are:

   Available in the ``story`` and ``comment-story`` templates:

   
   =============   ========================================================
   Template variables from comments.py available in story and comment-story
   ------------------------------------------------------------------------
   variable name   description
   =============   ========================================================
   num_comments    contains an integer count of the number of comments
                   associated withthis entry
   =============   ========================================================


   Available in the ``comment`` template:

   ============================   ===============================================================
   Template variables from comments.py
   ----------------------------------------------------------------------------------------------
   variable name                  description
   ============================   ===============================================================
   cmt_title                      the title of the comment

   cmt_description                the content of the comment or excerpt of the trackback/pingback

   cmt_link                       the pingback link referring to this entry

   cmt_author                     the author of the comment or trackback

   cmt_optionally_linked_author   the author, wrapped in an &lt;a href&gt; tag to 
                                  ``$cmt_link`` *if* it was provided

   cmt_pubDate                    the date and time of the comment/trackback/pingback

   cmt_source                     the source of the trackback
   ============================   ===============================================================


Email notification
------------------

The comment system can notify you via e-mail when new
comments/trackbacks/pingbacks are posted.  There are two ways to
configure this feature.  The first is to have email notifications sent
through your MTA via SMTP and the second is to have email
notifications sent through your MTA via a local command.

If you want to enable this feature, add the following properties to
your ``config.py`` file::

    py['comment_smtp_server'] - your SMTP server

OR::

    py['comment_mta_cmd']     - alternatively, the path to your MTA

AND THEN::

    py['comment_smtp_from']   - the address sending the notification
    py['comment_smtp_to']     - the address receiving the notification

For example, this sends email through your MTA via SMTP connecting to
localhost::

    py['comment_smtp_server'] = "localhost"
    py['comment_smtp_from']   = "joe@joe.com"
    py['comment_smtp_to']     = "joe@joe.com"

This sends email through your MTA via the command ``/usr/bin/mail``::

    py['comment_mta_cmd']     = "/usr/bin/mail"
    py['comment_smtp_from']   = "joe@joe.com"
    py['comment_smtp_to']     = "joe@joe.com"


Writing comments plugin templates
---------------------------------

This "diagram" shows which templates are responsible for what for
rendering a single entry::

    <div class="news">           <- story.html
    <h2>$title</h2>               |
    <div class="content">         |
    ...                           |
    </div>                        |
    links                         |
    </div>                       <-
    <div class="comments">       <- comment-story.html
    <div class="comment">        <- comment.html
    Posted by $blah at $blah      |
    $blah                         |
    </div>                       <-
    <div class="comment">        <- comment.html
    Posted by $blah at $blah      |
    $blah                         |
    </div>                       <-
    <div class="commentform">    <- comment-form.html
    form stuff here.              |
    </div>                        |
    </div>                       <-



AJAX commenting
---------------

Comment previewing and posting can optionally use `AJAX`_, as opposed
to full HTTP POST requests. This avoids a full-size roundtrip and
re-render, so commenting feels faster and more lightweight.

.. _AJAX: http://en.wikipedia.org/wiki/Ajax_(programming)

AJAX commenting degrades gracefully in older browsers. If the user's
browser doesn't support JavaScript or XmlHttpRequest, or if the user
has turned JavaScript off, comment posting and preview will use normal
HTTP POST.

**Enabling**

To enable AJAX commenting in your pyblosxom installation, just copy
``comments.js`` to your plugin directory and add the following
JavaScript to your ``comment-form`` template. (It's already included
in the ``comment-form.html`` template that comes with the comments
plugin.)

First, add a ``comment-anchor`` tag to the beginning of the template::

    <p id="comment-anchor" />

Add an ``onsubmit`` handler to the ``form`` tag::

    <form method="post" action="$base_url/$file_path#comment-anchor"
          name="comments_form" id="comments_form" onsubmit="return false;">

If you run pyblosxom inside `cgiwrap`_, remove ``#comment-anchor``
from the URL in the action attribute, since it confuses cgiwrap. (If
AJAX comment previewing and posting don't work, try removing
``#comment-anchor`` first. Your hosting provider may be using cgiwrap
without your knowledge. )

.. _cgiwrap: http://cgiwrap.sourceforge.net/

Next, add ``onclick`` handlers to the button ``input`` tags::

    <input value="Preview" name="preview" type="button" id="preview"
           onclick="send_comment('preview');" />
    <input value="Submit" name="submit" type="button" id="post"
           onclick="send_comment('post');" />

Finally, include this ``script`` tag somewhere after the ``form``
closing tag::

    <script type="text/javascript" src="/comments.js"></script>

The separate closing ``&lt;/script&gt;`` tag is necessary for
IE. Without it, IE won't actually run the code in ``comments.js``.

**Disabling**

To disable AJAX support, simply remove the JavaScript ``onsubmit`` and
``onclick`` handlers from your ``comment-form`` template. The comments
plugin will fall back to traditional HTTP POST commenting.



Dealing with comment spam
-------------------------

Expect it to happen.  Some folks get comment spam trickling in and
others get a torrential downpour.  It's best to deal with it from the
start.  It's also something you're going to have to deal with every
few months as spam techniques change and your needs change.

If this doesn't sound like something you want to actively maintain on
your blog, then you should encourage people to email comments to you
and rely upon your email spam-prevention.

As of contributed plugins pack 1.2 (March 27, 2005), the comments
plugin has a ``comment_reject`` callback which allows plugins to
examine each comment and reject it according to the plugin's
heuristics.  Because this is done in a callback, you can have multiple
comment rejection plugins that handle different situations.  A comment
won't be accepted until it has been looked at by each comment
rejection plugin you have running on your blog.

The recommended comment spam solution is ``akismetcomments`` and
``check_javascript``, in parallel.  ``akismetcomments`` uses
`Akismet`_, a centralized comment spam database and filter, and
``check_javascript`` simply checks that the client's user agent
supports Javascript.  (Spam bots almost never do.)

.. _Akismet: http://akismet.com/


**akismetcomments**

`Akismet`_ is a spam filter service developed and operated by
`Automattic`_, the people behind `WordPress`_.  Akismet maintains an
up-to-date blacklist, Bayesian filter, and other tools to determine
whether blog comments are spam or valid, ie "ham".

.. _WordPress: http://wordpress.com/
.. _Automattic: http://automattic.com/

The ``akismetcomments`` plugin passes every comment on your blog to
Akismet, which decides whether the comment is spam or ham.  If spam,
the comment is logged and discarded; if ham, it is accepted to your
blog.

To use ``akismetcomments``, you'll need to `sign up for a
Wordpress.com API key`_.

.. _sign up for a Wordpress.com API key: http://faq.wordpress.com/2005/10/19/api-key/

After you have your API key, copy ``akismetcomments.py`` and
``akismet.py`` to your plugin directory. Add an ``akismet_api_key``
config variable with to your API key to your ``config.py``.  Also,
make sure the ``baseurl`` config variable is defined::

    py['baseurl']        = "joe.com"
    py['akismet_api_key] = "ABQIAAAAg88GzFz..."

Finally, your blog's web server will need to be able to make outbound
HTTP connections on port 80 to ``api-key.rest.akismet.com``.  Some
hosting providers and firewalls may prevent this.  If you're not sure
about this, check with your webmaster or hosting provider.

``akismetcomments`` was written by `Benjamin 'Mako' Hill`_ and `Blake
Winton`_.

.. _Benjamin 'Mako' Hill: http://mako.cc/
.. _Blake Winton: http://bwinton.latte.ca/


**check_javascript**

Comment spam is usually sent by automated spam bots, which blindly
send HTTP POSTs to a large, static list of blog addresses. These spam
bots have very little in common with web browsers. In particular, they
rarely parse or render HTML, and even more rarely run Javascript.

Given this, Javascript can be an effective way to determine whether a
comment was submitted by a spam bot or a web browser.
``check_javascript`` uses a small piece of Javascript on the client
side to set the value of an ``input`` element in the comment form,
which it checks for on the server.

To use ``check_javascript``, first copy ``check_javascript.py`` to
your plugins directory.  Then include this hidden input element and
Javascript in your flavour's ``comment-form`` template::

    ...
    <input type="hidden" name="secretToken" id="secretTokenInput"
      value="pleaseDontSpam" />
    </form>

    <script type="text/javascript">
    // used by check_javascript.py. this is almost entirely backwards compatible,
    // back to 4.x browsers.
    document.getElementById("secretTokenInput").value = "$blog_title";
    </script>

It's included in the ``comment-form.html`` template in the
``contrib/plugins/comments/flavours/``, so if you use that template,
you're good to go.

``check_javascript`` was written by `Ryan Barrett`_.

.. _Ryan Barrett: http://snarfed.org/


**Rolling your own**


It's not hard to roll your own comment rejection plugin.  First figure
out what the heuristics involved would be.  Then write a plugin with a
``cb_comment_reject`` function in it.  In that function, look at the
data provided and reject the plugin if it seems appropriate to do so.
 
A basic template for writing a plugin to reject comments is as
follows.

Example: Template for plugin for rejecting comments

::

    FIXME - Documentation for what your plugin does and how to set it up
    goes here.

    FIXME - License information goes here.

    FIXME - Copyright information goes here.
    """
    __author__      = "FIXME - your name and email address"
    __version__     = "FIXME - version number and date released"
    __url__         = "FIXME - url where this plugin can be found"
    __description__ = "FIXME - one-line description of plugin"

    def verify_installation(request):
        # FIXME - code to verify that this plugin is installed correctly 
        # here.

        return 1


    def cb_comment_reject(args):
        req = args["request"]
        comment = args["comment"]

        blog_config = req.getConfiguration()

        # FIXME - code for figuring out whether this comment should
        # be rejected or not goes here.  If you want to reject the
        # comment, return 1.  Otherwise return 0.



Installing trackback
--------------------

If you want to support `trackbacks`_, copy
``plugins/comments/plugins/trackback.py`` to your plugins
directory.  Then add ``"trackback"`` to the ``load_plugins`` property
in your ``config.py`` file.

.. _trackbacks: http://www.sixapart.com/pronet/docs/trackback_spec

If you want trackbacks you need to advertise the trackback ping URL
for a particular entry.

You advertise a manual trackback ping link.  You can do this by
inserting the following HTML in story.html and comment-story.html
files::

    <a href="$base_url/trackback/$file_path" title="Trackback">TB</a> 

The ``/trackback`` URL prefix is configurable with the
``trackback_urltrigger`` config variable.

You can supply an embedded RDF description of the trackback ping::

    <!--
      <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
               xmlns:dc="http://purl.org/dc/elements/1.1/"
               xmlns:trackback="http://madskills.com/public/xml/rss/module/trackback/">
      <rdf:Description
        about="$base_url/$file_path"
        dc:title="$title"
        dc:identifier="$base_url/$file_path"
        trackback:ping="$base_url/trackback/$file_path"
     />
        </rdf:RDF>
    -->

This RDF should also be inserted in story.html and comment-story.html.
Since it is in an HTML comment, it doesn't matter where you put it.


Installing pingback
-------------------

If you want to support `pingbacks`_, copy
``plugins/comments/plugins/xmlrpc_pingback.py`` and
``xmlrpc_plugins/xmlrpc.py`` to your plugins directory.  Make
sure you have the ``base_url`` property defined in your ``config.py``
file.  Then add ``"xmlrpc_pingback"`` to the ``load_plugins`` property
in your ``config.py`` file.

.. _pingbacks: http://www.hixie.ch/specs/pingback/pingback

You'll need to advertise a pingback link in your ``head``
template. Add the following tag to the ``meta`` section::

    <link rel="pingback" href="http://joe.com/RPC" />

Replace ``joe.com`` with your ``baseurl``.
