#!/usr/bin/python

"""
CommentAPI provides support for Joe Gregario's CommentAPI 
<http://wellformedweb.org./story/9>.   To use it, place it in a CGI directory
and make sure that it is mapped to a URI on your webserver.

Then you must add the commentAPI tags to your RSS 2.0 feed.  The best way to
do this is to add an XML namespace declaration to the rss element:
    xmlns:wfw="http://wellformedweb.org/CommentAPI"
    
Then inside your RSS items you need to add a wfw:comment element:
    
    <wfw:comment>###commentAPI###/$file_path</wfw:comment>
    
    where ###commentAPI### is replaced by the URI that you mapped CommentAPI.cgi to

"""

__author__ = "Ted Leung <twl@sauria.com>"
__version__ = "$Id:"
__copyright__ = "Copyright (c) 2003 Ted Leung"
__license__ = "Python"

import cgitb; cgitb.enable()
import cgi

#import wingdbstub

import config, os, sys, time
from xml.dom.minidom import parseString

if __name__ == '__main__':
    from Pyblosxom import tools
    from Pyblosxom.entries.fileentry import FileEntry
    from Pyblosxom.Request import Request
    
    d = {}
    for mem in ["HTTP_HOST", "HTTP_USER_AGENT", "HTTP_REFERER", "PATH_INFO", "QUERY_STRING", "REMOTE_ADDR", "REQUEST_METHOD", "REQUEST_URI", "SCRIPT_NAME"]:
        d[mem] = os.environ.get(mem, "")
    
    request = Request()
    request.addConfiguration(config.py)
    request.addHttp(d)    
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
    data['extensions'] = tools.run_callback("entryparser",
                                            {'txt': PyBlosxom.defaultEntryParser},
                                            mappingfunc=lambda x,y:y,
                                            defaultfunc=lambda x:x)
   
    registry = tools.get_registry()
    registry["request"] = request
    
    datadir = config['datadir']
    try:
        path = d['PATH_INFO']
        if len(path) > 0:
            path = path[1:]
        filename = ''
        for ext in data['extensions'].keys():
            if os.path.isfile(os.path.join(datadir,path + '.' + ext)):
                filename = os.path.join(datadir,os.path.normpath('%s.%s' % (path, ext)))
                break 
        entry = FileEntry(config, filename, datadir )
        data = {}
        data['entry_list'] = [ entry ]
       
        commentString = sys.stdin.read()
        commentDOM = parseString(commentString)
    
        def dictFromDOM(dom, data, field, default=''):
            value = dom.getElementsByTagName(field)
            if len(value) == 1:
                data[field] = value[0].firstChild.data
            else:
                data[field] = default

        cdict = {}
        dictFromDOM(commentDOM, cdict, 'title')
        dictFromDOM(commentDOM, cdict, 'author')
        dictFromDOM(commentDOM, cdict, 'link') 
        dictFromDOM(commentDOM, cdict, 'source')
        # force an integer data stamp -- not in keeping with RFC 822,
        # but neither is RSS Buddy
        cdict['pubDate'] = str(time.time())
        dictFromDOM(commentDOM, cdict, 'description')
            
        writeComment(config, data, cdict)

        print "Content-Type: text/plain\n"
        print "OK"
    except OSError:
        print "Content-Type: text/plain\n"
        print "An Error Occurred"
        pass


 
