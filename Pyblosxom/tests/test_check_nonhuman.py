#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

import unittest

from Pyblosxom.tests import PluginTest, TIMESTAMP
from Pyblosxom.plugins import check_nonhuman

class TestCheckNonhuman(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, check_nonhuman)

    def test_comment_reject(self):
        comment = {}
        self.args['comment'] = comment

        # no iamhuman, rejection!
        ret = check_nonhuman.cb_comment_reject(self.args)
        self.assertEqual(True, ret[0])

        # iamhuman, so it passes
        comment['iamhuman'] = 'yes'
        ret = check_nonhuman.cb_comment_reject(self.args)
        self.assertEqual(False, ret)

        # foo, so it passes
        del comment['iamhuman']
        self.args["request"].get_configuration()["nonhuman_name"] = "foo"
        comment['foo'] = 'yes'
        ret = check_nonhuman.cb_comment_reject(self.args)
        self.assertEqual(False, ret)
