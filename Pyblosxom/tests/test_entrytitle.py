#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

import time
import os

from Pyblosxom import pyblosxom
from Pyblosxom.tests import PluginTest, TIMESTAMP
from Pyblosxom.plugins import entrytitle

class Test_entrytitle(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, entrytitle)

    def test_cb_head(self):
        # no entries yields no entry_title
        args = {
            "request": pyblosxom.Request({}, {}, {}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEqual(newargs["entry"].get("entry_title", ""), "")

        # one entry yields entry_title
        args = {
            "request": pyblosxom.Request(
                {},
                {},
                {"entry_list": [{"title": "foobar"}]}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEqual(newargs["entry"]["entry_title"], ":: foobar")

        # one entry with no title yields entry_title with "No title"
        args = {
            "request": pyblosxom.Request(
                {},
                {},
                {"entry_list": [{}]}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEqual(newargs["entry"]["entry_title"], ":: No title")

        # one entry yields entry_title, using entry_title_template
        # configuration property
        args = {
            "request": pyblosxom.Request(
                {"entry_title_template": "%(title)s ::"},
                {},
                {"entry_list": [{"title": "foobar"}]}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEqual(newargs["entry"]["entry_title"], "foobar ::")

        # multiple entries yields no title
        args = {
            "request": pyblosxom.Request(
                {},
                {},
                {"entry_list": [{"title": "foobar"}, {"title": "foobar2"}]}),
            "entry": {}
            }
        newargs = entrytitle.cb_head(args)
        self.assertEqual(newargs["entry"].get("entry_title", ""), "")

    def test_verify_installation(self):
        self.assertTrue(entrytitle.verify_installation(self.request))
