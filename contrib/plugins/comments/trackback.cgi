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
    
try:
    import logging
except ImportError:    
    def log(str):
        pass
else:
    logger = logging.getLogger('trackback')
    hdlr = logging.FileHandler('/tmp/trackback.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)

    def log(str):
        logger.info(str)

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
    from Pyblosxom.pyblosxom import PyBlosxom

    request = Request()
    request.addConfiguration(config.py)
    p = PyBlosxom(request)
    p.startup()
    config, data = p.common_start(start_callbacks=0, render=0)
   
    datadir = config['datadir']
    
    # must be done after plugin initialization
    from comments import writeComment    
    try:
        path = os.path.join(datadir, d['PATH_INFO'][1:])
        ext = tools.what_ext(data['extensions'].keys(), path)
        entry = FileEntry(config, '%s.%s' % (path, ext), datadir )
        data = {}
        data['entry_list'] = [ entry ]
        writeComment(config, data, cdict)
        print tb_good_response
    except OSError:
        message = 'URI '+d['PATH_INFO']+" doesn't exist"
        log(message)
        print tb_bad_response % message
    
else:
    log(message)
    print tb_bad_response % message
