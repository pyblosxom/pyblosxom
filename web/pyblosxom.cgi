#!/usr/bin/env python
"""pyblosxom
A Bloxsom clone in python, see http://www.raelity.org/apps/blosxom/ for 
Blosxom details.
"""
# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
import config

# If the user defined a "codebase" property in their config file,
# then we insert that into our sys.path because that's where the
# PyBlosxom installation is.
if config.py.has_key("codebase"):
    import sys
    sys.path.insert(0, config.py["codebase"])

__author__ = 'Wari Wahab <wari@wari.per.sg>'
__version__ = config.py['pyblosxom_version']
__date__ = "$Date$"
__revision__ = "$Revision$"
__copyright__ = "Copyright (c) 2003-2004 Wari Wahab"
__license__ = "Python"

if __name__ == '__main__':
    from Pyblosxom.pyblosxom import Request, test_installation, PyBlosxom
    import os, sys

    req = Request()
    req.addConfiguration(config.py)

    d = {}
    for mem in ["HTTP_HOST", "HTTP_USER_AGENT", "HTTP_REFERER", "PATH_INFO", 
            "QUERY_STRING", "REMOTE_ADDR", "REQUEST_METHOD", "REQUEST_URI", 
            "SCRIPT_NAME", "HTTP_IF_NONE_MATCH", "HTTP_IF_MODIFIED_SINCE"]:
        d[mem] = os.environ.get(mem, "")
    req.addHttp(d)

    if not os.environ.get("REQUEST_METHOD", ""):
        if len(sys.argv) > 1 and sys.argv[1] == "--static":
            p = PyBlosxom(req)
            p.runStaticRenderer()
        else:
            test_installation(req)

    else:
        p = PyBlosxom(req)
        p.run()

# vim: shiftwidth=4 tabstop=4 expandtab
