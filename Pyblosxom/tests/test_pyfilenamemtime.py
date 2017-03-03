#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################


from Pyblosxom.tests import PluginTest
from Pyblosxom.plugins import pyfilenamemtime
import time


def mtime_to_date(mtime):
    return time.strftime('%Y-%m-%d-%H-%M', time.localtime(mtime))


class Test_pyfilenamemtime(PluginTest):
    def setUp(self):
        PluginTest.setUp(self, pyfilenamemtime)

    def test_good_filenames(self):
        get_mtime = pyfilenamemtime.get_mtime
        for mem in (('foo-2011-10-23.txt', '2011-10-23-00-00'),
                    ('foo-2011-09-22-12-00.txt', '2011-09-22-12-00')):
            mtime = get_mtime(mem[0])
            print(mtime, mem[1])
            self.assertEqual(mtime_to_date(mtime), mem[1])
            
    def test_bad_filenames(self):
        get_mtime = pyfilenamemtime.get_mtime
        for mem in ('foo-2011.txt',
                    'foo-2011-10.txt',
                    'foo.txt'):
            self.assertEqual(get_mtime(mem[0]), None)
