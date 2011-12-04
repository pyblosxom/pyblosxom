#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2003, 2004, 2005 Sean Bowman
# Copyright (c) 2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

A reStructuredText entry formatter for pyblosxom.  reStructuredText is
part of the docutils project (http://docutils.sourceforge.net/).  To
use, you need a *recent* version of docutils.  A development snapshot
(http://docutils.sourceforge.net/#development-snapshots) will work
fine.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.rst_parser`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Install docutils.  Instructions are at
   http://docutils.sourceforge.net/


Usage
=====

Blog entries with a ``.rst`` extension will be parsed as
restructuredText.

You can also configure this as your default preformatter for ``.txt``
files by configuring it in your config file as follows::

   py['parser'] = 'reST'

Additionally, you can do this on an entry-by-entry basis by adding a
``#parser reST`` line in the metadata section.  For example::

   My Little Blog Entry
   #parser reST
   My main story...


Configuration
=============

There's two optional configuration parameter you can for additional
control over the rendered HTML::

   # To set the starting level for the rendered heading elements.
   # 1 is the default.
   py['reST_initial_header_level'] = 1

   # Enable or disable the promotion of a lone top-level section title to
   # document title (and subsequent section title to document subtitle
   # promotion); enabled by default.
   py['reST_transform_doctitle'] = 1


.. Note::

   If you're not seeing headings that you think should be there, try
   changing the ``reST_initial_header_level`` property to 0.
"""

__author__ = "Sean Bowman"
__email__ = "sean dot bowman at acm dot org"
__version__ = "2011-10-23"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "restructured text support for blog entries"
__category__ = "text"
__license__ = "MIT"
__registrytags__ = "1.5, core"


from docutils.core import publish_parts
from Pyblosxom import tools


PREFORMATTER_ID = 'reST'
FILE_EXT = 'rst'


def verify_installation(args):
    # no configuration needed
    return 1


def cb_entryparser(args):
    args[FILE_EXT] = readfile
    return args


def cb_preformat(args):
    if args.get("parser", None) == PREFORMATTER_ID:
        return parse(''.join(args['story']), args['request'])


def parse(story, request):
    config = request.getConfiguration()
    initial_header_level = config.get('reST_initial_header_level', 1)
    transform_doctitle = config.get('reST_transform_doctitle', 1)
    settings = {
        'initial_header_level': initial_header_level,
        'doctitle_xform': transform_doctitle
        }
    parts = publish_parts(
        story, writer_name='html', settings_overrides=settings)
    return parts['body']


def readfile(filename, request):
    entry_data = {}
    lines = open(filename).readlines()

    if len(lines) == 0:
        return {"title": "", "body": ""}

    title = lines.pop(0).strip()

    # absorb meta data
    while lines and lines[0].startswith("#"):
        meta = lines.pop(0)
        # remove the hash
        meta = meta[1:].strip()
        meta = meta.split(" ", 1)
        # if there's no value, we append a 1
        if len(meta) == 1:
            meta.append("1")
        entry_data[meta[0].strip()] = meta[1].strip()

    body = parse(''.join(lines), request)
    entry_data["title"] = title
    entry_data["body"] = body

    # Call the postformat callbacks
    tools.run_callback('postformat', {'request': request,
                                      'entry_data': entry_data})
    return entry_data
