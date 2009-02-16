import _path_pyblosxom

import sys
import os
import time

from Pyblosxom import tools

def gen_time(s):
    """
    Takes a string in YYYY/MM/DD hh:mm format and converts it to
    a float of seconds since the epoch.

    For example:
   
    >>> gen_time("2007/02/14 14:14")
    1171480440.0
    """
    return time.mktime(time.strptime(s, "%Y/%m/%d %H:%M"))

blog1 = [ { "category": "cat1",
            "filename": "entry1.txt",
            "mtime": gen_time("2007/02/14 14:14"),
            "title": "Happy Valentine's Day!",
            "metadata": { },
            "body": "<p>Today is Valentine's Day!  w00t!</p>" } ]

datadir = os.path.normpath(os.path.join(os.path.dirname(__file__), "../testgen"))

def setupblog(blist):
    for mem in blist:
        tools.create_entry(datadir,
                           mem["category"],
                           mem["filename"],
                           mem["mtime"],
                           mem["title"],
                           mem["metadata"],
                           mem["body"])

def cleanupblog():
   for root, dirs, files in os.walk(datadir, topdown=False):
       for name in files:
           print "removing %s" % (os.path.join(root, name))
           os.remove(os.path.join(root, name))

       for name in dirs:
           print "removing dir %s" % (os.path.join(root, name))
           os.rmdir(os.path.join(root, name))

   print "removing dir %s" % datadir
   os.rmdir(datadir)


class TestSetup:
   def test_harness(self):
       try:
           setupblog(blog1)

       finally:
           cleanupblog()

       # this is kind of a bogus assert, but if we get this far
       # without raising an exception, then our test harness is
       # probably working.
       assert 1 == 1
