#!/usr/bin/env python2
# vim: shiftwidth=4 tabstop=4 expandtab
"""pyblosxom - xmlrpc access
Enables XMLRPC interface to pyblosxom (bloggerAPI)
"""
# Uncomment this if you put libs directory outside of pyblosxom.cgi
#import sys
#sys.path.append('/home/subtle/src/pyblosxom')
#
# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
import config, sys
from libs.pyblosxom  import PyBlosxom
from libs.XMLRPC import xmlrpcHandler

if __name__ == '__main__':
    p = PyBlosxom(config.py, config.xmlrpc, 1)
    p.startup()
    xmlrpcHandler(p.py, p.xmlrpc, sys.stdin.read()).process()
