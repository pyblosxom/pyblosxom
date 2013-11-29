#######################################################################
# Copyright (c) 2006 Blake Winton
#
# Released into the Public Domain.
#######################################################################

"""
Summary
=======

This plugin implements the ``comment_reject`` callback of the comments
plugin.

If someone tries to comment on an entry that's older than 28 days, the
comment is rejected.


Install
=======

Requires the ``comments`` plugin.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.no_old_comments`` to the ``load_plugins``
   list in your ``config.py`` file.


Revisions
=========

1.0 - August 5th 2006: First released.
"""

__author__ = "Blake Winton"
__email__ = "bwinton+blog@latte.ca"
__version__ = "2011-10-28"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Prevent comments on entries older than a month."
__category__ = "comments"
__license__ = "Public Domain"
__registrytags__ = "1.4, 1.5, core"


import time
from Pyblosxom import tools


def verify_installation(request):
    return True


def cb_comment_reject(args):
    req = args["request"]
    comment = args["comment"]
    blog_config = req.get_configuration()

    max_age = blog_config.get('no_old_comments_max_age', 2419200)

    data = req.get_data()
    entry = data['entry_list'][0]

    logger = tools.get_logger()

    logger.debug('%s -> %s', entry['mtime'], comment)

    if (time.time() - entry['mtime']) >= max_age:
        logger.info('Entry too old, comment not posted!')
        return 1

    logger.info('Entry ok, comment posted!')
    return 0
