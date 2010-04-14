#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

If PyBlosxom is rendering a single entry (i.e. entry_list has 1 item
in it), then this populates the ``entry_title`` variable for the
header template.

Usage
=====

To use, add the ``$entry_title`` variable to your header template in
the <title> area.

Example::

    <title>$(blog_title)$(entry_title)</title>

"""
__author__ = "Will Kahn-Greene - willg at bluesock dot org"
__version__ = "2010-04-14"
__url__ = "http://pyblosxom.sourceforge.net/"
__description__ = "Populates $(entry_title) for head template."

def verify_installation(request):
    return 1

def cb_head(args):
    req = args["request"]
    entry = args["entry"]
    
    data = req.get_data()

    entry_list = data["entry_list"]
    if len(entry_list) == 1:
        entry["entry_title"] = ":: " + entry_list[0].get("title", "No title")

    return args
