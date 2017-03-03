#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

from Pyblosxom.tests import PluginTest
from Pyblosxom.plugins import pages

class PagesTest(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, pages)

    def test_is_frontpage(self):
        # test setup-related is_frontpage = False possibilities
        self.assertEqual(pages.is_frontpage({}, {}), False)
        self.assertEqual(pages.is_frontpage({"PATH_INFO": "/"}, {}),
                          False)
        self.assertEqual(pages.is_frontpage({"PATH_INFO": "/"},
                                             {"pages_frontpage": False}),
                          False)

        # test path-related possibilities
        for path, expected in (("/", True),
                               ("/index", True),
                               ("/index.html", True),
                               ("/index.xml", True),
                               ("/foo", False)):
            pyhttp = {"PATH_INFO": path}
            cfg = {"pages_frontpage": True}
            self.assertEqual(pages.is_frontpage(pyhttp, cfg), expected)
