#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (C) 2011 by the PyBlosxom team.  See AUTHORS.
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
This module has the code for handling crashes.

.. Note::

   This is a leaf node module!  It should never import other PyBlosxom
   modules or packages.
"""

import os
import pprint
import sys
import StringIO
import cgi
import traceback

_e = cgi.escape


class Response:
    """This is a minimal response that is returned by the crash
    handler.
    """
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

        self.seek = body.seek
        self.read = body.read


class CrashHandler:
    def __init__(self, httpresponse=False, environ=None):
        """
        :param httpresponse: boolean representing whether when
            handling a crash, we do http response headers
        """
        self.httpresponse = httpresponse

        if environ:
            self.environ = environ
        else:
            self.environ = {}

    def __call__(self, exc_type, exc_value, exc_tb):
        response = self.handle(exc_type, exc_value, exc_tb)
        if self.httpresponse:
            response.headers.append("Content-Length: %d" % httpresponse.body.len)
        sys.output.write("HTTP/1.0 %s\n" % response.status)
        for key, val in response.headers.items():
            sys.output.write("%s: %s\n" % (key, val))
        sys.output.write("\n")
        sys.output.write(response.body.read())
        sys.output.flush()

    def handle_by_response(self, exc_type, exc_value, exc_tb):
        """Returns a basic response object holding crash information
        for display.
        """
        headers = {}
        output = StringIO.StringIO()

        headers["Content-Type"] = "text/html"
        # FIXME - are there other userful headers?

        output.write("<html>")
        output.write("<title>HTTP 500: Server Error</title>")
        output.write("<body>")
        output.write("<h1>HTTP 500: Server Error</h1>")
        output.write("<p>A problem has occurred while PyBlosxom was "
                     "rendering this page.  Here is some useful information "
                     "to track down the root cause of the problem.</p>")
        try:
            import Pyblosxom.pyblosxom
            version = Pyblosxom.pyblosxom.VERSION
        except:
            version = "unknown"
        output.write("<p>Python version: %s" % _e(sys.version))
        output.write("<p>PyBlosxom version: %s</p>" % _e(version))

        output.write("<p>Error traceback:</p>")
        output.write("<pre>")
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        output.write(_e(tb))
        output.write("</pre>")

        output.write("<p>HTTP environment:</p>")
        output.write("<pre>")
        for key, val in self.environ.items():
            output.write("%s: %s\n" % (_e(repr(key)), _e(repr(val))))
        output.write("</pre>")

        output.write("</body>")
        output.write("</html>")

        headers["Content-Length"] = str(output.len)
        return Response("500 Server Error", headers, output)


def enable_excepthook(httpresponse=False):
    """This attaches the crashhandler to the sys.excepthook.
    This will handle any exceptions thrown that don't get
    handled anywhere else.

    If you're running PyBlosxom as a WSGI application or as a CGI
    script, you should create a CrashHandler instance and call
    handle_by_response.
    """
    sys.excepthook = CrashHandler(httpresponse=httpresponse)
