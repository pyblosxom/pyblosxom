#!/usr/bin/env python2
# vim: shiftwidth=4 tabstop=4 expandtab
"""An error 404 page handler
This is a helper for pyblosxom, see:
http://roughingit.subtlehints.net/py_stuff/weblogs/hacks/Half_Baked_and_a_Mostly_Fried.html
for details
"""
# Windows INI style file to read to override the values below
configFile = '../../p.ini'

# Essential data stuff
archiveRoot = '/py_stuff'
docRoot = 'py_stuff'
pyblosxomScriptPath = '/pyblosxom'
hostName = 'roughingit.subtlehints.net'

py = {}
xmlrpc = {}

# ------------ Nothing to change here --------------- #
__author__ = 'Wari Wahab <wari@wari.per.sg>'
__version__ = "0+5i_rev1"
__copyright__ = "Copyright (c) 2002 Wari Wahab"
__license__ = "Python"
py['pyblosxom_version'] = __version__
py['pyblosxom_name'] = 'pyblosxom'

import os, ConfigParser, cgi, sys, traceback, re
from StringIO import StringIO
from libs.pyblosxom import PyBlosxom

# Read Configuration from file
if os.path.isfile(configFile):
    cp = ConfigParser.ConfigParser()
    cp.read(configFile)
    if cp.has_section('pyblosxom'):
        for key in cp.options('pyblosxom'):
            py[key] = cp.get('pyblosxom', key).strip()
    if cp.has_section('xmlrpc'):
        for key in cp.options('xmlrpc'):
            xmlrpc[key] = cp.get('xmlrpc', key).strip()

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
    # Now we disect the document and remove the first two lines
    data = document.split('\n')
    file(filename, "w").write('\n'.join(data[4:]))

if __name__ == '__main__':
    try:
        redir = os.environ.get('REDIRECT_URI', '')
        if redir == '':
            redir = os.environ.get('REDIRECT_URL', '')
        pathInfo = re.sub(archiveRoot, '', redir)
        realfile = py['datadir'] + re.sub('.html', '.txt', pathInfo)
        if re.match(archiveRoot, redir) and os.path.exists(realfile):
            stdout = sys.stdout
            sys.stdout = StringIO()
            os.environ['PATH_INFO'] = pathInfo
            os.environ['SCRIPT_NAME'] = pyblosxomScriptPath
            os.environ['HTTP_HOST'] = hostName
            p = PyBlosxom(py, xmlrpc)
            p.startup()
            p.run()
            data = sys.stdout.getvalue()
            sys.stdout = stdout
            saveData(docRoot + pathInfo, data)
            sys.exit()
            
        else:
            print "Content-Type: text/html\n"
            print "Error: Page not found, proceed to <a href=/>RoughingIT</a><br />\n"

    except Exception, errmessage:
        (tbtype, value, tb) = sys.exc_info()
        if tbtype == SystemExit:
            raise tbtype, value
        else:
            print "Content-Type: text/html\n"
            print "<pre>"
            traceback.print_tb(tb)
            print tbtype, value
            print "</pre>"
            del tb
            sys.exit(1)
