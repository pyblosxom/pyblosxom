#!/usr/bin/python

"""
CommentAPI provides support for Joe Gregario's CommentAPI 
<http://wellformedweb.org/story/9>.   To use it, place it in a CGI directory
and make sure that it is mapped to a URI on your webserver.  Be sure that
you have comments.py installed

Then you must add the commentAPI tags to your RSS 2.0 feed.  The best way to
do this is to add an XML namespace declaration to the rss element:
    xmlns:wfw="http://wellformedweb.org/CommentAPI"
    
Then inside your RSS items you need to add a wfw:comment element:
    
    <wfw:comment>###commentAPI###/$file_path</wfw:comment>
    
    where ###commentAPI### is replaced by the URI that you mapped
    CommentAPI.cgi to.  At the moment, you need to map to a URI one level
    below the $base_url of the blog

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

from xml.parsers.expat import ExpatError
if __name__ == '__main__':
    # we don' take command line arguments
    if len(sys.argv) > 1:
        sys.exit("commentAPI.cgi expects to receive an RSS item on standard input")
    
    # copy the webserver environment into d
    d = {}
    for mem in ["HTTP_HOST", "HTTP_USER_AGENT", "HTTP_REFERER", "PATH_INFO", "QUERY_STRING", "REMOTE_ADDR", "REQUEST_METHOD", "REQUEST_URI", "SCRIPT_NAME"]:
        d[mem] = os.environ.get(mem, "")
    
    # setup the request, config and data for use
    from Pyblosxom import tools
    from Pyblosxom.entries.fileentry import FileEntry
    from Pyblosxom.Request import Request
    from Pyblosxom.pyblosxom import PyBlosxom
    request = Request()
    request.addConfiguration(config.py)
    request.addHttp(d)    

    p = PyBlosxom(request)
    p.startup()
    config, data = p.common_start(start_callbacks=0, render=0)
   
    datadir = config['datadir']
    try:
        path = d['PATH_INFO']
        if path == '':
            sys.exit("<html><body>CommentAPI.cgi expects to receive an RSS item on standard input</body></html>")
        # skip the first segment of the PATH
        # TODO: replace this with a $base_url type of rewrite.
        if len(path) > 0:
            path = path[1:]
            path = os.path.join(datadir, path)

        # path should represent a category URI which can be used to
        # locate the filentry containing the post to be commented on.
        # TODO: fix this os it works for Wari
        filename = ''
        ext = tools.what_ext(data['extensions'].keys(),path)
        filename = os.path.normpath('%s.%s' % (path, ext))
        # synthesize a file entry and put it on the entry list
        # TODO: I think this can be eliminated when we make the pyblosxom.py
        #       entry point in 0.8
        entry = FileEntry(config, filename, datadir )
        data = {}
        data['entry_list'] = [ entry ]
       
        # read the comment (an RSS item) from stdin
        # (it was POST'ed by the client)
        commentString = sys.stdin.read()
        if commentString == None:
            sys.exit("<html><body>CommentAPI expects to receive an RSS item on standard input</body></html>")
        try:
            commentDOM = parseString(commentString)
        except ExpatError, ee:
            sys.exit("<html><body>The RSS Item you supplied could not be parsed.\nThe error occured at line %d, column %d</body></html>" % (ee.lineno,ee.offset))
    
        def dictFromDOM(dom, data, field, default=''):
            """
            Fill in a field in dict with the content of a element in the dom

            TODO: epydoc
            """
            value = dom.getElementsByTagName(field)
            if len(value) == 1:
                data[field] = value[0].firstChild.data
            else:
                data[field] = default

        # use dictFromDOM to fill in a dict with the stuff in the comment
        cdict = {}
        dictFromDOM(commentDOM, cdict, 'title')
        dictFromDOM(commentDOM, cdict, 'author')
        dictFromDOM(commentDOM, cdict, 'link') 
        dictFromDOM(commentDOM, cdict, 'source')
        # force an integer data stamp -- not in keeping with RFC 822,
        # but neither is RSS 
        cdict['pubDate'] = str(time.time())
        dictFromDOM(commentDOM, cdict, 'description')
            
        # must be done after plugin initialization
        from comments import writeComment    
        # write the comment (in the dict)
        writeComment(config, data, cdict)

        print "Content-Type: text/plain\n"
        print "OK"
    except OSError:
        print "Content-Type: text/plain\n"
        print "An Error Occurred"
        pass


 
