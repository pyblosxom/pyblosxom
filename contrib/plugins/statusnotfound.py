# vim: tabstop=4 shiftwidth=4 expandtab
"""
404 Error Generator

If there are no entries in the entryList, abort with 404 Error
"""
__author__ = "Wari Wahab pyblosxom@wari.per.sg"
__version__ = "$Id$"
def load(py, entryList):
    # Generate our own 404 Error
    if not entryList:
        print 'Status: 404 Not Found'
        print 'Content-Type: text/html\n'
        print 'The page you are looking for is not available:'
        print 'Back to <a href="%(base_url)s">%(blog_title)s</a>' % py
        raise SystemExit
