"""
This module contains an extension to Blosxom file entries to support
comments.

This plugin requires the pyXML module.

This module supports the following config parameters (they are not
required):

    comment_dir - the directory we're going to store all our comments in.
                  this defaults to datadir + "comments".
    comment_ext - the file extension used to denote a comment file.
                  this defaults to "cmt".

    comment_smtp_server - the smtp server to send comments notifications
                          through.
    comment_smtp_from - the person comment notifications will be from.
    comment_smtp_to - the person to send comment notifications to.


Comments are stored 1 per file in a parallel hierarchy to the datadir
hierarchy.  The filename of the comment is the filename of the blog
entry, plus the creation time of the comment as a float, plus the 
comment extension.  The contents of the comment file is an RSS 2.0
formatted item.

Each entry has to have the following properties in order to work with
comments:

 1. absolute_path - the category of the entry.  ex. "dev/pyblosxom"
 2. fn - the filename of the entry without the file extension and without
    the directory.  ex. "staticrendering"
 3. file_path - the absolute_path plus the fn.  ex. "dev/pyblosxom/staticrendering"
"""
import cgi, glob, os.path, re, time, cPickle
from xml.sax.saxutils import escape
from Pyblosxom import tools
from Pyblosxom.entries.base import EntryBase

tools.make_logger('/tmp/comments.log')
    
def verify_installation(request):
    config = request.getConfiguration()

    retval = 1

    if config.has_key('comment_dir') and not os.path.isdir(config['comment_dir']):
        print 'The "comment_dir" property in the config file must refer to a directory'
        retval = 0

    actual_smtp_keys = []
    smtp_keys=['comment_smtp_server', 'comment_smtp_from', 'comment_smtp_to']
    for k in smtp_keys:
        if config.has_key(k):
            actual_smtp_keys.append(k)
    if len(k) > 0:
        for i in smtp_keys:
            if i not in actual_smtp_keys:
                print("Missing comment SMTP property: '%s'" % i)
                retval = 0
    
    optional_keys = ['comment_dir', 'comment_ext']
    for i in optional_keys:
        if not config.has_key(i):
            print("missing optional property: '%s'" % i)

    return retval

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
    try:
        return [ readComment(f) for f in filelist ]
    except:
        tools.log("Couldn't read comments for entry: ",entry)
        return []
    
def getCommentCount(entry, config):
    """
    @param: a file entry
    @type: dict
    
    @returns: the number of comments for the entry
    """
    if entry['absolute_path'] == None: return 0
    filelist = glob.glob(cmtExpr(entry,config))
    if filelist is not None:
        return len(filelist)
    return 0

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
    from xml.sax import make_parser, SAXException
    from xml.sax.handler import feature_namespaces, ContentHandler
    class cmtHandler(ContentHandler):
        def __init__(self, cmt):
            self._data = ""
            self.cmt = cmt
        def startElement(self, name, atts):
            self._data = ""
        def endElement(self, name):
            self.cmt['cmt_'+name] = self._data
        def characters(self, content):
            self._data += content

    cmt = {}
    
    try:
        story = open(filename)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        handler = cmtHandler(cmt)
        parser.setContentHandler(handler)
        parser.parse(story)
        story.close()
        cmt['cmt_time'] = cmt['cmt_pubDate'] # timestamp as float for comment anchor
        cmt['cmt_pubDate'] = time.ctime(float(cmt['cmt_pubDate']))
        story.close()
    except:
        tools.log("Couldn't read: ", filename)
        story.close()
    return cmt

