import sys, os

try:
    import Pyblosxom
except ImportError:
    testdir = os.path.join(os.path.dirname(__file__), "../../")
    sys.path.insert(0, testdir)
