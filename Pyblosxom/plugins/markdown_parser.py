#######################################################################
# Copyright (C) 2005, 2011 Benjamin Mako Hill
# Copyright (c) 2009, 2010, seanh
# Copyright (c) 2011 Blake Winton
# Copyright (c) 2011 Will Kahn-Greene
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#######################################################################

"""
Summary
=======

A Markdown entry formatter for Pyblosxom.


Install
=======

Requires python-markdown to be installed.  See
http://www.freewisdom.org/projects/python-markdown/ for details.

1. Add ``Pyblosxom.plugins.markdown_parser`` to the ``load_plugins``
   list in your ``config.py`` file


Usage
=====

Write entries using Markdown markup.  Entry filenames can end in
``.markdown``, ``.md``, and ``.mkd``.

You can also configure this as your default preformatter for ``.txt``
files by configuring it in your config file as follows::

   py['parser'] = 'markdown'

Additionally, you can do this on an entry-by-entry basis by adding a
``#parser markdown`` line in the metadata section.  For example::

   My Little Blog Entry
   #parser markdown
   My main story...

"""

__author__ = (
    "Benjamin Mako Hill <mako@atdot.cc>, seanh <snhmnd@gmail.com>, "
    "Blake Winton <bwinton@latte.ca>")
__email__ = ""
__version__ = "2011-11-02"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "Markdown entry parser"
__category__ = "text"
__license__ = "GPLv3 or later"
__registrytags__ = "1.5, core"

PREFORMATTER_ID = "markdown"
FILENAME_EXTENSIONS = ("markdown", "md", "mkd")

import markdown
from Pyblosxom import tools

md = markdown.Markdown(output_format="html4",
                       extensions=["footnotes", "codehilite"])


def verify_installation(args):
    # no configuration needed
    return 1


def cb_entryparser(args):
    for ext in FILENAME_EXTENSIONS:
        args[ext] = readfile
    return args


def cb_preformat(args):
    if args.get("parser", None) == PREFORMATTER_ID:
        return parse("".join(args["story"]), args["request"])


def parse(story, request):
    body = md.convert(story.decode("utf-8")).encode("utf-8")
    md.reset()
    return body


def readfile(filename, request):
    logger = tools.get_logger()
    logger.info("Calling readfile for %s", filename)
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

    body = parse("".join(lines), request)
    entry_data["title"] = title
    entry_data["body"] = body

    # Call the postformat callbacks
    tools.run_callback("postformat", {"request": request,
                                      "entry_data": entry_data})
    logger.info("Returning %r", entry_data)
    return entry_data
