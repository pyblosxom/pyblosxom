#######################################################################
# Copyright (c) 2006 Ryan Barrett
# Copyright (c) 2011 Will Kahn-Greene
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#######################################################################

"""
Summary
=======

This plugin filters spam with a dash of JavaScript on the client side.
The JavaScript sets a hidden input field ``secretToken`` in the
comment form to the blog's title.  This plugin checks the
``secretToken`` URL parameter and rejects the comment if it's not set
correctly.

The benefit of JavaScript as an anti-spam technique is that it's very
successful.  It has extremely low false positive and false negative
rates, as compared to conventional techniques like CAPTCHAs, bayesian
filtering, and keyword detection.

Of course, JavaScript has its own drawbacks, primarily that it's not
supported in extremely old browsers, and that users can turn it off.
That's a very small minority of cases, though.  Its effectiveness as
an anti-spam technique usually make that tradeoff worthwhile.


Install
=======

Requires the ``comments`` plugin.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.check_javascript`` to the ``load_plugins``
   list in your ``config.py`` file.

2. Configure as documented below.


Configure
=========

1. Make sure you have ``blog_title`` set in your ``config.py``.

2. Add the following bits to your ``comment-form`` template inside
   the ``<form>`` tags::

      <input type="hidden" name="secretToken" id="secretTokenInput"
        value="pleaseDontSpam" />

      <script type="text/javascript">
      // used by check_javascript.py. this is almost entirely backwards
      // compatible, back to 4.x browsers.
      document.getElementById("secretTokenInput").value = "$(blog_title)";
      </script>

"""
__author__ = "Ryan Barrett"
__email__ = "pyblosxom at ryanb dot org"
__version__ = "2011-10-25"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Rejects comments using JavaScript"
__category__ = "comments"
__license__ = "GPLv2"
__registrytags__ = "1.4, 1.5, core"


from Pyblosxom import tools


def verify_installation(request):
    return True


def cb_comment_reject(args):
    request = args["request"]
    config = request.get_configuration()
    http = request.get_http()
    form = http['form']

    if (('secretToken' in form and
         form['secretToken'].value == config['blog_title'])):
        return False

    dump = '\n'.join(['%s: %s' % (arg.name, arg.value)
                      for arg in list(dict(form).values())])
    logger = tools.get_logger()
    logger.info('Comment rejected from %s:\n%s' % (
            http['REMOTE_ADDR'], dump))
    return True
