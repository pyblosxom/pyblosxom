#!/usr/bin/env python

#!/path/to/python -u
# -u turns off character translation to allow transmission
# of gzip compressed content on Windows and OS/2

# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
from config import py as cfg

import os
import sys

# If the user defined a "codebase" property in their config file,
# then we insert that into our sys.path because that's where the
# PyBlosxom installation is.
if cfg.has_key("codebase"):
    sys.path.insert(0, cfg["codebase"])

from Pyblosxom.pyblosxom import PyBlosxom


if __name__ == '__main__':

    # create default environment. 
    # this is shared among the different ways to start Pyblosxom.
    env = {}
    # names taken from wsgi instead of inventing something new
    env['wsgi.input'] = sys.stdin
    env['wsgi.errors'] = sys.stderr
    # setup url_scheme for static rendering.
    if 'base_url' in cfg:
        env['wsgi.url_scheme'] = cfg['base_url'][:cfg['base_url'].find("://")]
    else:
        env['wsgi.url_scheme'] = "http"            

    if not os.environ.get("REQUEST_METHOD", ""):

        ### Install verification & static rendering

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

        try:

            ### Run as WSGI-CGI

            from wsgiref.handlers import CGIHandler
            from wsgi_app import application
            CGIHandler().run(application)

        except ImportError:

            ### Run as plain vanilla CGI

            # finish setting up the environment
            if os.environ.get("HTTPS") in ('yes','on','1'):
                env['wsgi.url_scheme'] = "https"
            for mem in ["HTTP_HOST", "HTTP_USER_AGENT", "HTTP_REFERER", "PATH_INFO", 
                    "QUERY_STRING", "REMOTE_ADDR", "REQUEST_METHOD", "REQUEST_URI", 
                    "SCRIPT_NAME", "HTTP_IF_NONE_MATCH", "HTTP_IF_MODIFIED_SINCE",
                    "HTTP_COOKIE", "CONTENT_LENGTH", "HTTP_ACCEPT", "HTTP_ACCEPT_ENCODING"]:
                env[mem] = os.environ.get(mem, "")
            
            # handle the request
            p = PyBlosxom(cfg, env)
            p.run()
            response = p.getResponse()
            response.sendHeaders(sys.stdout)
            response.sendBody(sys.stdout)


# vim: shiftwidth=4 tabstop=4 expandtab
