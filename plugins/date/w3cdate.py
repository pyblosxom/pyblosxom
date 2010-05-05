"""
Adds a 'w3cdate' variable to every entry which has the mtime of the
entry in ISO8601 format.

Adds a 'w3cdate' variable to the head and foot templates which has the
mtime of the first entry in the entrylist being displayed (this is
often the youngest/most-recent entry).


.. Note::

    When adding this plugin to the ``load_plugins`` list, it helps to
    put the plugin early in the list so that the data will be
    available to subsequent plugins.

.. Note::

    You might get better results if you have PyXMl installed as part
    of your Python installation.  If you don't, then we fudge the date
    using a home-brew function.


Thanks to Matej Cepl for the hacked iso8601 code that doesn't require
PyXML.


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
Copyright (c) 2010 Will Kahn-Greene         
"""
__author__ = "Ted Leung <twl@sauria.com>"
__version__ = "$Id$"
__copyright__ = "Copyright (c) 2003-2005 Ted Leung, 2010 Will Kahn-Greene"
__license__ = "Python"

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

import unittest

class W3CDateTest(unittest.TestCase):
    entry1 = {"timetuple": (2010, 1, 17, 15, 48, 20, 6, 17, 0)}
    entry2 = {"timetuple": (2010, 1, 17, 15, 58, 45, 6, 17, 0)}
    entry3 = {"timetuple": (2010, 1, 11, 21, 6, 26, 0, 11, 0)}
    
    def test_get_formatted_date(self):
        gfd = get_formatted_date
        #save old TZ environment for restoring
        tz = os.environ.get('TZ')
        #we expect US EASTERN time without DST
        os.environ['TZ'] = 'EST+05EST+05,M4.1.0,M10.5.0'
        time.tzset()
        self.assertEquals(gfd(self.entry1),
                          "2010-01-17T15:48:20-05:00")
        # reset time zone to whatever it was
        if tz is None:
            del os.environ['TZ']
        else:
            os.environ['TZ'] = tz
        time.tzset()

    def test_head_and_foot(self):
        from Pyblosxom.pyblosxom import Request
        gfd = get_formatted_date
        
        entry1 = dict(self.entry1)
        entry2 = dict(self.entry2)
        entry3 = dict(self.entry3)

        req = Request({}, {}, {"entry_list": [entry1, entry2, entry3]})
        entry = {}
        args = {"entry": entry, "request": req}
        cb_head(args)
        self.assertEquals(entry["w3cdate"], gfd(self.entry1))

        req = Request({}, {}, {"entry_list": [entry3, entry2, entry1]})
        entry = {}
        args = {"entry": entry, "request": req}
        cb_head(args)
        self.assertEquals(entry["w3cdate"], gfd(self.entry3))

    def test_story(self):
        entry = dict(self.entry1)
        args = {"entry": entry}
        cb_story(args)
        self.assertEquals(entry['w3cdate'], get_formatted_date(entry))
        

def get_test_suite():
    ret = unittest.TestLoader().loadTestsFromTestCase(W3CDateTest)
    return ret
