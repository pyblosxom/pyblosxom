#!/usr/bin/python

__author__ = "Ted Leung <twl@sauria.com>"
__version__ = "$Id:"
__copyright__ = "Copyright (c) 2003 Ted Leung"
__license__ = "Python"

import cgitb; cgitb.enable()
import cgi

import wingdbstub

import os, time
import config
    
tb_good_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>0</error>
</response>"""

tb_bad_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>1</error>
<message>%s</message>
</response>"""

d = {}
for mem in ["PATH_INFO", "SCRIPT_NAME", "REQUEST_METHOD", "HTTP_HOST", "QUERY_STRING", "REQUEST_URI", "HTTP_USER_AGENT", "REMOTE_ADDR","HTTP_ACCEPT"]:
    d[mem] = os.environ.get(mem, "")

form = cgi.FieldStorage()
       
print "Content-type: text/xml"
print

message = "not trackback"

if form.has_key("title") and form.has_key("excerpt") and form.has_key("url") and \
   form.has_key("blog_name"):
    cdict = { 'title': form['title'].value, \
              'author': 'Trackback from %s' % form['blog_name'].value, \
              'pubDate' : str(time.time()), \
              'link' : form['url'].value, \
              'source' : form['blog_name'].value, \
              'description' : form['excerpt'].value }
    from libs import tools
    from libs.entries.fileentry import FileEntry
    from libs.plugins.commentdecorator import writeComment
    from libs.Request import Request

    request = Request()
    request.addConfiguration(config.py)
    data = request.getData()
    import libs.entryparsers.__init__
    libs.entryparsers.__init__.initialize_extensions()
    data['extensions'] = libs.entryparsers.__init__.ext

    # import plugins
    import libs.plugins.__init__
    libs.plugins.__init__.initialize_plugins(config.py)
    
    registry = tools.get_registry()
    registry["request"] = request
    
    datadir = config.py['datadir']
    entry = FileEntry(config.py, datadir+d['PATH_INFO']+'.txt', datadir )
    data = {}
    data['entry_list'] = [ entry ]
    writeComment(config.py, data, cdict)
    
    print tb_good_response
else:
    print tb_bad_response % message
    
#print config.py
