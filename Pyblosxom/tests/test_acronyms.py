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
import re

from Pyblosxom import pyblosxom
from Pyblosxom.tests import PluginTest, TIMESTAMP
from Pyblosxom.plugins import acronyms

class Test_acronyms(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, acronyms)

    def tearDown(self):
        PluginTest.tearDown(self)

    def test_get_acronym_file(self):
        config = dict(self.config_base)
        self.assertTrue(acronyms.get_acronym_file(config),
                     os.path.join(self.datadir, os.pardir, "acronyms.txt"))

        config["acronym_file"] = os.path.join(self.datadir, "foo.txt")
        self.assertTrue(acronyms.get_acronym_file(config),
                     os.path.join(self.datadir, "foo.txt"))

    def test_verify_installation(self):
        config = dict(self.config_base)
        req = pyblosxom.Request(config, self.environ, {})
        self.assertTrue(acronyms.verify_installation(req) == 0)

        config["acronym_file"] = os.path.join(self.datadir, "foo.txt")
        req = pyblosxom.Request(config, self.environ, {})
        filename = acronyms.get_acronym_file(config)
        fp = open(filename, "w")
        fp.write("...")
        fp.close()
        
        self.assertTrue(acronyms.verify_installation(req) == 1)

    def test_build_acronyms(self):
        def check_this(lines, output):
            for inmem, outmem in zip(acronyms.build_acronyms(lines), output):
                self.assertEqual(inmem[0].pattern, outmem[0])
                self.assertEqual(inmem[1], outmem[1])

        check_this(["FOO = bar"],
                   [("(\\bFOO\\b)", "<acronym title=\"bar\">\\1</acronym>")])
        check_this(["FOO. = bar"],
                   [("(\\bFOO.\\b)", "<abbr title=\"bar\">\\1</abbr>")])
        check_this(["FOO = abbr|bar"],
                   [("(\\bFOO\\b)", "<abbr title=\"bar\">\\1</abbr>")])
        check_this(["FOO = acronym|bar"],
                   [("(\\bFOO\\b)", "<acronym title=\"bar\">\\1</acronym>")])
        # this re doesn't compile, so it gets skipped
        check_this(["FOO[ = bar"], [])

    def test_cb_story(self):
        req = pyblosxom.Request(
            self.config, self.environ,
            {"acronyms":acronyms.build_acronyms(["FOO = bar"])})

        # basic test
        args = {"request": req,
                "entry": {"body": "<p>This is FOO!</p>"}}

        ret = acronyms.cb_story(args)

        self.assertEqual(
            args["entry"]["body"],
            "<p>This is <acronym title=\"bar\">FOO</acronym>!</p>")

        # test to make sure substitutions don't happen in tags
        args = {"request": req,
                "entry": {"body": "<FOO>This is FOO!</FOO>"}}

        ret = acronyms.cb_story(args)

        self.assertEqual(
            args["entry"]["body"],
            "<FOO>This is <acronym title=\"bar\">FOO</acronym>!</FOO>")
