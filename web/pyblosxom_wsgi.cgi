#!/usr/bin/env python

#!/path/to/python -u
# -u turns off character translation to allow transmission
# of gzip compressed content on Windows and OS/2

# This is a WSGI version of pyblosxom.cgi.
# If you have the wsgiref library installed you can use this
# instead of the vanilla pyblosxom.cgi.
# This is primarily interesting for testing and as a proof-of-concept.

# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()

import sys
import os

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
from config import py as cfg

# If the user defined a "codebase" property in their config file,
# then we insert that into our sys.path because that's where the
# PyBlosxom installation is.
if cfg.has_key("codebase"):
    sys.path.insert(0, cfg["codebase"])


if __name__ == '__main__':

    if not os.environ.get("REQUEST_METHOD", ""):

        ### Install verification & static rendering

        from Pyblosxom.pyblosxom import PyBlosxom
        
        env = {}
        # names taken from wsgi instead of inventing something new
        env['wsgi.input'] = sys.stdin
        env['wsgi.errors'] = sys.stderr
        # setup url_scheme for static rendering.
        if 'base_url' in cfg:
            env['wsgi.url_scheme'] = cfg['base_url'][:cfg['base_url'].find("://")]
        else:
            env['wsgi.url_scheme'] = "http"            
    
        p = PyBlosxom(cfg, env)

        if len(sys.argv) > 1 and sys.argv[1] == "--static":
            if "--incremental" in sys.argv:
                incremental = 1
            else:
                incremental = 0
            p.runStaticRenderer(incremental)
        else:
            p.testInstallation()

    else:

        ### Run as WSGI-CGI

        from wsgiref.handlers import CGIHandler
        from wsgi_app import application

        CGIHandler().run(application)


# vim: shiftwidth=4 tabstop=4 expandtab
