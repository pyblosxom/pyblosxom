#
# Comment poster
#
# IMPORTANT: This plugin requires the pyXML module
#
#

import cgi, glob, os.path, re, time, cPickle
from xml.sax.saxutils import escape
from libs import tools
from libs.entries.base import EntryBase
    
"""
This module contains an extension to Blosxom file entries to support comments
"""

#
# file system  implementation
# Comments are stored 1 per file, in a parallel hierarchy to the datadir hierarchy
# The filename of the comment is the filename of the blog entry plus the creation
# time of the comment as a time float.
# The contents of the comment file is an RSS 2.0 item
#        
        
def readComments(entry, config):
    """
    @param: a file entry
    @type: dict
    
    @returns: a list of comment dicts
    """
    filelist = glob.glob(cmtExpr(entry, config))
    filelist.sort()
    if not entry.has_key('num_comments'):
        entry['num_comments'] = len(filelist)
    return [ readComment(f) for f in filelist ]
    
def getCommentCount(entry, config):
    """
    @param: a file entry
    @type: dict
    
    @returns: the number of comments for the entry
    """
    if entry['absolute_path'] == None: return 0
    filelist = glob.glob(cmtExpr(entry,config))
    return len(filelist)

def cmtExpr(entry, config):
    """
    Return a string containing the regular expression for comment entries
    
    @param: a file entry
    @type: dict
    @returns: a string with the directory path for the comment
    
    @param: configuratioin dictionary
    @type: dict
    
    @returns: a string containing the regular expression for comment entries
    """
    
    cmtDir = os.path.join(config['comment_dir'],entry['absolute_path'])
    cmtExpr = os.path.join(cmtDir,entry['fn']+'-*.'+config['comment_ext'])
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
    except SAXException:
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
    cdir = os.path.join(config['comment_dir'],entry['absolute_path'])
    cdir = os.path.normpath(cdir)
    if not os.path.isdir(cdir):
        os.makedirs(cdir)
    cfn = os.path.join(cdir,entry['fn']+"-"+comment['pubDate']+"."+config['comment_ext'])
     
    # write comment
    try :
        cfile = file(cfn, "w")
    
        def makeXMLField(name, field):
            return "<"+name+">"+cgi.escape(field[name])+"</"+name+">\n";
    
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
        
    #write latest pickle
    try:
        latestFilename = os.path.join(config['comment_dir'],'LATEST.cmt')
        latest = file(latestFilename,"w")
        modTime = float(comment['pubDate'])
        cPickle.dump(modTime,latest)
        latest.close()
    except (EOFError, IOError):
        pass
    
    
    # if the right config keys are set, notify by e-mail
    if config.has_key('comment_smtp_server') and \
       config.has_key('comment_smtp_from') and \
       config.has_key('comment_smtp_to'):
        import smtplib
        try:
            server = smtplib.SMTP(config['comment_smtp_server'])
            curl = config['base_url']+'/'+entry['file_path']
            message = "Subject: write back by %s\r\n\r\n%s\r\n%s\r\n%s" \
                      %  (comment['author'], comment['description'], cfn, curl)
            server.sendmail(config['comment_smtp_from'], config['comment_smtp_to'], message)
            server.quit()
        except:
            pass

