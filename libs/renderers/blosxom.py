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
                        config[match.groups()[0]] = match.groups()[1].strip()
            
        return flavours[taste]

    def __printTemplate(self, entry, template):
        """
        @param entry: either a dict or the Entry object
        @type  entry: dict or Entry

        @param template: the template string
        @type  template: string

        @returns: the content string
        @rtype: string
        """
        if template:
            finaltext = tools.parseitem(entry, tools.parse(entry, template))
            return finaltext.replace(r'\$', '$')
        return ""

    def __processEntry(self, entry, current_date):
        """
        Main workhorse of pyblosxom stories, comments and other miscelany goes
        here

        @param entry: either a dict or an Entry object
        @type  entry: dict or Entry object
        """
        data = self._request.getData()
        config = self._request.getConfiguration()

        output = []

        if re.search(r'\Wxml', data['content-type']):
            entry['title'] = cgi.escape(entry['title'])
            entry.setData(cgi.escape(entry.getData()))

        elif data['content-type'] == 'text/plain':
            s = tools.Stripper()
            s.feed(entry.getData())
            s.close()
            p = ['  ' + line for line in s.gettext().split('\n')]
            entry.setData('\n'.join(p))
            
        entry.update(data)
        entry.update(config)

        if entry['date'] != current_date:
            current_date = entry['date']
            if not self.dayFlag:
                output.append(self.__printTemplate(entry, self.flavour.get('date_foot' ,'')))
            self.dayFlag = 0
            output.append(self.__printTemplate(entry, self.flavour.get('date_head' ,'')))
        output.append(self.__printTemplate(entry, self.flavour.get('story' ,'')))
        return "".join(output), current_date


    def __processContent(self):
        """
        Processes the content for the story portion of a page.

        @returns: the content string
        @rtype: string
        """
        config = self._request.getConfiguration()
        data = self._request.getData()

        outputbuffer = []

        content_type = type(self._content)
        if callable(self._content):
            # if the content is a callable function, then we just spit out
            # whatever it returns as a string
            outputbuffer.append(self._content())

        elif content_type is dict:
            # if the content is a dict, then we parse it as if it were an
            # entry--except it's distinctly not an EntryBase derivative
            self._content.update(data)
            output = tools.parse(self._content, self.flavour['story'])
            outputbuffer.append(output)

        elif content_type is list:
            current_date = ''

            maxcount = config['num_entries']
            if maxcount and len(self._content) > maxcount:
                self._content = self._content[:maxcount]

            for entry in self._content:
                # FIXME - commented this next line out
                # data.update(entry)
                output, current_date = self.__processEntry(entry, current_date)
                outputbuffer.append(output)

                # FIXME what's this do?
                # if entry['pi_yr'] == '':
                #     break

        return "".join(outputbuffer)

    def render(self, header = 1):
        """
        Figures out flavours and such and then renders the content according
        to which flavour we're using.

        @param header: whether (1) or not (0) to render the HTTP headers
        @type  header: boolean
        """
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
                self._out.write(self.__processContent())
            if self.flavour.has_key('date_foot'): 
                self._out.write(tools.parse(parsevars, self.flavour['date_foot']))
            if self.flavour.has_key('foot'): 
                self._out.write(tools.parse(parsevars, self.flavour['foot']))
        
        self.rendered = 1

        # FIXME - we might want to do this at a later point?
        cache = tools.get_cache()
        if cache:
            cache.close()
                

class Renderer(BlosxomRenderer):
    pass
