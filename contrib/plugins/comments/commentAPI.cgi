#!/usr/bin/python

__author__ = "Ted Leung <twl@sauria.com>"
__version__ = "$Id:"
__copyright__ = "Copyright (c) 2003 Ted Leung"
__license__ = "Python"

import cgitb; cgitb.enable()
import cgi

import wingdbstub

import config, os, sys, time
from xml.dom.minidom import parseString

if __name__ == '__main__':
    from libs import tools
    from libs.entries.fileentry import FileEntry
    from libs.plugins.commentdecorator import writeComment
    from libs.Request import Request
    
    d = {}
    for mem in ["PATH_INFO", "SCRIPT_NAME", "REQUEST_METHOD", "HTTP_HOST", "QUERY_STRING", "REQUEST_URI", "HTTP_USER_AGENT", "REMOTE_ADDR"]:
        d[mem] = os.environ.get(mem, "")
    
    request = Request()
    request.addConfiguration(config.py)
    request.addHttp(d)    
    config = request.getConfiguration()
    data = request.getData()
    
    # import plugins
    import libs.plugins.__init__
    libs.plugins.__init__.initialize_plugins(config)
    
    # do start callback
    tools.run_callback("start", {'request': request}, mappingfunc=lambda x,y:y)

    # entryparser callback is runned first here to allow other plugins
    # register what file extensions can be used
    from libs.pyblosxom import PyBlosxom
    data['extensions'] = tools.run_callback("entryparser",
                                            {'txt': PyBlosxom.defaultEntryParser},
                                            mappingfunc=lambda x,y:y,
                                            defaultfunc=lambda x:x)
   
    registry = tools.get_registry()
    registry["request"] = request
    
    datadir = config['datadir']
    try:
        entry = FileEntry(config, datadir+d['PATH_INFO']+'.txt', datadir )
        data = {}
        data['entry_list'] = [ entry ]
       
        commentString = sys.stdin.read()
        commentDOM = parseString(commentString)
    
        def dictFromDOM(dom, dict, field):
            value = dom.getElementsByTagName(field)
            if len(value) == 1:
                dict[field] = value[0].firstChild.data
            else:
                dict[field] = ''

        cdict = {}
        dictFromDOM(commentDOM, cdict, 'title')
        dictFromDOM(commentDOM, cdict, 'author')
        dictFromDOM(commentDOM, cdict, 'link') 
        dictFromDOM(commentDOM, cdict, 'source')
        # force an integer data stamp -- not in keeping with RFC 822,
        # but neither is RSS Buddy
        cdict['pubDate'] = str(time.time())
#        dictFromDOM(commentDOM, cdict, 'pubDate')
        dictFromDOM(commentDOM, cdict, 'description')
            
        writeComment(config, data, cdict)

        print "Content-Type: text/plain\n"
        print "OK"
#        print d['REQUEST_URI']
#        print cdict
    except OSError:
        print "Content-Type: text/plain\n"
        print "An Error Occurred"
        pass


 