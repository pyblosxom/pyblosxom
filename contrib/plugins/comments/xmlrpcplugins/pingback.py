from config import py
from Pyblosxom.pyblosxom import PyBlosxom
from Pyblosxom.Request import Request
from Pyblosxom import tools

import os, re, sgmllib, time, urllib

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
    import Pyblosxom.plugin_utils
    Pyblosxom.plugin_utils.initialize_plugins(config)

    # do start callback
    tools.run_callback("start", {'request': req}, mappingfunc=lambda x,y:y)
    
    p = PyBlosxom(req)
    p.startup()

    data['extensions'] = tools.run_callback("entryparser",
                                            {'txt': p.defaultEntryParser},
                                            mappingfunc=lambda x,y:y,
                                            defaultfunc=lambda x:x)

    uri = uri.replace(config['base_url'], '')
    req.addHttp({'PATH_INFO': uri, "form": {}})
    p.processPathInfo({'request': req})
    
    args = { 'request': req }
    es =  p.defaultFileListHandler(args)

    if len(es) == 1 and uri.find(es[0]['file_path']) >= 0:
        return es[0]

    for i in es:
        if i['fn'] == data['pi_frag'][1:]:
            return i
            
def pingback(request, source, target):
    source_file = urllib.urlopen(source.split('#')[0])
    source_page = parser()
    source_page.feed(source_file.read())
    source_file.close()

    if source_page.title == "": source_page.title = source
    
    if target in source_page.hrefs:
        target_entry = fileFor(request, target)

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
                        body=body[:body.rfind(' ',0,250)][:250] + " ...<br />"
        except:
            pass

        cmt = {'title':source_page.title, \
               'author':'Pingback from %s' % source_page.title,
               'pubDate' : str(time.time()), \
               'link': source,
               'source' : '',
               'description' : body}
        
        from comments import writeComment
        config = request.getConfiguration()
        data = request.getData()
        datadir = config['datadir']
        data['entry_list'] = [ target_entry ]

        # TODO: Check if comment from the URL exists
        writeComment(config, data, cmt)
               
        return "success pinging %s from %s\n" % (source, target)
    else:
        return "produce xmlrpc fault here"

def register_xmlrpc_methods():
    return {'pingback.ping': pingback }
