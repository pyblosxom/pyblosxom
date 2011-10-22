#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003-2005 Ted Leung
# Copyright (c) 2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Adds a ``w3cdate`` variable to the head and foot templates which has
the mtime of the first entry in the entrylist being displayed (this is
often the youngest/most-recent entry).


.. Note::

   When adding this plugin to the ``load_plugins`` list, it helps to
   put the plugin early in the list so that the data will be
   available to subsequent plugins.

.. Note::

   You might get better results if you have PyXML installed as part
   of your Python installation.  If you don't, then we fudge the date
   using a home-brew function.


Thanks to Matej Cepl for the hacked iso8601 code that doesn't require
PyXML.
"""

__author__ = "Ted Leung"
__email__ = "twl at sauria dot com"
__version__ = "$Id$"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "Adds a 'w3cdate' variable which is the mtime in ISO8601 format."
__category__ = "date"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


import rfc822
import time
import os
from Pyblosxom import tools

def iso8601_hack_tostring(t, timezone):
    timezone = int(timezone)
    if timezone:
        sign = (timezone < 0) and "+" or "-"
        timezone = abs(timezone)
        hours = timezone / (60 * 60)
        minutes = (timezone % (60 * 60)) / 60
        tzspecifier = "%c%02d:%02d" % (sign, hours, minutes)
    else:
        tzspecifier = "Z"
    psecs = t - int(t)
    t = time.gmtime(int(t) - timezone)
    year, month, day, hours, minutes, seconds = t[:6]
    if seconds or psecs:
        if psecs:
            psecs = int(round(psecs * 100))
            f = "%4d-%02d-%02dT%02d:%02d:%02d.%02d%s"
            v = (year, month, day, hours, minutes, seconds, psecs, tzspecifier)
        else:
            f = "%4d-%02d-%02dT%02d:%02d:%02d%s"
            v = (year, month, day, hours, minutes, seconds, tzspecifier)
    else:
        f = "%4d-%02d-%02dT%02d:%02d%s"
        v = (year, month, day, hours, minutes, tzspecifier)
    return f % v

try:
    from xml.utils import iso8601
    format_date = iso8601.tostring

except (ImportError, AttributeError):
    format_date = iso8601_hack_tostring


def get_formatted_date(entry):
    if not entry:
        return ""

    time_tuple = entry['timetuple']
    tzoffset = time.timezone

    # if is_dst flag set, adjust for daylight savings time
    if time_tuple[8] == 1:
        tzoffset = time.altzone
    return format_date(time.mktime(time_tuple), tzoffset)

def cb_story(args):
    entry = args['entry']
    entry["w3cdate"] = get_formatted_date(entry)

def cb_head(args):
    entry = args["entry"]

    req = args["request"]
    data = req.get_data()

    entrylist = data.get("entry_list", None)
    if not entrylist:
        return args

    entry["w3cdate"] = get_formatted_date(entrylist[0])
    return args

cb_foot = cb_head
