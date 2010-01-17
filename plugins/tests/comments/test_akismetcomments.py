"""
Tests for the akismetcomments plugin.
"""

__author__ = 'Ryan Barrett <pyblosxom@ryanb.org>'
__url__ = 'http://pyblosxom.sourceforge.net/wiki/index.php/Framework_for_testing_plugins'

from nose.tools import eq_
from plugins.tests.test_base import PluginTest
from plugins.comments.plugins import akismet, akismetcomments
import sys

class MockAkismet:
    """A mock Akismet class."""
    GOOD_KEY = 'my_test_key'
    IPADDRESS = '12.34.56.78'
    BLOG_URL = 'http://blog.url/'
    comment_check_return = None
    comment_check_error = False

    def __init__(self, key=None, blog_url=None, agent=None):
        self.key = key
        eq_(MockAkismet.BLOG_URL, blog_url)

    def verify_key(self):
        return self.key == MockAkismet.GOOD_KEY

    def comment_check(self, body, data):
        if MockAkismet.comment_check_error:
            MockAkismet.comment_check_error = False
            raise akismet.AkismetError()
        else:
            eq_('body', body)
            return MockAkismet.comment_check_return

    @classmethod
    def inject_comment_check(cls, ret):
        cls.comment_check_return = ret

    @classmethod
    def inject_comment_check_error(cls):
        cls.comment_check_error = True

class TestAkismetComments(PluginTest):
    """Test class for the akismetcomments plugin.
    """
    def setUp(self):
        PluginTest.setUp(self, akismetcomments)

        akismet.Akismet = MockAkismet
        self.config['base_url'] = MockAkismet.BLOG_URL
        self.config['akismet_api_key'] = MockAkismet.GOOD_KEY
        self.args['comment'] = {'ipaddress': MockAkismet.IPADDRESS}

    def test_verify_installation(self):
        """verify_installation should check for an api key and verify it."""
        eq_(True, akismetcomments.verify_installation(self.request))

        # try without an akismet_api_key config var
        del self.config['akismet_api_key']
        eq_(False, akismetcomments.verify_installation(self.request))

        # try with an import error
        akismet = sys.modules['plugins.comments.plugins.akismet']
        del sys.modules['plugins.comments.plugins.akismet']
        eq_(False, akismetcomments.verify_installation(self.request))
        sys.modules['plugins.comments.plugins.akismet'] = akismet

        # try with a key that doesn't verify
        self.config['akismet_api_key'] = 'bad_key'
        orig_verify_key = akismet.Akismet.verify_key
        eq_(False, akismetcomments.verify_installation(self.request))

    def test_comment_reject(self):
        """comment_reject() should pass the comment through to akismet."""
        # no comment to reject
        assert 'comment' not in self.data
        eq_(False, akismetcomments.cb_comment_reject(self.args))

        self.set_form_data({})
        eq_(False, akismetcomments.cb_comment_reject(self.args))
        self.set_form_data({'body': 'body'})

        # bad api key
        self.config['akismet_api_key'] = 'bad_key'
        eq_(False, akismetcomments.cb_comment_reject(self.args))
        self.config['akismet_api_key'] = MockAkismet.GOOD_KEY

        # akismet error
        MockAkismet.inject_comment_check_error()
        eq_((True, 'Missing essential data (e.g., a UserAgent string).'),
            akismetcomments.cb_comment_reject(self.args))

        # akismet says ham
        MockAkismet.inject_comment_check(False)
        eq_(False, akismetcomments.cb_comment_reject(self.args))

        # akismet says spam
        MockAkismet.inject_comment_check(True)
        eq_((True, 'I\'m sorry, but your comment was rejected by the <a href="'
                   'http://akismet.com/">Akismet</a> spam filtering system.'),
            akismetcomments.cb_comment_reject(self.args))
