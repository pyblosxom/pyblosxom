import sys
import os
import time

from tests.helpers import UnitTestBase
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

class BlogTest(UnitTestBase):
    def get_datadir(self):
        tempdir = self.get_temp_dir()
        return os.path.join(tempdir, "datadir")
    
    def setup_blog(self, blist):
        datadir = self.get_datadir()
        for mem in blist:
            tools.create_entry(datadir,
                               mem["category"],
                               mem["filename"],
                               mem["mtime"],
                               mem["title"],
                               mem["metadata"],
                               mem["body"])

    def cleanup_blog(self):
        datadir = self.get_datadir()
        for root, dirs, files in os.walk(datadir, topdown=False):
            for name in files:
                print "removing %s" % (os.path.join(root, name))
                os.remove(os.path.join(root, name))

            for name in dirs:
                print "removing dir %s" % (os.path.join(root, name))
                os.rmdir(os.path.join(root, name))

        print "removing dir %s" % datadir
        os.rmdir(datadir)
    

class TestBlogTest(BlogTest):
    blog = [{"category": "cat1",
             "filename": "entry1.txt",
             "mtime": gen_time("2007/02/14 14:14"),
             "title": "Happy Valentine's Day!",
             "metadata": {},
             "body": "<p>Today is Valentine's Day!  w00t!</p>"}]

    def test_harness(self):
        tempdir = self.get_temp_dir()

        # this is kind of a bogus assert, but if we get this far
        # without raising an exception, then our test harness is
        # probably working.

        try:
            self.setup_blog(TestBlogTest.blog)
            self.eq_(1, 1)
        finally:
            self.cleanup_blog()
            self.eq_(1, 1)

