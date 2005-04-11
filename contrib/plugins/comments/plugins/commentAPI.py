"""
Copyright (c) 2003-2005 Ted Leung

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

CommentAPI provides support for Joe Gregario's CommentAPI 
<http://wellformedweb.org/story/9>.   To use it, place it your plugins
directory and make sure that you define py['commentAPI_urltrigger'], which
is the URI to be used for talking to the commentAPI.  Be sure that
you have comments.py installed

You must also add the commentAPI tags to your RSS 2.0 feed.  The best way to
do this is to add an XML namespace declaration to the rss element:
    xmlns:wfw="http://wellformedweb.org/CommentAPI"
    
Then inside your RSS items you need to add a wfw:comment element:
    
    <wfw:comment>$base_url/###commentAPI###/$file_path</wfw:comment>
    
    where ###commentAPI### is the value of commentAPI_urltrigger

%<---------------------------------------------------------
py['commentAPI_urltrigger'] = "/commentAPI"
%<---------------------------------------------------------

"""
import os, os.path
from Pyblosxom import tools

def cb_start(args):
    request = args["request"]
    config = request.getConfiguration()
    logdir = config.get("logdir", "/tmp")
    logfile = os.path.normpath(logdir + os.sep + "commentAPI.log")

    tools.make_logger(logfile)

def verify_installation(request):
    config = request.getConfiguration()
    retval = 1

    # all config properties are optional
    if not config.has_key('commentAPI_urltrigger'):
        print("missing optional property: 'commentAPI_urltrigger'")

    return retval

def cb_handle(args):
    """

    @param args: a dict of plugin arguments
    @type args: dict
    """
    request = args['request']
    pyhttp = request.getHttp()
    config = request.getConfiguration()

    urltrigger = config.get('commentAPI_urltrigger','/commentAPI')

    path_info = pyhttp['PATH_INFO']
    if path_info.startswith(urltrigger):
        try:
            from Pyblosxom.entries.fileentry import FileEntry
            import os, sys
            pi = path_info.replace(urltrigger,'')
            if pi == '':
                sys.exit("<html><body>CommentAPI.cgi expects to receive an RSS item on standard input</body></html>")

            datadir = config['datadir']
            path = os.path.join(datadir, pi[1:])
            data = request.getData()
            filename = ''
            ext = tools.what_ext(data['extensions'].keys(),path)
            filename = os.path.normpath('%s.%s' % (path, ext))
            entry = FileEntry(request, filename, datadir )
            data = {}
            data['entry_list'] = [ entry ]

            commentString = sys.stdin.read()
            if commentString == None:
                sys.exit("<html><body>CommentAPI expects to receive an RSS item on standard input</body></html>")
            try:
                from xml.dom.minidom import parseString
                from xml.parsers.expat import ExpatError
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
            import time
            cdict['pubDate'] = str(time.time())
            dictFromDOM(commentDOM, cdict, 'description')

            # must be done after plugin initialization
            from comments import writeComment    
            # write the comment (in the dict)
            writeComment(request, config, data, cdict, config['blog_encoding'])

            print "Content-Type: text/plain\n"
            print "OK"
        except OSError:
            print "Content-Type: text/plain\n"
            print "An Error Occurred"
        return 1
    else:
        return 0
