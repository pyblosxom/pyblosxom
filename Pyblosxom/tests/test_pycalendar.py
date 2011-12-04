#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

from Pyblosxom.plugins import pycalendar

import os
import unittest
import tempfile
import shutil

class PyCalendarTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        if hasattr(self, 'tmpdir'):
            shutil.rmtree(self.tmpdir)

    def get_datadir(self):
        return os.path.join(self.tmpdir, "datadir")

    entry1 = {"timetuple": (2010, 1, 17, 15, 48, 20, 6, 17, 0)}

    def test_generate_calendar(self):
        entry1 = dict(PyCalendarTest.entry1)

        from Pyblosxom.pyblosxom import Request
        req = Request({"datadir": self.get_datadir()},
                      {},
                      {"entry_list": [entry1],
                       "extensions": {}})
        pycalendar.cb_prepare({"request": req})

        data = req.get_data()
        cal = data["calendar"]

        cal.generate_calendar()
