#!/usr/bin/env python2
# vim: shiftwidth=4 tabstop=4 expandtab
"""pyblosxom - xmlrpc access
Enables XMLRPC interface to pyblosxom
"""
# Uncomment this if you put libs directory outside of pyblosxom.cgi
#import sys
#sys.path.append('/home/subtle/src/pyblosxom')

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
#import cgitb
#cgitb.enable()
import config, sys

if __name__ == '__main__':
    from libs.Request  import Request
    from libs.xmlrpc import xmlrpcHandler

    req = Request()
    req.addConfiguration(config.py)
    req.addConfiguration({'xmlrpc': config.xmlrpc})
    xmlrpcHandler(req, sys.stdin.read()).process()
