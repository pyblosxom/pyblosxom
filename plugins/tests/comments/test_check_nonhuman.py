import unittest

from plugins.tests.test_base import PluginTest, TIMESTAMP
from plugins.comments import check_nonhuman

class TestCheckNonhuman(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, check_nonhuman)

    def test_comment_reject(self):
        comment = {}
        self.args['comment'] = comment

        # no iamhuman, rejection!
        ret = check_nonhuman.cb_comment_reject(self.args)
        self.assertEquals(True, ret[0])

        # iamhuman, so it passes
        comment['iamhuman'] = 'yes'
        ret = check_nonhuman.cb_comment_reject(self.args)
        self.assertEquals(False, ret)

        # foo, so it passes
        del comment['iamhuman']
        self.args["request"].get_configuration()["nonhuman_name"] = "foo"
        comment['foo'] = 'yes'
        ret = check_nonhuman.cb_comment_reject(self.args)
        self.assertEquals(False, ret)
