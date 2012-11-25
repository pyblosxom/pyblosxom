#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
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
   http://pyblosxom.github.com/ or in the tarball under
   docs/_static/plugins/comments/.


This plugin has related files like flavour templates, javascript file,
shell scripts and such.  All of these files can be gotten from `here
<../_static/plugins/comments/>`_


Flavour templates
=================

The comments plugin requires at least the ``comment-story``,
``comment``, and ``comment-form`` templates.

The way the comments plugin assembles flavour files is like this::

    comment-story
    comment (zero or more)
    comment-form

Thus if you want to have your entire comment section in a div
container, you'd start the div container at the top of
``comment-story`` and end it at the bottom of ``comment-form``.


comment-story
-------------

The ``comment-story`` template comes at the beginning of the comment
section before the comments and the comment form.


Variables available:

   $num_comments - Contains an integer count of the number of comments
                   associated with this entry


.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.github.com/ or in the tarball under
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
   http://pyblosxom.github.com/ or in the tarball under
   docs/_static/plugins/comments/.


Link to file: `comment <../_static/plugins/comments/comment>`_

.. literalinclude:: ../_static/plugins/comments/comment
   :language: html


comment-form
------------

The ``comment-form`` comes at the end of all the comments.  It has the
comment form used to enter new comments.

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.github.com/ or in the tarball under
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

.. Note::

   Comment preview is implemented by default---all the bits listed
   below are in the comment-form and comment-preview templates.

   This documentation is here in case you had an older version of the
   comments plugin or you want to know what to remove to remove
   comment preview.


If you would like comment previews, you need to do 2 things.

1. Add a preview button to the ``comment-form`` template like this::

      <input name="preview" type="submit" value="Preview" />

   You may change the contents of the value attribute, but the name of
   the input must be "preview".  I put it next to the "Submit" button.

2. Still in your ``comment-form.html`` template, you need to use the
   comment values to fill in the values of your input fields like so::

      <input name="author" type="text" value="$(cmt_author)">
      <input name="email" type="text" value="$(cmt_email)">
      <input name="url" type="text" value="$(cmt_link)">
      <textarea name="body">$(cmt_description)</textarea>

   If there is no preview available, these variables will be stripped
   from the text and cause no problem.

3. Create a ``comment-preview`` template.  This can be a copy of your
   ``comment`` template if you like with some additional text along the
   lines of **"This is a preview!"**

   All of the available variables from the ``comment`` template are
   available in the ``comment-preview`` template.

.. only:: text

   You can find the comment-story file in the docs at
   http://pyblosxom.github.com/ or in the tarball under
   docs/_static/plugins/comments/.


comment-preview
---------------

Link to file: `comment-preview <../_static/plugins/comments/comment-preview>`_

.. literalinclude:: ../_static/plugins/comments/comment-preview
   :language: html


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

