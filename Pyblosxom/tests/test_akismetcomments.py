#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Tests for the akismetcomments plugin.
"""

__author__ = 'Ryan Barrett <pyblosxom@ryanb.org>'
__url__ = 'http://pyblosxom.github.com/wiki/index.php/Framework_for_testing_plugins'

from Pyblosxom.tests import PluginTest
from Pyblosxom.plugins import akismetcomments
import sys

# FIXME: we do some icky things here to mock Akismet.  It'd be better
# to have a real mocking module like Mock or Fudge.

class MockAkismet:
    """A mock Akismet class."""
    GOOD_KEY = 'my_test_key'
    IPADDRESS = '12.34.56.78'
    BLOG_URL = 'http://blog.url/'
    comment_check_return = None
    comment_check_error = False

    def __init__(self, key=None, blog_url=None, agent=None):
        self.key = key
        assert MockAkismet.BLOG_URL == blog_url

    def verify_key(self):
        return self.key == MockAkismet.GOOD_KEY

    def comment_check(self, comment, data=None, build_data=True, DEBUG=False):
        if MockAkismet.comment_check_error:
            MockAkismet.comment_check_error = False
            raise akismet.AkismetError()
        else:
            assert 'foo' == comment
            ret = MockAkismet.comment_check_return
            MockAkismet.comment_check_return = None
            return ret

    @classmethod
    def inject_comment_check(cls, ret):
        cls.comment_check_return = ret

    @classmethod
    def inject_comment_check_error(cls):
        cls.comment_check_error = True

class Mockakismet:
    class AkismetError(Exception):
        pass

    Akismet = MockAkismet

sys.modules['akismet'] = Mockakismet
import akismet


class TestAkismetComments(PluginTest):
    """Test class for the akismetcomments plugin.
    """
    def setUp(self):
        PluginTest.setUp(self, akismetcomments)

        akismet.Akismet = MockAkismet

        self.config['base_url'] = MockAkismet.BLOG_URL
        self.config['akismet_api_key'] = MockAkismet.GOOD_KEY
        self.args['comment'] = {'description': "foo",
                                'ipaddress': MockAkismet.IPADDRESS}

    def test_verify_installation(self):
        """verify_installation should check for an api key and verify it."""
        self.assertEqual(
            True, akismetcomments.verify_installation(self.request))

        # try without an akismet_api_key config var
        del self.config['akismet_api_key']
        self.assertEqual(
            False, akismetcomments.verify_installation(self.request))

        # try with an import error
        akismet = sys.modules['akismet']
        del sys.modules['akismet']
        self.assertEqual(
            False, akismetcomments.verify_installation(self.request))
        sys.modules['akismet'] = akismet

        # try with a key that doesn't verify
        self.config['akismet_api_key'] = 'bad_key'
        orig_verify_key = akismet.Akismet.verify_key
        self.assertEqual(False, akismetcomments.verify_installation(self.request))

    def test_comment_reject(self):
        """comment_reject() should pass the comment through to akismet."""
        # no comment to reject
        assert 'comment' not in self.data
        self.assertEqual(
            False,
            akismetcomments.cb_comment_reject(self.args))

        self.set_form_data({})
        self.assertEqual(
            False, akismetcomments.cb_comment_reject(self.args))
        self.set_form_data({'body': 'body'})

    def test_bad_api_key_reject(self):
        # bad api key
        self.config['akismet_api_key'] = 'bad_key'
        self.assertEqual(
            False, akismetcomments.cb_comment_reject(self.args))
        self.config['akismet_api_key'] = MockAkismet.GOOD_KEY

    def test_akismet_error(self):
        # akismet error
        MockAkismet.inject_comment_check_error()
        print(akismet.Akismet.comment_check_error)
        self.assertEqual(
            (True, 'Missing essential data (e.g., a UserAgent string).'),
            akismetcomments.cb_comment_reject(self.args))

    def test_akismet_ham(self):
        # akismet says ham
        MockAkismet.inject_comment_check(False)
        self.assertEqual(
            False, akismetcomments.cb_comment_reject(self.args))

    def test_akismet_spam(self):
        # akismet says spam
        MockAkismet.inject_comment_check(True)
        self.assertEqual(
            (True, 'I\'m sorry, but your comment was rejected by the <a href="'
             'http://akismet.com/">Akismet</a> spam filtering system.'),
            akismetcomments.cb_comment_reject(self.args))
