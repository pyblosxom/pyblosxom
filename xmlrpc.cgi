#!/usr/bin/env python2
# vim: shiftwidth=4 tabstop=4 expandtab
"""pyblosxom - xmlrpc access
Enables XMLRPC interface to pyblosxom
"""
# Uncomment this if you put libs directory outside of xmlrpc.cgi
#import sys
#sys.path.append('/home/wari/pyblosxom')

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
import config, sys, os, xmlrpclib

# 10Kb should be enough for most documents
MAXREQUEST_LENGTH = config.xmlrpc.get('maxrequest_length', 10000) 

if __name__ == '__main__':
    try:
        contentLength = int(os.environ["CONTENT_LENGTH"])
        if contentLength > MAXREQUEST_LENGTH:
            raise ValueError, 'Request too large - %s bytes' % contentLength
    except:
        response = xmlrpclib.dumps(xmlrpclib.Fault(1, "%s: %s" % sys.exc_info()[:2]))
        print 'Content-type: text/xml'
        print 'Content-length: %s' % len(response)
        print
        print response
    else:
        from libs.Request  import Request
        from libs.xmlrpc import xmlrpcHandler

        data = sys.stdin.read(contentLength)
        req = Request()
        req.addConfiguration(config.py)
        req.addConfiguration({'xmlrpc': config.xmlrpc})
        xmlrpcHandler(req, data).process()