def sanitize(body):
    """
    This code shamelessly lifted from Sam Ruby's mombo/post.py
    """
    body=re.sub(r'\s+$','',body)
    body=re.sub('\r\n?','\n', body)

    # naked urls become hypertext links
    body=re.sub('(^|[\\s.:;?\\-\\]<])' + 
                '(http://[-\\w;/?:@&=+$.!~*\'()%,#]+[\\w/])' +
                '(?=$|[\\s.:;?\\-\\[\\]>])',
                '\\1<a href="\\2">\\2</a>',body)

    # html characters used in text become escaped
    body=escape(body)

    # passthru <a href>, <em>, <i>, <b>, <blockquote>, <br/>, <p>, 
    # <abbr>, <acronym>, <big>, <cite>, <code>, <dfn>, <kbd>, <pre>, <small>
    # <strong>, <sub>, <sup>, <tt>, <var>
    body=re.sub('&lt;a href="([^"]*)"&gt;([^&]*)&lt;/a&gt;',
                '<a href="\\1">\\2</a>', body)
    body=re.sub('&lt;a href=\'([^\']*)\'&gt;([^&]*)&lt;/a&gt;',
                '<a href="\\1">\\2</a>', body)
    body=re.sub('&lt;em&gt;([^&]*)&lt;/em&gt;', '<em>\\1</em>', body)
    body=re.sub('&lt;i&gt;([^&]*)&lt;/i&gt;', '<i>\\1</i>', body)
    body=re.sub('&lt;b&gt;([^&]*)&lt;/b&gt;', '<b>\\1</b>', body)
    body=re.sub('&lt;blockquote&gt;([^&]*)&lt;/blockquote&gt;', 
                '<blockquote>\\1</blockquote>', body)
    body=re.sub('&lt;br\s*/?&gt;\n?','\n',body)

    body=re.sub('&lt;abbr&gt;([^&]*)&lt;/abbr&gt;', '<abbr>\\1</abbr>', body)
    body=re.sub('&lt;acronym&gt;([^&]*)&lt;/acronym&gt;', '<acronym>\\1</acronym>', body)
    body=re.sub('&lt;big&gt;([^&]*)&lt;/big&gt;', '<big>\\1</big>', body)
    body=re.sub('&lt;cite&gt;([^&]*)&lt;/cite&gt;', '<cite>\\1</cite>', body)
    body=re.sub('&lt;code&gt;([^&]*)&lt;/code&gt;', '<code>\\1</code>', body)
    body=re.sub('&lt;dfn&gt;([^&]*)&lt;/dfn&gt;', '<dfn>\\1</dfn>', body)
    body=re.sub('&lt;kbd&gt;([^&]*)&lt;/kbd&gt;', '<kbd>\\1</kbd>', body)
    body=re.sub('&lt;pre&gt;([^&]*)&lt;/pre&gt;', '<pre>\\1</pre>', body)
    body=re.sub('&lt;small&gt;([^&]*)&lt;/small&gt;', '<small>\\1</small>', body)
    body=re.sub('&lt;strong&gt;([^&]*)&lt;/strong&gt;', '<strong>\\1</strong>', body)
    body=re.sub('&lt;sub&gt;([^&]*)&lt;/sub&gt;', '<sub>\\1</sub>', body)
    body=re.sub('&lt;sup&gt;([^&]*)&lt;/sup&gt;', '<sup>\\1</sup>', body)
    body=re.sub('&lt;tt&gt;([^&]*)&lt;/tt&gt;', '<tt>\\1</tt>', body)
    body=re.sub('&lt;var&gt;([^&]*)&lt;/var&gt;', '<var>\\1</var>', body)

    body=re.sub('&lt;/?p&gt;','\n\n',body).strip()

    # wiki like support: _em_, *b*, [url title]
    body=re.sub(r'\b_(\w.*?)_\b', r'<em>\1</em>', body)
    body=re.sub(r'\*(\w.*?)\*', r'<b>\1</b>', body)
    body=re.sub(r'\[(\w+:\S+\.gif) (.*?)\]', r'<img src="\1" alt="\2" />', body)
    body=re.sub(r'\[(\w+:\S+\.jpg) (.*?)\]', r'<img src="\1" alt="\2" />', body)
    body=re.sub(r'\[(\w+:\S+\.png) (.*?)\]', r'<img src="\1" alt="\2" />', body)
    body=re.sub(r'\[(\w+:\S+) (.*?)\]', r'<a href="\1">\2</a>', body).strip()

    # unordered lists: consecutive lines starting with spaces and an asterisk
    chunk=re.compile(r'^( *\*.*(?:\n *\*.*)+)',re.M).split(body)
    for i in range(1, len(chunk), 2):
        (html,stack)=('', [''])
        for indent,line in re.findall(r'( +)\* +(.*)', chunk[i]) + [('','')]:
            if indent>stack[-1]: (stack,html)=(stack+[indent],html+'<ul>\r')
            while indent<stack[-1]: (stack,html)=(stack[:-1],html+'</ul>\r')
            if line: html += '<li>'+line+'</li>\r'
            chunk[i]=html

    # white space
    chunk=re.split('\n\n+', ''.join(chunk))
#    if len(chunk)>1: body='<p>' + '</p>\r<p>'.join(chunk) + '</p>\r'
    body=re.sub('\n','<br />\n', body)
    body=re.compile('<p>(<ul>.*?</ul>)\r</p>?',re.M).sub(r'\1',body)
    body=re.compile('<p>(<blockquote>.*?</blockquote>)</p>?',re.M).sub(r'\1',body)
    body=re.sub('\r', '\n', body)
    body=re.sub('  +', '&nbsp; ', body)

    return body        
        
        
def cb_prepare(args):
    """cvs
    Handle comment related HTTP POST's
    
    @param request: pyblosxom request object
    @type request: a Pyblosxom request object
    """
    request = args["request"]
    form = request.getHttp()['form']
    config = request.getConfiguration()
    data = request.getData()
    
    if form.has_key("title") and form.has_key("author") and form.has_key("body"):

        body = form['body'].value
        
        body = sanitize(body)

        # Check if the form has a URL
        url = (form.has_key('url') and [form['url'].value] or [''])[0]
        
        cdict = {'title': form['title'].value, \
                 'author' : form['author'].value, \
                 'pubDate' : str(time.time()), \
                 'link' : url, \
                 'source' : '', \
                 'description' : body }
        
        writeComment(config, data, cdict)


def cb_head(args):
    renderer = args['renderer']
    template = args['template']

    newtemplate = renderer.flavour.get('comment-head','')
    if not newtemplate == '' and len(renderer.getContent()) == 1:
        args['template'] = newtemplate
    return template
        
def cb_story(args):
    renderer = args['renderer']
    entry = args['entry']
    template = args['template']
    request = tools.get_registry()["request"]
    config = request.getConfiguration()
    if len(renderer.getContent()) == 1 and renderer.flavour.has_key('comment-story'):
        template = renderer.flavour.get('comment-story','')
        output = []
        entry['comments'] = readComments(entry, config)
        if entry.has_key('comments'):        
            for comment in entry['comments']:
                renderer.outputTemplate(output, comment, 'comment')
            renderer.outputTemplate(output, entry, 'comment-form')
        args['template'] = template +u"".join(output)
    else:
        entry['num_comments'] = getCommentCount(entry,config)
        return template
    
def cb_start(args):
    request = args['request']
    config = request.getConfiguration()
    custom_flavours = ['comment-head', 'comment-story', 'comment', 'comment-form']
    if not config.has_key('blosxom_custom_flavours'):
        config['blosxom_custom_flavours'] = custom_flavours
    else:
        for mem in custom_flavours:
            if mem not in config['blosxom_custom_flavours']:
                config['blosxom_custom_flavours'].append(mem)
    if not config.has_key('comment_dir'):
        config['comment_dir'] = os.path.join(config['datadir'],'comments')
    if not config.has_key('comment_ext'):
        config['comment_ext'] = 'cmt'
