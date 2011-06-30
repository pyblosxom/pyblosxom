from plugins.tests.test_base import PluginTest
from plugins.content import pages

class PagesTest(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, pages)

    def test_is_frontpage(self):
        # test setup-related is_frontpage = False possibilities
        self.assertEquals(pages.is_frontpage({}, {}), False)
        self.assertEquals(pages.is_frontpage({"PATH_INFO": "/"}, {}),
                          False)
        self.assertEquals(pages.is_frontpage({"PATH_INFO": "/"},
                                             {"pages_frontpage": False}),
                          False)

        # test path-related possibilities
        for path, expected in (("", True),
                               ("/", True),
                               ("/index", True),
                               ("index", True),
                               ("/index.html", True),
                               ("/index.xml", True),
                               ("/foo", False)):
            pyhttp = {"PATH_INFO": path}
            cfg = {"pages_frontpage": True}
            self.assertEquals(pages.is_frontpage(pyhttp, cfg), expected)
