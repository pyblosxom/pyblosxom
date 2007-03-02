#!/usr/bin/env python

#!/path/to/python -u
# -u turns off character translation to allow transmission
# of gzip compressed content on Windows and OS/2

# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()

import os, sys

# this allows for a config.py override
script = os.environ.get('SCRIPT_FILENAME', None)
if script is not None:
    script = script[0:script.rfind("/")]
    sys.path.insert(0, script)

# this allows for grabbing the config based on the DocumentRoot
# setting if you're using apache
root = os.environ.get('DOCUMENT_ROOT', None)
if root is not None:
    sys.path.insert(0, root)

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
from config import py as cfg

# If the user defined a "codebase" property in their config file,
# then we insert that into our sys.path because that's where the
# PyBlosxom installation is.
if cfg.has_key("codebase"):
    sys.path.insert(0, cfg["codebase"])

from Pyblosxom.pyblosxom import PyBlosxom

if __name__ == '__main__':
    env = {}

    # names taken from wsgi instead of inventing something new
    env['wsgi.input'] = sys.stdin
    env['wsgi.errors'] = sys.stderr

    # setup url_scheme for static rendering
    if 'base_url' in cfg.keys():
        env['wsgi.url_scheme'] = cfg['base_url'][:cfg['base_url'].find("://")]
    else:
        env['wsgi.url_scheme'] = "http"

    if not os.environ.has_key("REQUEST_METHOD"):
        print "Please use pyblcmd for command-line functionality."
        sys.exit(0)

    try:
        # try running as a WSGI-CGI
        from wsgiref.handlers import CGIHandler
        from wsgi_app import application
        CGIHandler().run(application)

    except ImportError:
        # run as a regular CGI

        if os.environ.get("HTTPS") in ("yes", "on", "1"):
            env['wsgi.url_scheme'] = "https"

        for mem in ["HTTP_HOST", "HTTP_USER_AGENT", "HTTP_REFERER",
                    "PATH_INFO", "QUERY_STRING", "REMOTE_ADDR",
                    "REQUEST_METHOD", "REQUEST_URI", "SCRIPT_NAME",
                    "HTTP_IF_NONE_MATCH", "HTTP_IF_MODIFIED_SINCE",
                    "HTTP_COOKIE", "CONTENT_LENGTH", "CONTENT_TYPE",
                    "HTTP_ACCEPT", "HTTP_ACCEPT_ENCODING"]:
            env[mem] = os.environ.get(mem, "")

        p = PyBlosxom(cfg, env)

        p.run()
        response = p.getResponse()
        response.sendHeaders(sys.stdout)
        response.sendBody(sys.stdout)

# vim: shiftwidth=4 tabstop=4 expandtab
