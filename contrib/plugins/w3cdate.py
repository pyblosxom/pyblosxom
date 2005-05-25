"""
Adds a 'w3cdate' variable to every entry which has the mtime of the entry
in ISO8601 format

Adds a 'w3cdate' variable to the head and foot templates which has the mtime
of the first entry in the entrylist being displayed (this is often the
youngest/most-recent entry).


WARNING: you must have PyXML installed as part of your python installation 
in order for this plugin to work

Place this plugin early in your load_plugins list, so that the w3cdate will
be available to subsequent plugins


Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Copyright (c) 2003-2005 Ted Leung
"""
__author__ = "Ted Leung <twl@sauria.com>"
__version__ = "$Id$"
__copyright__ = "Copyright (c) 2003-2005 Ted Leung"
__license__ = "Python"

import xml.utils.iso8601
import time
from Pyblosxom import tools

def get_formatted_date(entry):
    if not entry:
        return ""

    time_tuple = entry['timetuple']
    tzoffset = time.timezone

    # if is_dst flag set, adjust for daylight savings time
    if time_tuple[8] == 1:
        tzoffset = time.altzone
    return xml.utils.iso8601.tostring(time.mktime(time_tuple),tzoffset)    


def cb_head(args):
    entry = args["entry"]

    req = args["request"]
    data = req.getData()
    config = req.getConfiguration()

    entrylist = data.get("entry_list", None)
    if not entrylist:
        return args

    entry["w3cdate"] = get_formatted_date(entrylist[0])
    return args


def cb_story(args):
    entry = args['entry']
    entry["w3cdate"] = get_formatted_date(entry)


def cb_foot(args):
    entry = args["entry"]

    req = args["request"]
    data = req.getData()
    config = req.getConfiguration()

    entrylist = data.get("entry_list", None)
    if not entrylist:
        return args

    entry["w3cdate"] = get_formatted_date(entrylist[0])
    return args
