#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################
import os
import unittest
import traceback
import plugins.tests

def has_get_test_suite(filename):
    if "testrunner" in filename:
        return False
    try:
        pointer = open(filename, "r")
    except (IOError, OSError):
        return False

    for line in pointer:
        if "get_test_suite" in line:
            pointer.close()
            return True

    pointer.close()
    return False

def get_import_path(basedir, path):
    path = path[len(basedir)+1:]
    
    path = path.replace(os.sep, ".")
    if path.endswith(".py"):
        path = path[:-3]

    return path

def import_module(path):
    try:
        module = __import__(path)
        for c in path.split(".")[1:]:
            module = getattr(module, c)
                
        return module
    except ImportError:
        print "ImportError: Couldn't import %s" % path
        print "".join(traceback.format_exc())
        return
    except StandardError:
        print "Couldn't import %s" % path
        print "".join(traceback.format_exc())
        return

def get_test_suites(testdir):
    suites = []
    
    for root, dirs, files in os.walk(testdir):
        if root == testdir:
            continue

        for file_ in files:
            if file_.startswith("_") or not file_.endswith(".py"):
                continue

            filename = os.path.join(root, file_)
            if not has_get_test_suite(filename):
                continue

            path = get_import_path(os.path.dirname(testdir), filename)
            module = import_module(path)
            if not module:
                continue

            try:
                suite = getattr(module, "get_test_suite")()
            except StandardError:
                print "Error calling get_test_suite() on %s" % path
                print "".join(traceback.format_exc())
                continue

            suites.append(suite)
    return suites

def get_suite():
    testdir = os.path.abspath(os.path.dirname(__file__))
    suites = get_test_suites(testdir)

    suites.append(unittest.TestLoader().loadTestsFromModule(plugins.tests))
    test_suite = unittest.TestSuite(suites)
    return test_suite

def main():
    unittest.TextTestRunner(verbosity=2).run(get_suite())

if __name__ == "__main__":
    main()
