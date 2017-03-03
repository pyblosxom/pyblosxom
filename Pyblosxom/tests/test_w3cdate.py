#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

from Pyblosxom.plugins import w3cdate

import os
import unittest
import time

class W3CDateTest(unittest.TestCase):
    entry1 = {"timetuple": (2010, 1, 17, 15, 48, 20, 6, 17, 0)}
    entry2 = {"timetuple": (2010, 1, 17, 15, 58, 45, 6, 17, 0)}
    entry3 = {"timetuple": (2010, 1, 11, 21, 6, 26, 0, 11, 0)}

    def test_get_formatted_date(self):
        gfd = w3cdate.get_formatted_date
        #save old TZ environment for restoring
        tz = os.environ.get('TZ')
        #we expect US EASTERN time without DST
        os.environ['TZ'] = 'EST+05EST+05,M4.1.0,M10.5.0'
        time.tzset()
        self.assertEqual(gfd(W3CDateTest.entry1),
                          "2010-01-17T15:48:20-05:00")
        # reset time zone to whatever it was
        if tz is None:
            del os.environ['TZ']
        else:
            os.environ['TZ'] = tz
        time.tzset()

    def test_head_and_foot(self):
        from Pyblosxom.pyblosxom import Request
        gfd = w3cdate.get_formatted_date

        entry1 = dict(W3CDateTest.entry1)
        entry2 = dict(W3CDateTest.entry2)
        entry3 = dict(W3CDateTest.entry3)

        req = Request({}, {}, {"entry_list": [entry1, entry2, entry3]})
        entry = {}
        args = {"entry": entry, "request": req}
        w3cdate.cb_head(args)
        self.assertEqual(entry["w3cdate"], gfd(self.entry1))

        req = Request({}, {}, {"entry_list": [entry3, entry2, entry1]})
        entry = {}
        args = {"entry": entry, "request": req}
        w3cdate.cb_head(args)
        self.assertEqual(entry["w3cdate"], gfd(self.entry3))

    def test_story(self):
        entry = dict(self.entry1)
        args = {"entry": entry}
        w3cdate.cb_story(args)
        self.assertEqual(entry['w3cdate'], w3cdate.get_formatted_date(entry))
