#!/usr/bin/env python

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

if __name__ == '__main__':
    import Pyblosxom.pyblosxom
    from Pyblosxom.pyblosxom import Request, test_installation, PyBlosxom
    import os, sys

    config.py["pyblosxom_name"] = "pyblosxom"
    config.py["pyblosxom_version"] = Pyblosxom.pyblosxom.VERSION_DATE

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
            if "--incremental" in sys.argv:
                incremental = 1
            else:
                incremental = 0
            p = PyBlosxom(req)
            p.runStaticRenderer(incremental)
        else:
            test_installation(req)

    else:
        p = PyBlosxom(req)
        p.run()

# vim: shiftwidth=4 tabstop=4 expandtab
