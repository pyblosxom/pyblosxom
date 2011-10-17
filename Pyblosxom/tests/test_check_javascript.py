#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (C) 2010-2011 by the PyBlosxom team.  See AUTHORS.
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Tests for the check_javascript plugin.
"""

__author__ = 'Ryan Barrett <pyblosxom@ryanb.org>'
__url__ = 'http://pyblosxom.bluesock.org/wiki/index.php/Framework_for_testing_plugins'

from Pyblosxom.tests import PluginTest
from Pyblosxom.plugins.comments import check_javascript

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
        self.assertEquals(True, check_javascript.cb_comment_reject(self.args))

        # bad secretToken
        self.set_form_data({'secretToken': 'not the title'})
        self.assertEquals(True, check_javascript.cb_comment_reject(self.args))

        # good secretToken
        self.set_form_data({'secretToken': 'test title'})
        self.assertEquals(False, check_javascript.cb_comment_reject(self.args))
