from config import py
from libs.pyblosxom import PyBlosxom
from libs.Request import Request
from libs import tools

import cgi, os, re, sgmllib, time, urllib

class parser(sgmllib.SGMLParser):
    """ Shamelessly grabbed from Sam Ruby
    from http://www.intertwingly.net/code/mombo/pingback.py
    """
    """ extract title and hrefs from a web page"""
    intitle=0
    title = ""
    hrefs = []

    def do_a(self, attrs):
        attrs=dict(attrs)
        if attrs.has_key('href'): self.hrefs.append(attrs['href'])
        
    def do_title(self, attrs):
        if self.title=="": self.intitle=1
    def unknown_starttag(self, tag, attrs):
        self.intitle=0
    def unknown_endtag(self,tag):
        self.intitle=0
    def handle_charref(self, ref):
        if self.intitle: self.title = self.title + ("&#%s;" % ref)
    def handle_data(self,text):
        if self.intitle: self.title = self.title + text

        
def fileFor(req, uri):
    config = req.getConfiguration()
    data = req.getData()

    # import plugins
    import libs.plugins.__init__
    libs.plugins.__init__.initialize_plugins(config)

    # do start callback
    tools.run_callback("start", {'request': req}, mappingfunc=lambda x,y:y)
    
    req.addHttp({"form": cgi.FieldStorage()})
    
    p = PyBlosxom(req)
    p.startup()

    data['extensions'] = tools.run_callback("entryparser",
                                            {'txt': PyBlosxom.defaultEntryParser},
                                            mappingfunc=lambda x,y:y,
                                            defaultfunc=lambda x:x)

    data['pi_yr'] = ''
    data['pi_mo'] = ''
    data['pi_da'] = ''
    path_info = uri.split('/')[4:] # get rid of http and script
    if path_info[0] == '':
        path_info.pop(0)

    p.processPathInfo(path_info)
    
    args = { 'request': req }
    es =  p.defaultFileListHandler(args)
    
    for i in es:
        if i['fn'] == data['pi_frag'][1:]:
            return i['file_path']
            
def pingback(request, source, target):
    source_file = urllib.urlopen(source.split('#')[0])
    source_page = parser()
    source_page.feed(source_file.read())
    source_file.close()

    if source_page.title == "": source_page.title = source
    
    if target in source_page.hrefs:
        target_file = fileFor(request, target)

        body = ''
        try:
            from rssfinder import getFeeds
            from rssparser import parse

            baseurl=source.split("#")[0]
            for feed in getFeeds(baseurl):
                for item in parse(feed)['items']:
                    if item['link']==source:
                        if 'title' in item: title = item['title']
                        if 'content_encoded' in item: body = item['content_encoded'].strip()
                        if 'description' in item: body = item['description'].strip() or body
                        body=re.compile('<.*?>',re.S).sub('',body)
                        body=re.sub('\s+',' ',body)
                        body=body[:body.rfind(' ',0,250)][:250] + " ...<br /><br />"
        except:
            pass

        cmt = {'title':source_page.title, \
               'author':'Pingback',
               'pubDate' : str(time.time()), \
               'link': source,
               'source' : '',
               'description' : body}
        
        from libs.plugins.commentdecorator import writeComment
        config = request.getConfiguration()
        data = request.getData()
        from libs.entries.fileentry import FileEntry
        datadir = config['datadir']
        entry = FileEntry(config, datadir+'/'+target_file+'.txt', datadir)
        data['entry_list'] = [ entry ]
        writeComment(config, data, cmt)
               
        return "success pinging %s from %s\n" % (source, target)
    else:
        return "produce xmlrpc fault here"

def register_xmlrpc_methods():
    return {'pingback.ping': pingback }
