# vim: shiftwidth=4 tabstop=4 expandtab
from libs import tools
from libs.renderers.base import RendererBase
import re, os, sys, cgi

class BlosxomRenderer(RendererBase):
    def __init__(self, request, out = sys.stdout):
        RendererBase.__init__(self, request, out)
        self.dayFlag = 1

    def __getFlavour(self, taste = 'html'):
        """
        Flavours, or views, or templates, as some may call it, defaults are
        given, but can be overidden with files on the datadir. Don't like the
        default html templates, add your own, head.html, story.html etc.
        """
        # Ugly default templates, have to though :(
        html = {'content_type' : 'text/html',
                'head' : """<html><head><link rel="alternate" type="application/rss+xml" title="RSS" href="$url/?flav=rss" /><title>$blog_title $pi_da $pi_mo $pi_yr</title></head><body><center><font size="+3">$blog_title</font><br />$pi_da $pi_mo $pi_yr</center><p />""",
                'date_head' : '<div class="blosxomDayDiv">\n<span class="blosxomDate">$date</span>',
                'story' : """<p><a name="$fn"><b>$title</b></a><br />$body<br /><br />posted at: $ti | path: <a href="$url/$path">/$path</a> | <a href="$base_url/$file_path.$flavour">permanent link to this entry</a></p>\n""",
                'date_foot' : '</div>',
                'foot' : """<p /><center><a href="http://roughingit.subtlehints.net/pyblosxom"><img src="http://roughingit.subtlehints.net/images/pb_pyblosxom.gif" border="0" /></body></html>"""}
        rss = {'content_type' : 'text/xml',
               'head' : """<?xml version="1.0"?>\n<!-- name="generator" content="pyblosxom/0+5i" -->\n<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n\n<rss version="0.91">\n  <channel>\n    <title>$blog_title $pi_da $pi_mo $pi_yr</title>\n    <link>$url</link>\n    <description>$blog_description</description>\n    <language>$blog_language</language>\n""",
               'story' : """<item>\n    <title>$title</title>\n    <link>$base_url/$file_path.html</link>\n    <description>$body</description>\n  </item>\n""",
               'foot' : '   </channel>\n</rss>'}
        rss3 = {'content_type' : 'text/plain',
                'head' : """title: $blog_title\ndescription: $blog_description\nlink: $url\ncreator: wari@wari.per.sg Wari Wahab\nerrorsTo: wari@wari.per.sg Wari Wahab\nlang: $blog_language\n\n""",
                'story' :  """title: $title\nlink: $base_url/$file_path.html\ncreated: $w3cdate\nsubject: $path\nguid: $file_path\n""",
                'foot' : ''}
        esf = {'content_type' : 'text/plain',
                'head' : """title: $blog_title\ncontact: contact@example.com (The Contact Person)\nlink: $url\n\n""",
                'story' :  """$mtime\t$title\t$base_url/$file_path""",
                'foot' : ''}
        error = {'content_type' : 'text/plain',
                 'head' : """ Error: I'm afraid this is the first I've heard of a "$flavour" flavoured pyblosxom.\n Try dropping the "?flav=$flavour" bit from the end of the URL.\n\n"""}
        flavours = {'html' : html, 'rss' : rss, 'error' : error, 'rss3' : rss3, 'esf' : esf}
        # End of ugly portion! Yucks :)
        # Look for flavours in datadir

        data = self._request.getData()
        config = self._request.getConfiguration()

        pattern = re.compile(r'(config|content_type|head|date_head|date_foot|foot|story)\.' 
                + taste)
        flavourlist = tools.Walk(data['root_datadir'], 1, pattern)
        if not flavourlist:
            flavourlist = tools.Walk(config['datadir'], 1, pattern)

        for filename in flavourlist:
            flavouring = os.path.basename(filename).split('.')
            if flavours.has_key(flavouring[1]):
                flavours[flavouring[1]][flavouring[0]] = file(filename).read().strip()
            else:
                flavours[flavouring[1]] = { flavouring[0] : file(filename).read().strip() }

        if not flavours.has_key(taste):
            taste = 'error'

        # Check for any configuration override in flavours
        if flavours[taste].has_key('config'):
            for s in flavours[taste]['config'].split('\n'):
                if s.strip() != '':
                    match = re.match(r'(\w+)\s+(.*)', s)
                    if match:
                        data[match.groups()[0]] = match.groups()[1].strip()
            
        return flavours[taste]

    def __processEntry(self, filename, current_date, cache):
        """
        Main workhorse of pyblosxom stories, comments and other miscelany goes
        here
        """
        data = self._request.getData()

        def printTemplate(text, template):
            if template != '':
                self._out.write(tools.parseitem(text, tools.parse(text, template)).replace(r'\$', '$'))

        entryData = {}
        # Look for cached documents
        if cache.has_key(filename):
            entryData = cache[filename]
        
        # Cached? Try our entryparsers then.
        if not entryData:
            fileExt = re.search(r'\.([\w]+)$', filename)
            try:
                entryData = data['extensions'][fileExt.groups()[0]].parse(filename, self._request, cache)
            except IOError:
                return current_date

        if re.search(r'\Wxml', data['content-type']):
            entryData['title'] = cgi.escape(entryData['title'])
            entryData['body'] = cgi.escape(entryData['body'])
        elif data['content-type'] == 'text/plain':
            s = tools.Stripper()
            s.feed(entryData['body'])
            s.close()
            p = ['  ' + line for line in s.gettext().split('\n')]
            entryData['body'] = '\n'.join(p)
            
        entryData.update(data)
        if data['date'] != current_date:
            current_date = data['date']
            if not self.dayFlag:
                printTemplate(entryData, self.flavour.get('date_foot' ,''))
            self.dayFlag = 0
            printTemplate(entryData, self.flavour.get('date_head' ,''))
        printTemplate(entryData, self.flavour.get('story' ,''))
        return current_date


    def __processContent(self):
        config = self._request.getConfiguration()
        data = self._request.getData()

        cache_driver = tools.importName('libs.cache', config.get('cacheDriver', 'base'))
        cache = cache_driver.BlosxomCache(config.get('cacheConfig', ''))
        # Body stuff
        content_type = type(self._content)
        if callable(self._content):
            sys._out.write(self._content())
        elif content_type is dict:
            self._content.update(data)
            self._out.write(tools.parse(self._content, self.flavour['story']))
        elif content_type is list:
            current_date = ''
            count = 1
            for entry in self._content:
                data.update(entry)
                current_date = self.__processEntry(entry['filename'], current_date, cache)
                if data['pi_yr'] == '' and count >= int(config['num_entries']):
                    break
                count += 1
            cache.close()
                
    def render(self, header = 1):
        data = self._request.getData()
        config = self._request.getConfiguration()

        parsevars = {}
        for mem in config.keys():
            parsevars[mem] = config[mem]

        for mem in data.keys():
            parsevars[mem] = data[mem]

        self.flavour = self.__getFlavour(data.get('flavour', 'html'))
        data['content-type'] = self.flavour['content_type'].strip()
        if header:
            if self._needs_content_type:
                self.addHeader(['Content-type: %(content_type)s' % self.flavour])

            for line in self._header:
                self._out.write(line + '\n')
            self._out.write('\n')
        
        if self._content:
            if self.flavour.has_key('head'): 
                self._out.write(tools.parse(parsevars, self.flavour['head']))
            if self.flavour.has_key('story'):
                self.__processContent()
            if self.flavour.has_key('date_foot'): 
                self._out.write(tools.parse(parsevars, self.flavour['date_foot']))
            if self.flavour.has_key('foot'): 
                self._out.write(tools.parse(parsevars, self.flavour['foot']))
        
        self.rendered = 1


class Renderer(BlosxomRenderer):
    pass
