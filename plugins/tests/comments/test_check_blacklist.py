import unittest

from plugins.tests.test_base import PluginTest
from plugins.comments import check_blacklist

class TestCheckBlacklist(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, check_blacklist)

    def test_comment_reject(self):
        comment = {}
        self.args['comment'] = comment
        cfg = self.args["request"].get_configuration()

        # no comment_rejected_words--so it passes
        ret = check_blacklist.cb_comment_reject(self.args)
        self.assertEquals(False, ret)

        # rejected words, but none in the comment
        cfg["comment_rejected_words"] = ["foo"]
        comment["body"] = "this is a happy comment"
        ret = check_blacklist.cb_comment_reject(self.args)
        self.assertEquals(False, ret)

        # rejected words, one is in the comment
        cfg["comment_rejected_words"] = ["this"]
        ret = check_blacklist.cb_comment_reject(self.args)
        self.assertEquals(True, ret[0])
