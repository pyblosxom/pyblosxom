#
# Comment poster
#

import cgi, glob, os.path, string, time
from libs import tools
from libs.entries.base import EntryBase

    
"""
This module contains an extension to Blosxom file entries to support comments
"""

class CommentDecorator(EntryBase):
    """
    This class supports comments stored in files
    """
    
    def __init__(self, entryob):
        EntryBase.__init__(self)
        self._child = entryob
        self._comments = 0
        
    def getMetadata(self, key, default=None):
        """
        We add comment data to the data for a file entry.  
        Comment data is only computed if it's referenced 
        """
        if key == 'num_comments':
            self.countComments()
        if key == 'comments' and not self._comments:
            self.getComments()
        return self._child.getMetadata(key, default)
    
    def getData(self):
        return self._child.getData()
        
    def has_key(self, key):
        """
        Has key is needed because we want to check and see if an entry has comments
        """
        if key == 'num_comments':
            self.countComments()
        if key =='comments' and not self._comments:
            self.getComments()
        return self._child.has_key(key)
    
    def setData(self, data):
        self._child.setData(data)

    def setMetadata(self, key, value):
        self._child.setMetadata(key, value)

    def getMetadataKeys(self):
        return self._child.getMetadataKeys()
    
  
    def getComments(self):
        """
        Get the comments for this entry and stick them in 'comments' as a list
        Also compute a count and stick this in 'num_comments'
        """
        cmts = readComments(self)
        self._comments = 1
        self['comments'] = cmts
        self['num_comments'] = len(cmts)
        
    def countComments(self):
        """
        Compute the number of comments for this entry an stick it in 'num_comments'
        """

        self['num_comments'] = getCommentCount(self)

#
# file system  implementation
# Comments are stored 1 per file, in a parallel hierarchy to the datadir hierarchy
# The filename of the comment is the filename of the blog entry plus the creation
# time of the comment as a time float.
# The contents of the comment file is an RSS 2.0 item
#        
        
def readComments(entry):
    """
    @param: a file entry
    @type: dict
    
    @returns: a list of comment dicts
    """
    filelist = glob.glob(cmtExpr(entry))
    filelist.sort()
    return [ readComment(f) for f in filelist ]
    
def getCommentCount(entry):
    """
    @param: a file entry
    @type: dict
    
    @returns: the number of comments for the entry
    """
    if entry['absolute_path'] == None: return 0
    filelist = glob.glob(cmtExpr(entry))
    return len(filelist)

def cmtDir(entry):
    """
    @param: a file entry
    @type: dict
    
    @returns: a string with the directory path for the comment
    """
    cmtDir = entry['datadir']+'/'+entry['comment_dir']+'/'+entry['absolute_path']
    return cmtDir

def cmtExpr(entry):
    """
    Return a string containing the regular expression for comment entries
    
    @returns: a string containing the regular expression for comment entries
    """
    
    cmtExpr = cmtDir(entry)+'/'+entry['fn']+'-*.'+entry['comment_ext']
    return cmtExpr

    
def readComment(filename):
    """
    Read a comment from filename
    
    @param: filename containing a comment
    @type: string
    
    @returns: a comment dict
    """
    
    from xml.sax import saxutils, make_parser, SAXException
    from xml.sax.handler import feature_namespaces
    class cmtHandler(saxutils.DefaultHandler):
        def __init__(self, cmt):
            self._data = ""
        def startElement(self, name, atts):
            self._data = ""
        def endElement(self, name):
            cmt['cmt_'+name] = self._data
        def characters(self, content):
            self._data += content

    cmt = {}
    
    try:
        story = file(filename)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        handler = cmtHandler(cmt)
        parser.setContentHandler(handler)
        parser.parse(story)
        story.close()
        cmt['cmt_time'] = cmt['cmt_pubDate'] # timestamp as float for comment anchor
        cmt['cmt_pubDate'] = time.ctime(float(cmt['cmt_pubDate']))
    except SAXException, se:
        story.close()
    except: 
        story.close()
    return cmt

def writeComment(config, data, comment):
    """
    Write a comment
    
    @param: dict containing pyblosxom config info
    @type: dict
    
    @param: dict containing entry info
    @type: dict
    
    @param: dict containing comment info
    @type: dict
    """
    entry = data['entry_list'][0]
    datadir = config['datadir']
    cdir = datadir+'/'+config['comment_dir']+'/'+entry['absolute_path']
    cdir = os.path.normpath(cdir)
    if not os.path.isdir(cdir):
        os.makedirs(cdir)
    cfn = cdir+'/'+entry['fn']+"-"+comment['pubDate']+"."+config['comment_ext']
     
    try :
        cfile = file(cfn, "w")
    
        def makeXMLField(name, dict):
            return "<"+name+">"+cgi.escape(dict[name])+"</"+name+">\n";
    
        cfile.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
        cfile.write("<item>\n")
        cfile.write(makeXMLField('title',comment))
        cfile.write(makeXMLField('author',comment))
        cfile.write(makeXMLField('link',comment))
        cfile.write(makeXMLField('source',comment))
        cfile.write(makeXMLField('pubDate',comment))
        cfile.write(makeXMLField('description',comment))
        cfile.write("</item>\n")
        cfile.close()
    except:
        cfile.close()
    
    import smtplib
    try:
        server = smtplib.SMTP('192.168.0.1')
        server.sendmail("blog@sauria.com", "twl@sauria.com", \
                        "Subject: write back by %s\r\n\r\n%s\r\n%s" \
                        %  (comment['author'], cfn, comment['description']))
        server.quit()
    except:
        pass

def cb_prepare(args):
    """
    Handle comment related HTTP POST's
    
    @param request: pyblosxom request object
    @type request: a Pyblosxom request object
    """
    request = args["request"]
    form = request.getHttp()['form']
    config = request.getConfiguration()
    data = request.getData()
    
    if form.has_key("title") and form.has_key("author") and form.has_key("url") \
       and form.has_key("body"):

        cdict = {'title': form['title'].value, \
                 'author' : form['author'].value, \
                 'pubDate' : str(time.time()), \
                 'link' : form['url'].value, \
                 'source' : '', \
                 'description' : form['body'].value }
        
        writeComment(config, data, cdict)

    data = request.getData()
    entry_list = data['entry_list']
        
    for i in range(len(entry_list)):
        entry_list[i] = CommentDecorator(entry_list[i])
            
def cb_story(dict):
    renderer = dict['renderer']
    entry = dict['entry']
    template = dict['template']
    if len(renderer.getContent()) == 1:
        output = []
        if entry.has_key('comments'):        
            for comment in entry['comments']:
                renderer.outputTemplate(output, comment, 'comment')
            renderer.outputTemplate(output, entry, 'comment-form')
        return template +u"".join(output)
    else:
        return template