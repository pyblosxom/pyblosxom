#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2006-2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

This works in conjunction with the comments plugin and allows you to
significantly reduce comment spam by adding a "I am human" checkbox to
your form.  Any comments that aren't "from a human" get rejected
immediately.

This shouldn't be the only way you reduce comment spam.  It's probably
not useful to everyone, but would be useful to some people as a quick
way of catching some of the comment spam they're getting.

Usually this works for a while, then spam starts coming in again.  At
that point, I change the ``nonhuman_name`` config.py variable value
and I stop getting comment spam.


Install
=======

Requires the ``comments`` plugin.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.check_nonhuman`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Configure as documented below.


Usage
=====

For setup, copy the plugin to your plugins directory and add it to
your load_plugins list in your config.py file.

Then add the following item to your config.py (this defaults to
"iamhuman")::

   py["nonhuman_name"] = "iamhuman"


Then add the following to your comment-form template just above the
submit button (make sure to match the input name to your configured
input name)::

   <input type="checkbox" name="iamhuman" value="yes">
   Yes, I am human!


Alternatively, if you set the ``nonhuman_name`` property, then you should
do this::

   <input type="checkbox" name="$(nonhuman_name)" value="yes">
   Yes, I am human!


Additionally, the nonhuman plugin can log when it rejected a comment.
This is good for statistical purposes.  1 if "yes, I want to log" and
0 (default) if "no, i don't want to log".  Example::

   py["nonhuman_log"] = 1


And that's it!

The idea came from::

   http://www.davidpashley.com/cgi/pyblosxom.cgi/2006/04/28#blog-spam
"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2011-10-25"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Rejects non-human comments."
__category__ = "comments"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


import os
import time
from Pyblosxom.tools import pwrap


def verify_installation(request):
    config = request.get_configuration()
    if not "nonhuman_name" in config:
        pwrap("missing optional property: 'nonhuman_name'")

    return True


def cb_comment_reject(args):
    r = args["request"]
    c = args["comment"]

    config = r.get_configuration()

    if not config.get("nonhuman_name", "iamhuman") in c:
        if config.get("nonhuman_log", 0) and "logdir" in config:
            fn = os.path.join(config["logdir"], "nothuman.log")
            f = open(fn, "a")
            f.write("%s: %s\n" % (
                    time.ctime(), c.get("ipaddress", None)))
            f.close()
        return True, "Comment rejected: I don't think you're human."

    return False
