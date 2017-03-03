#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Tests for the check_javascript plugin.
"""

__author__ = 'Ryan Barrett <pyblosxom@ryanb.org>'
__url__ = 'http://pyblosxom.github.com/wiki/index.php/Framework_for_testing_plugins'

from Pyblosxom.tests import PluginTest
from Pyblosxom.plugins import check_javascript

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
        self.assertEqual(True, check_javascript.cb_comment_reject(self.args))

        # bad secretToken
        self.set_form_data({'secretToken': 'not the title'})
        self.assertEqual(True, check_javascript.cb_comment_reject(self.args))

        # good secretToken
        self.set_form_data({'secretToken': 'test title'})
        self.assertEqual(False, check_javascript.cb_comment_reject(self.args))