def writeComment(config, data, comment):
    """
    Write a comment
    
    @param config: dict containing pyblosxom config info
    @type  config: dict
    
    @param data: dict containing entry info
    @type  data: dict
    
    @param comment: dict containing comment info
    @type  comment: dict
    """
    entry = data['entry_list'][0]
    cdir = os.path.join(config['comment_dir'],entry['absolute_path'])
    cdir = os.path.normpath(cdir)
    if not os.path.isdir(cdir):
        os.makedirs(cdir)
    cfn = os.path.join(cdir,entry['fn']+"-"+comment['pubDate']+"."+config['comment_ext'])
     
    # write comment
    cfile = None
    try :
        cfile = open(cfn, "w")
    except:
        tools.log("Couldn't open comment file %s for writing" % cfn)
        return
    else:
        pass
    
    def makeXMLField(name, field):
        return "<"+name+">"+cgi.escape(field[name])+"</"+name+">\n";
    try:
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
        tools.log("Error writing comment data for ", cfn)
        cfile.close()
        
    #write latest pickle
    latest = None
    latestFilename = os.path.join(config['comment_dir'],'LATEST.cmt')
    try:
        latest = open(latestFilename,"w")
    except:
        tools.log("Couldn't open latest comment pickle for writing")
        return
    else:
        modTime = float(comment['pubDate'])

    try:
        cPickle.dump(modTime,latest)
        latest.close()
    except (IOError):
        # should log or e-mail
        if latest:
            latest.close()
        return
    
    # if the right config keys are set, notify by e-mail
    if config.has_key('comment_smtp_server') \
            and config.has_key('comment_smtp_from') \
            and config.has_key('comment_smtp_to'):
        import smtplib
        author = escape_SMTP_commands(clean_author(comment['author']))
        description = escape_SMTP_commands(comment['description'])
        try:
            server = smtplib.SMTP(config['comment_smtp_server'])
            curl = config['base_url']+'/'+entry['file_path']
        
            message = []
            message.append("From: %s" % config["comment_smtp_from"])
            message.append("To: %s" % config["comment_smtp_to"])
            message.append("Date: %s" % time.ctime(modTime))
            message.append("Subject: write back by %s" % author)
            message.append("")
            message.append("%s\n%s\n%s\n" % (description, cfn, curl))
            server.sendmail(from_addr=config['comment_smtp_from'], 
                            to_addrs=config['comment_smtp_to'], 
                            msg="\n".join(message))
            server.quit()
        except:
            tools.log("Error sending mail: %s" % message)
            pass

def clean_author(s):
    """
    Guard against blasterattacko style attacks that embedd SMTP commands in
    author field.

    If author field is more than one line, reduce to one line

    @param the string to be checked
    @type string

    @returns the sanitized string
    """
    return s.splitlines()[0]

def escape_SMTP_commands(s):
    """
    Guard against blasterattacko style attacks that embed SMTP commands by
    using an HTML span to make the command syntactically invalid to SMTP but
    renderable by HTML

    @param the string to be checked
    @type string

    @returns the sanitized string
    """
    def repl_fn(mo):
        return '<span>'+mo.group(0)+'</span>'
    s = re.sub('([Tt]o:.*)',repl_fn,s)
    s = re.sub('([Ff]rom:.*)',repl_fn,s)
    s = re.sub('([Ss]ubject:.*)',repl_fn,s)
    return s

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
    """
    Handle comment related HTTP POST's.
    
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

        # expand all of entry vars for expansion
        entry = args['entry']
        single_entry = entry['entry_list'][0]
        single_entry['title'] # force lazy evaluation
        entry.update(single_entry)
        args['entry'] = entry
    return template
        

def cb_story(args):
    renderer = args['renderer']
    entry = args['entry']
    template = args['template']
    request = args["request"]
    config = request.getConfiguration()
    if len(renderer.getContent()) == 1 \
            and renderer.flavour.has_key('comment-story') \
            and not entry.has_key("no_comments"):
        template = renderer.flavour.get('comment-story','')
        args['template'] = template

    entry['num_comments'] = getCommentCount(entry, config)
    return template

def cb_story_end(args):
    renderer = args['renderer']
    entry = args['entry']
    template = args['template']
    request = args["request"]
    config = request.getConfiguration()
    if len(renderer.getContent()) == 1 \
            and renderer.flavour.has_key('comment-story') \
            and not entry.has_key("no_comments"):
        output = []
        entry['comments'] = readComments(entry, config)
        if entry.has_key('comments'):        
            for comment in entry['comments']:
                renderer.outputTemplate(output, comment, 'comment')
            renderer.outputTemplate(output, entry, 'comment-form')
        args['template'] = template +u"".join(output)

    entry['num_comments'] = getCommentCount(entry, config)
    return template
    
def cb_start(args):
    request = args['request']
    config = request.getConfiguration()

    if not config.has_key('comment_dir'):
        config['comment_dir'] = os.path.join(config['datadir'],'comments')
    if not config.has_key('comment_ext'):
        config['comment_ext'] = 'cmt'
