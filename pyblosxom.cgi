#!/usr/bin/env python2
# vim: shiftwidth=4 tabstop=4 expandtab
"""pyblosxom
A Bloxsom clone in python, see http://www.raelity.org/apps/blosxom/ for details
"""
# Uncomment this if you put libs directory outside of pyblosxom.cgi
#import sys
#sys.path.append('/path/to/libs/directory')
# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
import config

__author__ = 'Wari Wahab <wari@wari.per.sg>'
__version__ = config.py['pyblosxom_version']
__date__ = "$Date$"
__revision__ = "$Revision$"
__copyright__ = "Copyright (c) 2003 Wari Wahab"
__license__ = "Python"

if __name__ == '__main__':
    from libs.pyblosxom import PyBlosxom
    from libs.Request import Request
    import os, cgi

    req = Request()
    req.addConfiguration(config.py)

    d = {}
    for mem in ["PATH_INFO", "SCRIPT_NAME", "REQUEST_METHOD", "HTTP_HOST", "QUERY_STRING", "REQUEST_URI", "HTTP_USER_AGENT", "REMOTE_ADDR"]:
        d[mem] = os.environ.get(mem, "")
    req.addHttp(d)

    req.addHttp({"form": cgi.FieldStorage()})

    p = PyBlosxom(req)
    p.startup()
    p.run()
