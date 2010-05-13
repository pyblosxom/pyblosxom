import time
import os

from plugins.tests.test_base import PluginTest, TIMESTAMP
from plugins.archives import yeararchives

class Test_yeararchives(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, yeararchives)

    def tearDown(self):
        PluginTest.tearDown(self)

    def test_parse_path_info(self):
        for testin, testout in [
            ("", None),
            ("/", None),
            ("/2003", ("2003", None)),
            ("/2003/", ("2003", None)),
            ("/2003/index", ("2003", None)),
            ("/2003/index.flav", ("2003", "flav")),
            ]:
 
            self.assertEquals(yeararchives.parse_path_info(testin),
                              testout)
