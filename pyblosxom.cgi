#!/usr/bin/env python2
# vim: shiftwidth=4 tabstop=4 expandtab
"""pyblosxom
A Bloxsom clone in python, see http://www.raelity.org/apps/blosxom/ for details
"""
import os, cgi, sys
from libs.pyblosxom import PyBlosxom
# Uncomment this if you put libs directory outside of pyblosxom.cgi
#sys.path.append('/path/to/libs/directory')
# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()

# Windows INI style file to read to override the values below
configFile = '../../p.ini'

py = {}
# What's this blog's title?
py['blog_title'] = "Another pyblosxom blog"

# What's this blog's description (for outgoing RSS feed)?
py['blog_description'] = "blosxom with a touch of python"

# What's this blog's primary language (for outgoing RSS feed)?
py['blog_language'] = "en"

# Where are this blog's entries kept?
py['datadir'] = "/path/to/blog"

# Should I stick only to the datadir for items or travel down the directory
# hierarchy looking for items?  If so, to what depth?
# 0 = infinite depth (aka grab everything), 1 = datadir only, n = n levels down
py['depth'] = 0

# How many entries should I show on the home page?
py['num_entries'] = 40

# Trackback data directory (If you install Standalone Trackback Tool)
py['tb_data'] = '/path/to/tb_data/directory'

# Default parser/preformatter. Defaults to plain (does nothing)
py['parser'] = 'plain'

# Enable Caching? Depends on your directory permissions and whether you use
# preformatters
py['cache_enable'] = 0

# Cached file extension.
py['cache_ext'] = '.compiled'

# XML-RPC data
trackback = {}
# enable XML-RPC interface? Default no. Use 1 to enable
trackback['enable'] = 1
trackback['path'] = '/trackback'

# XML-RPC data
xmlrpc = {}
# enable XML-RPC interface? Default no. Use 1 to enable
xmlrpc['enable'] = 0
# Username to access this server
xmlrpc['username'] = 'someusername'
# Password to access this server
xmlrpc['password'] = 'somepassword'
# Path call that activates XML-RPC mode
xmlrpc['path'] = '/RPC2'

# ------------ Nothing to change here --------------- #
__author__ = 'Wari Wahab <wari@wari.per.sg>'
__version__ = "0+5i_rev3"
__date__ = "$Date$"
__revision__ = "$Revision$"
__copyright__ = "Copyright (c) 2002 Wari Wahab"
__license__ = "Python"
py['pyblosxom_version'] = __version__
py['pyblosxom_name'] = 'pyblosxom'

# Override default configurations
if os.path.isfile(configFile):
    import ConfigParser
    cp = ConfigParser.ConfigParser()
    cp.read(configFile)
    if cp.has_section('pyblosxom'):
        for key in cp.options('pyblosxom'):
            py[key] = cp.get('pyblosxom', key).strip()
    if cp.has_section('xmlrpc'):
        for key in cp.options('xmlrpc'):
            xmlrpc[key] = cp.get('xmlrpc', key).strip()

p = PyBlosxom(py, xmlrpc)
p.startup()

if __name__ == '__main__':
    path_info = os.environ.get('PATH_INFO','')
    if  path_info != xmlrpc['path']: 
        p.run()
    else:
        if not int(xmlrpc['enable']): 
            p.run()
        # XML-RPC, starts here
        from libs.XMLRPC import xmlrpcHandler
        xmlrpcHandler(p.py, p.xmlrpc, sys.stdin.read()).process()