"""

__author__ = "Ted Leung, et al"
__email__ = "pyblosxom-devel at sourceforge dot net"
__version__ = "2011-12-17"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Adds comments to a blog entry."
__category__ = "comments"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


import cgi
import glob
import re
import time
import cPickle
import os
import codecs
import sys
import subprocess
import traceback

from email.MIMEText import MIMEText
from xml.sax.saxutils import escape
from Pyblosxom import tools
from Pyblosxom.renderers import blosxom
from Pyblosxom.tools import pwrap, pwrap_error

LATEST_PICKLE_FILE = 'LATEST.cmt'

def cb_start(args):
    request = args["request"]
    config = request.get_configuration()

    if not 'comment_dir' in config:
        config['comment_dir'] = os.path.join(config['datadir'],'comments')
    if not 'comment_ext' in config:
        config['comment_ext'] = 'cmt'
    if not 'comment_draft_ext' in config:
        config['comment_draft_ext'] = config['comment_ext']
    if not 'comment_nofollow' in config:
        config['comment_nofollow'] = 0

def verify_installation(request):
    config = request.get_configuration()

    retval = True

    if 'comment_dir' in config and not os.path.isdir(config['comment_dir']):
        pwrap_error(
           'The "comment_dir" property in the config file must refer '
           'to a directory')
        retval = False

    smtp_keys_defined = []
    smtp_keys=[
        'comment_smtp_server',
        'comment_smtp_from',
        'comment_smtp_to']
    for k in smtp_keys:
        if k in config:
            smtp_keys_defined.append(k)

    if smtp_keys_defined:
        for i in smtp_keys:
            if i not in smtp_keys_defined:
                pwrap_error("Missing comment SMTP property: '%s'" % i)
                retval = False

    optional_keys = [
        'comment_dir',
        'comment_ext',
        'comment_draft_ext',
        'comment_nofollow',
        'comment_disable_after_x_days']
    for i in optional_keys:
        if not i in config:
            pwrap("missing optional property: '%s'" % i)

    if 'comment_disable_after_x_days' in config:
        if ((not isinstance(config['comment_disable_after_x_days'], int) or
             config['comment_disable_after_x_days'] <= 0)):
            pwrap("comment_disable_after_x_days has a non-positive "
                  "integer value.")

    return retval

def createhtmlmail(html, headers):
    """
    Create a mime-message that will render HTML in popular
    MUAs, text in better ones

    Based on: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/67083
    """
    import MimeWriter
    import mimetools
    import cStringIO

    out = cStringIO.StringIO() # output buffer for our message
    htmlin = cStringIO.StringIO(html)

    text = re.sub('<.*?>', '', html)
    txtin = cStringIO.StringIO(text)

    # FIXME MimeWriter is deprecated as of Python 2.6
    writer = MimeWriter.MimeWriter(out)
    for header,value in headers:
        writer.addheader(header, value)
    writer.addheader("MIME-Version", "1.0")
    writer.startmultipartbody("alternative")
    writer.flushheaders()

    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'us-ascii')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()

    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()

    writer.lastpart()
    msg = out.getvalue()
    out.close()

    return msg

def read_comments(entry, config):
    """
    @param: a file entry
    @type: dict

    @returns: a list of comment dicts
    """
    filelist = glob.glob(cmt_expr(entry, config))
    comments = []
    for f in filelist:
        comments += read_file(f, config)
    comments = [(cmt['cmt_time'], cmt) for cmt in comments]
    comments.sort()
    return [c[1] for c in comments]

def cmt_expr(entry, config):
    """
    Return a string containing the regular expression for comment entries

    @param: a file entry
    @type: dict
    @returns: a string with the directory path for the comment

    @param: configuratioin dictionary
    @type: dict

    @returns: a string containing the regular expression for comment entries
    """
    cmt_dir = os.path.join(config['comment_dir'], entry['absolute_path'])
    cmt_expr = os.path.join(cmt_dir, entry['fn'] + '-*.' + config['comment_ext'])
    return cmt_expr

def read_file(filename, config):
    """
    Read comment(s) from filename

    @param filename: filename containing comment(s)
    @type filename: string

    @param config: the pyblosxom configuration settings
    @type config: dictionary

    @returns: a list of comment dicts
    """
    from xml.sax import make_parser
    from xml.sax.handler import feature_namespaces, ContentHandler

    class cmt_handler(ContentHandler):
        def __init__(self, cmts):
            self.cmts = cmts
        def startElement(self, name, atts):
            if name == 'item':
                self.cur_cmt = {}
            self._data = ""
        def endElement(self, name):
            self.cur_cmt['cmt_' + name] = self._data
            if name == 'item':
                self.cmts.append(self.cur_cmt)
        def characters(self, content):
            self._data += content

    cmts = []

    try:
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        handler = cmt_handler(cmts)
        parser.setContentHandler(handler)
        parser.parse(filename)

    # FIXME - bare except here--bad!
    except:
        logger = tools.get_logger()
        logger.error("bad comment file: %s\nerror was: %s" %
                     (filename, traceback.format_exception(*sys.exc_info())))
        return []

    for cmt in cmts:
        # time.time()
        cmt['cmt_time'] = float(cmt['cmt_pubDate'])
        # pretty time
        cmt['cmt_pubDate'] = time.ctime(float(cmt['cmt_pubDate']))
        cmt['cmt_w3cdate'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                           time.gmtime(cmt['cmt_time']))
        cmt['cmt_date'] = time.strftime('%a %d %b %Y',
                                        time.gmtime(cmt['cmt_time']))
        if cmt['cmt_link']:
            link = add_dont_follow('<a href="%s">%s</a>' %
                                   (cmt['cmt_link'], cmt['cmt_author']),
                                   config)
            cmt['cmt_optionally_linked_author'] = link
        else:
            cmt['cmt_optionally_linked_author'] = cmt['cmt_author']

    return cmts

def write_comment(request, config, data, comment, encoding):
    """
    Write a comment

    @param config: dict containing pyblosxom config info
    @type  config: dict

    @param data: dict containing entry info
    @type  data: dict

    @param comment: dict containing comment info
    @type  comment: dict

    @return: The success or failure of creating the comment.
    @rtype: string
    """
    entry_list = data.get("entry_list", [])
    if not entry_list:
        return "No such entry exists."

    entry = data['entry_list'][0]
    cdir = os.path.join(config['comment_dir'], entry['absolute_path'])
    cdir = os.path.normpath(cdir)
    if not os.path.isdir(cdir):
        os.makedirs(cdir)

    cfn = os.path.join(cdir, entry['fn'] + "-" + comment['pubDate'] + "." + config['comment_draft_ext'])

    def make_xml_field(name, field):
        return "<" + name + ">" + cgi.escape(field.get(name, "")) + "</"+name+">\n";

    filedata = '<?xml version="1.0" encoding="%s"?>\n' % encoding
    filedata += "<item>\n"
    for key in comment:
        filedata += make_xml_field(key, comment)
    filedata += "</item>\n"

    try :
        cfile = codecs.open(cfn, "w", encoding)
    except IOError:
        logger = tools.get_logger()
        logger.error("couldn't open comment file '%s' for writing" % cfn)
        return "Internal error: Your comment could not be saved."

    cfile.write(filedata)
    cfile.close()

    # write latest pickle
    latest = None
    latest_filename = os.path.join(config['comment_dir'], LATEST_PICKLE_FILE)
    try:
        latest = open(latest_filename, "w")
    except IOError:
        logger = tools.get_logger()
        logger.error("couldn't open latest comment pickle for writing")
        return "Couldn't open latest comment pickle for writing."
    else:
        mod_time = float(comment['pubDate'])

    try:
        cPickle.dump(mod_time, latest)
        latest.close()
    except IOError:
        if latest:
            latest.close()

        logger = tools.get_logger()
        logger.error("comment may not have been saved to pickle file.")
        return "Internal error: Your comment may not have been saved."

    if ((('comment_mta_cmd' in config
          or 'comment_smtp_server' in config)
         and 'comment_smtp_to' in config)):
        # FIXME - removed grabbing send_email's return error message
        # so there's no way to know if email is getting sent or not.
        send_email(config, entry, comment, cdir, cfn)

    # figure out if the comment was submitted as a draft
    if config["comment_ext"] != config["comment_draft_ext"]:
        return "Comment was submitted for approval.  Thanks!"

    return "Comment submitted.  Thanks!"

def send_email(config, entry, comment, comment_dir, comment_filename):
    """Send an email to the blog owner on a new comment

    @param config: configuration as parsed by Pyblosxom
    @type config: dictionary

    @param entry: a file entry
    @type config: dictionary

    @param comment: comment as generated by read_comments
    @type comment: dictionary

    @param comment_dir: the comment directory
    @type comment_dir: string

    @param comment_filename: file name of current comment
    @type comment_filename: string
    """
    import smtplib
    # import the formatdate function which is in a different
    # place in Python 2.3 and up.
    try:
        from email.Utils import formatdate
    except ImportError:
        from rfc822 import formatdate
    from socket import gethostbyaddr

    author = escape_smtp_commands(clean_author(comment['author']))
    description = escape_smtp_commands(comment['description'])
    ipaddress = escape_smtp_commands(comment.get('ipaddress', '?'))

    if 'comment_smtp_from' in config:
        email = config['comment_smtp_from']
    else:
        email = escape_smtp_commands(clean_author(comment['email']))

    try:
        curl = "%s/%s" % (config['base_url'],
                          tools.urlencode_text(entry['file_path']))
        comment_dir = os.path.join(config['comment_dir'], entry['absolute_path'])

        # create the message
        message = []
        message.append("Name: %s" % author)
        if 'email' in comment:
            message.append("Email: %s" % comment['email'])
        if 'link' in comment:
            message.append("URL: %s" % comment['link'])
        try:
            host_name = gethostbyaddr(ipaddress)[0]
            message.append("Hostname: %s (%s)" % (host_name, ipaddress))
        # FIXME - bare except here--bad!
        except:
            message.append("IP: %s" % ipaddress)
        message.append("Entry URL: %s" % curl)
        message.append("Comment location: %s" % comment_filename)
        message.append("\n\n%s" % description)

        if 'comment_mta_cmd' in config:
            # set the message headers
            message.insert(0, "")
            message.insert(0, "Subject: comment on %s" % curl)
            message.insert(0, "Date: %s" % formatdate(float(comment['pubDate'])))
            message.insert(0, "To: %s" % config["comment_smtp_to"])
            message.insert(0, "From: %s" % email)

            body = '\n'.join(message).encode('utf-8')

            argv = [config['comment_mta_cmd'],
                    '-s',
                    '"comment on %s"' % curl,
                    config['comment_smtp_to']]

            process = subprocess.Popen(
                argv, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.stdin.write(body)
            process.stdin.close()
            process.wait()
            stdout = process.stdout.read()
            stderr = process.stderr.read()
            tools.get_logger().debug('Ran MTA command: ' + ' '.join(argv))
            tools.get_logger().debug('Received stdout: ' + stdout)
            tools.get_logger().debug('Received stderr: ' + stderr)
            # the except clause below will catch this
            assert stderr == '', stderr

        else:
            assert 'comment_smtp_server' in config
            server = smtplib.SMTP(config['comment_smtp_server'])
            mimemsg = MIMEText("\n".join(message).encode("utf-8"), 'plain', 'utf-8')

            # set the message headers
            mimemsg["From"] = email
            mimemsg["To"] = config["comment_smtp_to"]
            mimemsg["Date"] = formatdate(float(comment["pubDate"]))
            mimemsg["Subject"] = ("comment on %s" % curl)

            # send the message via smtp
            server.sendmail(from_addr=email,
                            to_addrs=config['comment_smtp_to'],
                            msg=mimemsg.as_string())
            server.quit()

    except Exception, e:
        tools.get_logger().error("error sending email: %s" %
                                traceback.format_exception(*sys.exc_info()))

def check_comments_disabled(config, entry):
    disabled_after_x_days = config.get("comment_disable_after_x_days", 0)
    if not isinstance(disabled_after_x_days, int):
        # FIXME - log an error?
        return False

    if disabled_after_x_days <= 0:
        # FIXME - log an error?
        return False

    if not entry.has_key('mtime'):
        return False

    entry_age = (time.time() - entry['mtime']) / (60 * 60 * 24)
    if entry_age > disabled_after_x_days:
        return True
    return False

def clean_author(s):
    """
    Guard against blasterattacko style attacks that embedd SMTP commands in
    author field.

    If author field is more than one line, reduce to one line

    @param the string to be checked
    @type string

    @returns the sanitized string
    """
    return s.splitlines()[0]

def escape_smtp_commands(s):
    """
    Guard against blasterattacko style attacks that embed SMTP commands by
    using an HTML span to make the command syntactically invalid to SMTP but
    renderable by HTML

    @param the string to be checked
    @type string

    @returns the sanitized string
    """
    def repl_fn(mo):
        return '<span>'+mo.group(0)+'</span>'
    s = re.sub('([Tt]o:.*)',repl_fn,s)
    s = re.sub('([Ff]rom:.*)',repl_fn,s)
    s = re.sub('([Ss]ubject:.*)',repl_fn,s)
    return s

def sanitize(body):
    """
    This code shamelessly lifted from Sam Ruby's mombo/post.py
    """
    body=re.sub(r'\s+$','',body)
    body=re.sub('\r\n?','\n', body)

    # naked urls become hypertext links
    body=re.sub('(^|[\\s.:;?\\-\\]<])' +
                '(http://[-\\w;/?:@&=+$.!~*\'()%,#]+[\\w/])' +
                '(?=$|[\\s.:;?\\-\\[\\]>])',
                '\\1<a href="\\2">\\2</a>',body)

    # html characters used in text become escaped
    body = escape(body)

    # passthru <a href>, <em>, <i>, <b>, <blockquote>, <br/>, <p>,
    # <abbr>, <acronym>, <big>, <cite>, <code>, <dfn>, <kbd>, <pre>, <small>
    # <strong>, <sub>, <sup>, <tt>, <var>, <ul>, <ol>, <li>
    body = re.sub('&lt;a href="([^"]*)"&gt;([^&]*)&lt;/a&gt;',
                 '<a href="\\1">\\2</a>', body)
    body = re.sub('&lt;a href=\'([^\']*)\'&gt;([^&]*)&lt;/a&gt;',
                '<a href="\\1">\\2</a>', body)
    body = re.sub('&lt;em&gt;([^&]*)&lt;/em&gt;', '<em>\\1</em>', body)
    body = re.sub('&lt;i&gt;([^&]*)&lt;/i&gt;', '<i>\\1</i>', body)
    body = re.sub('&lt;b&gt;([^&]*)&lt;/b&gt;', '<b>\\1</b>', body)
    body = re.sub('&lt;blockquote&gt;([^&]*)&lt;/blockquote&gt;',
                '<blockquote>\\1</blockquote>', body)
    body = re.sub('&lt;br\s*/?&gt;\n?', '\n', body)

    body = re.sub('&lt;abbr&gt;([^&]*)&lt;/abbr&gt;', '<abbr>\\1</abbr>', body)
    body = re.sub('&lt;acronym&gt;([^&]*)&lt;/acronym&gt;', '<acronym>\\1</acronym>', body)
    body = re.sub('&lt;big&gt;([^&]*)&lt;/big&gt;', '<big>\\1</big>', body)
    body = re.sub('&lt;cite&gt;([^&]*)&lt;/cite&gt;', '<cite>\\1</cite>', body)
    body = re.sub('&lt;code&gt;([^&]*)&lt;/code&gt;', '<code>\\1</code>', body)
    body = re.sub('&lt;dfn&gt;([^&]*)&lt;/dfn&gt;', '<dfn>\\1</dfn>', body)
    body = re.sub('&lt;kbd&gt;([^&]*)&lt;/kbd&gt;', '<kbd>\\1</kbd>', body)
    body = re.sub('&lt;pre&gt;([^&]*)&lt;/pre&gt;', '<pre>\\1</pre>', body)
    body = re.sub('&lt;small&gt;([^&]*)&lt;/small&gt;', '<small>\\1</small>', body)
    body = re.sub('&lt;strong&gt;([^&]*)&lt;/strong&gt;', '<strong>\\1</strong>', body)
    body = re.sub('&lt;sub&gt;([^&]*)&lt;/sub&gt;', '<sub>\\1</sub>', body)
    body = re.sub('&lt;sup&gt;([^&]*)&lt;/sup&gt;', '<sup>\\1</sup>', body)
    body = re.sub('&lt;tt&gt;([^&]*)&lt;/tt&gt;', '<tt>\\1</tt>', body)
    body = re.sub('&lt;var&gt;([^&]*)&lt;/var&gt;', '<var>\\1</var>', body)

    # handle lists
    body = re.sub('&lt;ul&gt;\s*', '<ul>', body)
    body = re.sub('&lt;/ul&gt;\s*', '</ul>', body)
    body = re.sub('&lt;ol&gt;\s*', '<ol>', body)
    body = re.sub('&lt;/ol&gt;\s*', '</ol>', body)
    body = re.sub('&lt;li&gt;([^&]*)&lt;/li&gt;\s*', '<li>\\1</li>', body)
    body = re.sub('&lt;li&gt;', '<li>', body)

    body = re.sub('&lt;/?p&gt;', '\n\n', body).strip()

    # wiki like support: _em_, *b*, [url title]
    body = re.sub(r'\b_(\w.*?)_\b', r'<em>\1</em>', body)
    body = re.sub(r'\*(\w.*?)\*', r'<b>\1</b>', body)
    body = re.sub(r'\[(\w+:\S+\.gif) (.*?)\]', r'<img src="\1" alt="\2" />', body)
    body = re.sub(r'\[(\w+:\S+\.jpg) (.*?)\]', r'<img src="\1" alt="\2" />', body)
    body = re.sub(r'\[(\w+:\S+\.png) (.*?)\]', r'<img src="\1" alt="\2" />', body)
    body = re.sub(r'\[(\w+:\S+) (.*?)\]', r'<a href="\1">\2</a>', body).strip()

    # unordered lists: consecutive lines starting with spaces and an asterisk
    chunk = re.compile(r'^( *\*.*(?:\n *\*.*)+)',re.M).split(body)
    for i in range(1, len(chunk), 2):
        html, stack = '', ['']
        for indent, line in re.findall(r'( +)\* +(.*)', chunk[i]) + [('','')]:
            if indent > stack[-1]:
                stack, html = stack + [indent], html + '<ul>\r'
            while indent<stack[-1]:
                stack, html = stack[:-1], html + '</ul>\r'
            if line:
                html += '<li>' + line + '</li>\r'
            chunk[i] = html

    # white space
    chunk = re.split('\n\n+', ''.join(chunk))
    body = re.sub('\n', '<br />\n', body)
    body = re.compile('<p>(<ul>.*?</ul>)\r</p>?', re.M).sub(r'\1', body)
    body = re.compile('<p>(<blockquote>.*?</blockquote>)</p>?', re.M).sub(r'\1', body)
    body = re.sub('\r', '\n', body)
    body = re.sub('  +', '&nbsp; ', body)

    return body

def dont_follow(mo):
    return '<a rel="nofollow" ' + mo.group(1) + '>'

def add_dont_follow(s, config):
    url_pat_str = '<a ([^>]+)>'
    url_pat = re.compile(url_pat_str)
    if config['comment_nofollow'] == 1:
        return url_pat.sub(dont_follow, s)
    else:
        return s

def cb_prepare(args):
    """
    Handle comment related HTTP POST's.

    @param request: pyblosxom request object
    @type request: a Pyblosxom request object
    """
    request = args["request"]
    form = request.get_http()['form']
    config = request.get_configuration()
    data = request.get_data()
    pyhttp = request.get_http()

    # first we check to see if we're going to print out comments
    # the default is not to show comments
    data['display_comment_default'] = False

    # check to see if they have "showcomments=yes" in the querystring
    qstr = pyhttp.get('QUERY_STRING', None)
    if qstr != None:
        parsed_qs = cgi.parse_qs(qstr)
        if 'showcomments' in parsed_qs:
            if parsed_qs['showcomments'][0] == 'yes':
                data['display_comment_default'] = True

    # check to see if the bl_type is "file"
    if "bl_type" in data and data["bl_type"] == "file":
        data["bl_type_file"] = "yes"
        data['display_comment_default'] = True

    # second, we check to see if they're posting a comment and we
    # need to write the comment to disk.
    posting = (('ajax' in form and form['ajax'].value == 'post') or
               not "preview" in form)
    if (("title" in form and "author" in form
         and "body" in form and posting)):

        entry = data.get("entry_list", [])
        if len(entry) == 0:
            data["rejected"] = True
            data["comment_message"] = "No such entry exists."
            return
        entry = entry[0]

        if check_comments_disabled(config, entry):
            data["rejected"] = True
            data["comment_message"] = "Comments for that entry are disabled."
            return

        encoding = config.get('blog_encoding', 'utf-8')
        decode_form(form, encoding)

        body = form['body'].value
        author = form['author'].value
        title = form['title'].value
        url = ('url' in form and [form['url'].value] or [''])[0]

        # sanitize incoming data
        body = sanitize(body)
        author = sanitize(author)
        title = sanitize(title)

        # it doesn't make sense to add nofollow to link here, but we should
        # escape it. If you don't like the link escaping, I'm not attached
        # to it.
        cmt_time = time.time()
        w3cdate = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(cmt_time))
        date = time.strftime('%a %d %b %Y', time.gmtime(cmt_time))
        cdict = {'title': title,
                 'author': author,
                 'pubDate': str(cmt_time),
                 'w3cdate': w3cdate,
                 'date': date,
                 'link': massage_link(url),
                 'source': '',
                 'description': add_dont_follow(body, config)}

        keys = form.keys()
        keys = [k for k in keys
                if k not in ["title", "url", "author", "body", "description"]]
        for k in keys:
            cdict[k] = form[k].value

        if 'email' in form:
            cdict['email'] = form['email'].value

        cdict['ipaddress'] = pyhttp.get('REMOTE_ADDR', '')

        # record the comment's timestamp, so we can extract it and send it
        # back alone, without the rest of the page, if the request was ajax.
        data['cmt_time'] = float(cdict['pubDate'])

        argdict = {"request": request, "comment": cdict}
        reject = tools.run_callback("comment_reject",
                                    argdict,
                                    donefunc=lambda x:x != 0)
        if (((isinstance(reject, tuple) or isinstance(reject, list))
             and len(reject) == 2)):
            reject_code, reject_message = reject
        else:
            reject_code, reject_message = reject, "Comment rejected."
        if reject_code == 1:
            data["comment_message"] = reject_message
            data["rejected"] = True
        else:
            data["comment_message"] = write_comment(request, config, data, \
                                                   cdict, encoding)

class AjaxRenderer(blosxom.Renderer):
    """ The renderer used when responding to AJAX requests to preview
    and post comments. Renders *only* the comment and comment-preview
    divs.
    """
    def __init__(self, request, data):
        out = request.get_configuration().get('stdoutput', sys.stdout)
        blosxom.Renderer.__init__(self, request, out)
        self._ajax_type = request.get_http()['form']['ajax'].value
        self._data = data

    def _should_output(self, entry, template_name):
        """ Return whether we should output this template, depending on the
        type of ajax request we're responding to.
        """
        if self._ajax_type == 'preview' and template_name == 'comment-preview':
            return True
        elif self._ajax_type == 'post' and template_name == 'comment-form':
            return True
        else:
            return False

    def render_template(self, entry, template_name, override=0):
        if self._should_output(entry, template_name):
            return blosxom.Renderer.render_template(
                self, entry, template_name, override)
        else: return ""

    def _output_flavour(self, entry, template_name):
        if self._should_output(entry, template_name):
            blosxom.Renderer._output_flavour(self, entry, template_name)

def cb_renderer(args):
    request = args['request']
    config = request.get_configuration()
    http = request.get_http()
    form = http['form']

    # intercept ajax requests with our renderer
    if 'ajax' in form and http.get('REQUEST_METHOD', '') == 'POST':
        data = '&'.join(['%s=%s' % (arg.name, arg.value) for arg in form.list])
        tools.get_logger().info('AJAX request: %s' % data)
        return AjaxRenderer(request, request.get_data())

def cb_handle(args):
    request = args['request']
    config = request.get_configuration()

    # serve /comments.js for ajax comments
    if request.get_http()['PATH_INFO'] == '/comments.js':
        response = request.get_response()
        response.add_header('Content-Type', 'text/javascript')

        # look for it in each of the plugin_dirs
        for dir in config['plugin_dirs']:
            comments_js = os.path.join(dir, 'comments.js')
            if os.path.isfile(comments_js):
                f = open(comments_js, 'r')
                response.write(f.read())
                f.close()
                return True

def massage_link(linkstring):
    """Don't allow html in the link string. Prepend http:// if there isn't
    already a protocol."""
    for c in "<>'\"":
        linkstring = linkstring.replace(c, '')
    if linkstring and linkstring.find(':') == -1:
        linkstring = 'http://' + linkstring
    return linkstring

def decode_form(d, blog_encoding):
    """Attempt to decode the POST data with a few likely character encodings.

    If the Content-type header in the HTTP request includes a charset, try
    that first. Then, try the encoding specified in the pybloscom config file.
    if Those fail, try iso-8859-1, utf-8, and ascii.
    """
    encodings = [blog_encoding, 'iso-8859-1', 'utf-8', 'ascii']
    charset = get_content_type_charset()
    if charset:
        encodings = [charset] + encodings

    for key in d.keys():
        for e in encodings:
            try:
                d[key].value = d[key].value.decode(e)
                break
            # FIXME - bare except--bad!
            except:
                continue

def get_content_type_charset():
    """Extract and return the charset part of the HTTP Content-Type
    header.

    Returns None if the Content-Type header doesn't specify a charset.
    """
    content_type = os.environ.get('CONTENT_TYPE', '')
    match = re.match('.+; charset=([^;]+)', content_type)
    if match:
        return match.group(1)
    else:
        return None

def cb_head(args):
    renderer = args['renderer']
    template = args['template']

    if 'comment-head' in renderer.flavour and len(renderer.getContent()) == 1:
        args['template'] = renderer.flavour['comment-head']

        # expand all of entry vars for expansion
        entry = args['entry']
        single_entry = entry['entry_list'][0]
        single_entry['title'] # force lazy evaluation
        entry.update(single_entry)
        args['entry'] = entry
    return template

def cb_story(args):
    """For single entry requests, when commenting is enabled and the
    flavour has a comment-story template, append its contents to the
    story template's.
    """
    renderer = args['renderer']
    entry = args['entry']
    template = args['template']
    request = args["request"]
    data = request.get_data()
    config = request.get_configuration()
    # FIXME - entry is currently broken and doesn't support "in"
    if entry.has_key('absolute_path') and not entry.has_key('nocomments'):
        entry['comments'] = read_comments(entry, config)
        entry['num_comments'] = len(entry['comments'])
        if ((len(renderer.get_content()) == 1
             and 'comment-story' in renderer.flavour
             and data['display_comment_default'])):
            template = renderer.flavour.get('comment-story', '')
            args['template'] = args['template'] + template

    return template

def build_preview_comment(form, entry, config):
    """Build a prevew comment by brute force

    @param form: cgi form object (or compatible)
    @type form: Dictionary of objects with a .value propery

    @param entry: pyblosxom entry object
    @type entry: pyblosxom entry object

    @param config: the pyblosxom configuration settings
    @type config: dictionary

    @return: the comment HTML, a string
    """
    c = {}
    # required fields
    try:
        c['cmt_time'] = float(time.time())
        c['cmt_author'] = form['author'].value
        c['cmt_title'] = form['title'].value
        c['cmt_item'] = sanitize(form['body'].value)
        cmt_time = time.time()
        c['cmt_pubDate'] = time.ctime(cmt_time)
        c['cmt_w3cdate'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                         (time.gmtime(cmt_time)))
        c['cmt_date'] = time.strftime('%a %d %b %Y',
                                      time.gmtime(cmt_time))
        c['cmt_description'] = sanitize(form['body'].value)

        # optional fields
        c['cmt_optionally_linked_author'] = c['cmt_author']
        if 'url' in form:
            c['cmt_link'] = massage_link(form['url'].value)
            if c['cmt_link']:
                link = add_dont_follow('<a href="%s">%s</a>' %
                                       (c['cmt_link'], c['cmt_author']),
                                       config)
                c['cmt_optionally_linked_author'] = link

        if 'openid_url' in form:
            c['cmt_openid_url'] = massage_link(form['openid_url'].value)

        if 'email' in form:
            c['cmt_email'] = form['email'].value

    except KeyError, e:
        c['cmt_error'] = 'Missing value: %s' % e

    entry.update(c)
    return c

def cb_story_end(args):
    renderer = args['renderer']
    entry = args['entry']
    template = args['template']
    request = args["request"]
    data = request.get_data()
    form = request.get_http()['form']
    config = request.get_configuration()
    # FIXME - entry is currently broken and doesn't support "in"
    if ((entry.has_key('absolute_path')
         and len(renderer.get_content()) == 1
         and 'comment-story' in renderer.flavour
         and not entry.has_key('nocomments')
         and data['display_comment_default'])):
        output = []
        if entry.has_key('comments'):
            comment_entry_base = dict(entry)
            del comment_entry_base['comments']
            for comment in entry['comments']:
                comment_entry = dict(comment_entry_base)
                comment_entry.update(comment)
                output.append(renderer.render_template(comment_entry, 'comment'))
        if (('preview' in form
             and 'comment-preview' in renderer.flavour)):
            com = build_preview_comment(form, entry, config)
            output.append(renderer.render_template(com, 'comment-preview'))
        elif 'rejected' in data:
            rejected = build_preview_comment(form, entry, config)
            msg = '<span class="error">%s</span>' % data["comment_message"]
            rejected['cmt_description'] = msg
            rejected['cmt_description_escaped'] = escape(msg)
            output.append(renderer.render_template(rejected, 'comment'))
        if not check_comments_disabled(config, entry):
            output.append(renderer.render_template(entry, 'comment-form'))
        args['template'] = template + "".join(output)

    return template
