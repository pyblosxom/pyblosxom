#!/usr/bin/python

__author__ = "Ted Leung <twl@sauria.com>"
__version__ = "$Id:"
__copyright__ = "Copyright (c) 2003 Ted Leung"
__license__ = "Python"

import cgitb; cgitb.enable()
import cgi

#import wingdbstub

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
for mem in ["HTTP_HOST", "HTTP_USER_AGENT", "HTTP_REFERER", "PATH_INFO", "QUERY_STRING", "REMOTE_ADDR", "REQUEST_METHOD", "REQUEST_URI", "SCRIPT_NAME"]:
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
    from Pyblosxom import tools
    from Pyblosxom.entries.fileentry import FileEntry
    from Pyblosxom.Request import Request

    request = Request()
    request.addConfiguration(config.py)
    config = request.getConfiguration()
    data = request.getData()

    # import plugins
    import Pyblosxom.plugin_utils
    Pyblosxom.plugin_utils.initialize_plugins(config)
    
    # must be done after plugin initialization
    from comments import writeComment

    # do start callback
    tools.run_callback("start", {'request': request}, mappingfunc=lambda x,y:y)

    # entryparser callback is runned first here to allow other plugins
    # register what file extensions can be used
    from Pyblosxom.pyblosxom import PyBlosxom

    p = PyBlosxom(request)
    p.startup()

    data['extensions'] = tools.run_callback("entryparser",
                                            {'txt': p.defaultEntryParser},
                                            mappingfunc=lambda x,y:y,
                                            defaultfunc=lambda x:x)
   
    registry = tools.get_registry()
    registry["request"] = request
    
    datadir = config['datadir']
    try:
        entry = FileEntry(config, datadir+d['PATH_INFO']+'.txt', datadir )
        data = {}
        data['entry_list'] = [ entry ]
        writeComment(config, data, cdict)
        print tb_good_response
    except OSError:
        message = 'URI '+d['PATH_INFO']+" doesn't exist"
        print tb_bad_response % message
    
else:
    print tb_bad_response % message
