#!/usr/bin/env python2
# vim: shiftwidth=4 tabstop=4 expandtab
"""An error 404 page handler
This is a helper for pyblosxom, see:
    http://roughingit.subtlehints.net/py_stuff/weblogs/hacks/Half_Baked_and_a_Mostly_Fried.html
    for details
"""
# Uncomment this to look for libs/ directory elsewhere
#sys.path.append('/path/to/pyblosxom/installation/dir')
# Uncomment to debug (May not work due to buffering)
#import cgitb; cgitb.enable()
import os, cgi, sys, traceback, re
import config

# Essential data stuff - Edit this for site specific information
archiveRoot = '/myblog'
docRoot = 'myblog'
pyblosxomScriptPath = '/cgi-bin/pyblosxom.cgi'
hostName = 'www.example.com'

py = config.py

# ------------ Nothing to change here --------------- #
__author__ = 'Wari Wahab <wari@wari.per.sg>'
__version__ = config.__version__
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2002 Wari Wahab"
__license__ = "Python"
py['pyblosxom_version'] = __version__
py['pyblosxom_name'] = 'pyblosxom'

x
from StringIO import StringIO
from libs.pyblosxom import PyBlosxom

def makepath(path):
    """
    from holger@trillke.net 2002/03/18
    """
    from os import makedirs
    from os.path import normpath,dirname,exists,abspath
    dpath = normpath(dirname(path))
    if not exists(dpath): makedirs(dpath)
    return normpath(abspath(path))

def saveData(filename, document):
    makepath(filename)
    print document
    # Now we disect the document and remove the first few lines
    data = document.split('\n')
    line = data.pop(0)
    while line != '':
        if line == 'Status: 404 Not Found':
            return
        line = data.pop(0)
    file(filename, "w").write('\n'.join(data))

if __name__ == '__main__':
    redir = os.environ.get('REDIRECT_URI', '')
    if redir == '':
        redir = os.environ.get('REDIRECT_URL', '')
    pathInfo = re.sub(archiveRoot, '', redir)
    if redir.startswith(archiveRoot):
        stdout = sys.stdout
        sys.stdout = StringIO()
        os.environ['PATH_INFO'] = pathInfo
        os.environ['SCRIPT_NAME'] = pyblosxomScriptPath
        os.environ['HTTP_HOST'] = hostName
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
        data = sys.stdout.getvalue()
        sys.stdout = stdout
        saveData(docRoot + pathInfo, data)
        sys.exit()
        
    else:
        print "Error: 404\nContent-Type: text/html\n"
        print "Error: Page not found, proceed to <a href=/>RoughingIT</a><br />\n"
