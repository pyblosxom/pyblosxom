#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

import unittest
import os

def get_suite():
    names = os.listdir(os.path.dirname(__file__))
    names = ["Pyblosxom.tests.%s" % m[:-3]
             for m in names
             if m.startswith("test_") and m.endswith(".py")]
    suite = unittest.TestLoader().loadTestsFromNames(names)
    return suite

test_suite = get_suite()

def main():
    unittest.TextTestRunner().run(test_suite)

if __name__ == "__main__":
    main()
