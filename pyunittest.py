"""
This module uses the Python unittest framework to unittest various
pieces inside of Python--mostly stuff that's standalone in the 
tools module.
"""
# we kind of assume this is being run in ./pyblosxom/
import sys, unittest
# sys.path.insert(0, "./")

from Pyblosxom import tools
from Pyblosxom.pyblosxom import Request

class TestLocking(unittest.TestCase):
    def testLocking(self):
        """
        req = Request()
        req.addConfiguration( { "datadir": "./" } )

        # get a lock
        self.failUnlessEqual(tools.get_lock(req, "testlock"), 1)
        # get the same lock again (should fail)
        self.failUnlessEqual(tools.get_lock(req, "testlock"), 0)
        # return the lcok
        self.failUnlessEqual(tools.return_lock(req, "testlock"), None)
        # get the same lock again (should succeed)
        self.failUnlessEqual(tools.get_lock(req, "testlock"), 1)
        """
        # FIXME - this needs to be re-written
        

# need test cases for Pyblosxom/tools.VAR_REGEXP

# need test cases for Pyblosxom/tools.Stripper

# need test cases for Pyblosxom/tools.Replacer

# need test cases for Pyblosxom/tools.parse

if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))

# vim: tabstop=4 shiftwidth=4 expandtab
