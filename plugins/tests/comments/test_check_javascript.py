"""
Tests for the check_javascript plugin.
"""

__author__ = 'Ryan Barrett <pyblosxom@ryanb.org>'
__url__ = 'http://pyblosxom.sourceforge.net/wiki/index.php/Framework_for_testing_plugins'

from nose.tools import eq_
from plugins.tests.test_base import PluginTest
from plugins.comments.plugins import check_javascript
import cgi, cPickle, os, StringIO, sys, urllib

class TestCheckJavascript(PluginTest):
    """Test class for the check_javascript plugin.
    """
    def setUp(self):
        PluginTest.setUp(self, check_javascript)
        self.config['blog_title'] = 'test title'

    def test_comment_reject(self):
        """check_javascript should check the secretToken query argument."""
        # no secretToken
        assert 'secretToken' not in self.http
        eq_(True, check_javascript.cb_comment_reject(self.args))

        # bad secretToken
        self.set_form_data({'secretToken': 'not the title'})
        eq_(True, check_javascript.cb_comment_reject(self.args))

        # good secretToken
        self.set_form_data({'secretToken': 'test title'})
        eq_(False, check_javascript.cb_comment_reject(self.args))
