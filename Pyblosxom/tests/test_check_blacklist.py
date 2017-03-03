#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

import unittest

from Pyblosxom.tests import PluginTest
from Pyblosxom.plugins import check_blacklist

class TestCheckBlacklist(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, check_blacklist)

    def test_comment_reject(self):
        comment = {}
        self.args['comment'] = comment
        cfg = self.args["request"].get_configuration()

        # no comment_rejected_words--so it passes
        ret = check_blacklist.cb_comment_reject(self.args)
        self.assertEqual(False, ret)

        # rejected words, but none in the comment
        cfg["comment_rejected_words"] = ["foo"]
        comment["body"] = "this is a happy comment"
        ret = check_blacklist.cb_comment_reject(self.args)
        self.assertEqual(False, ret)

        # rejected words, one is in the comment
        cfg["comment_rejected_words"] = ["this"]
        ret = check_blacklist.cb_comment_reject(self.args)
        self.assertEqual(True, ret[0])
