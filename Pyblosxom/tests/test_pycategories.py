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

from Pyblosxom.entries.base import generate_entry

from Pyblosxom.tests import PluginTest, TIMESTAMP
from Pyblosxom.plugins import pycategories

def parse_text():
    return

class Test_pycategories(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, pycategories)
        self.request.get_data()["extensions"] = {"txt": parse_text}

    def tearDown(self):
        PluginTest.tearDown(self)

    def test_cb_prepare(self):
        self.assertTrue("categorylinks" not in self.request.get_data())
        pycategories.cb_prepare(self.args)
        self.assertTrue("categorylinks" in self.request.get_data())

    def test_verify_installation(self):
        self.assertTrue(pycategories.verify_installation)

    def test_no_categories(self):
        pycategories.cb_prepare(self.args)
        self.assertEqual(
            str(self.request.get_data()["categorylinks"]),
            "<ul class=\"categorygroup\">\n\n</ul>")

    def generate_entry(self, filename):
        filename = os.path.join(self.datadir, filename)
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
            
        file = open(filename, "w")
        file.write("Test entry at %s\nbody body body\n" % filename)
        file.close()

    def test_categories(self):
        self.generate_entry("test1.txt")
        self.generate_entry("cat1/test_cat1.txt")
        self.generate_entry("cat2/test_cat2.txt")

        pycategories.cb_prepare(self.args)
        self.assertEqual(
            str(self.request.get_data()["categorylinks"]),
            "\n".join(
                ['<ul class="categorygroup">',
                 '<li><a href="http://bl.og//index.html">/</a> (3)</li>',
                 '<li><ul class="categorygroup">',
                 '<li><a href="http://bl.og//cat1/index.html">cat1/</a> (1)</li>',
                 '<li><a href="http://bl.og//cat2/index.html">cat2/</a> (1)</li>',
                 '</ul></li>',
                 '</ul>']))
