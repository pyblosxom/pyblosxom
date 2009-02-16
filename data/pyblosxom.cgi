#!/usr/bin/env python

# -u turns off character translation to allow transmission
# of gzip compressed content on Windows and OS/2
#!/path/to/python -u

# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()


# Don't touch anything below this line
# --------------------------------------------------

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

    # if there's no REQUEST_METHOD, then this is being run on the
    # command line and we should execute the command_line_handler.
    if not os.environ.has_key("REQUEST_METHOD"):
        from Pyblosxom.pyblosxom import command_line_handler

        args = sys.argv[1:]

        if len(args) == 0:
            args = ["--test"]

        sys.exit(command_line_handler("pyblosxom.cgi", args))


    # names taken from wsgi instead of inventing something new
    env['wsgi.input'] = sys.stdin
    env['wsgi.errors'] = sys.stderr

    # figure out what the protocol is for the wsgi.url_scheme property.
    # we look at the base_url first and if there's nothing set there,
    # we look at environ.
    if 'base_url' in cfg.keys():
        env['wsgi.url_scheme'] = cfg['base_url'][:cfg['base_url'].find("://")]

    else:
        if os.environ.get("HTTPS", "off") in ("on", "1"):
            env["wsgi.url_scheme"] = "https"

        else:
            env['wsgi.url_scheme'] = "http"

    try:
        # try running as a WSGI-CGI
        from wsgiref.handlers import CGIHandler
        from Pyblosxom.pyblosxom import PyBlosxomWSGIApp
        CGIHandler().run(PyBlosxomWSGIApp())

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
