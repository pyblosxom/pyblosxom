from Pyblosxom.tests.test_backwards_compatibility import *
from Pyblosxom.tests.test_blog import *
from Pyblosxom.tests.test_entries import *
from Pyblosxom.tests.test_pathinfo import *
from Pyblosxom.tests.test_tools import *

import unittest
import os

def get_suite():
    names = os.listdir(os.path.dirname(__file__))
    names = ["Pyblosxom.tests.%s" % m[:-3]
             for m in names
             if m.startswith("test_") and m.endswith(".py")]
    suite = unittest.TestLoader().loadTestsFromNames(names)
    return suite

def main():
    unittest.TextTestRunner().run(get_suite())

if __name__ == "__main__":
    main()
