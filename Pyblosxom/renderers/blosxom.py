"""
BlosxomRenderer can use the following keys from config.py:

py['blosxom_custom_flavours'] is a list of strings containing additional
flavour templates to be recognized by PyBlosxom.

examples::

    py["blosxom_custom_flavours"] = ["registry", "magictemplate"]

"""

from Pyblosxom import tools
from Pyblosxom.renderers.base import RendererBase
import re, os, sys, codecs
try:
    from xml.sax.saxutils import escape
except ImportError:
    from cgi import escape


class BlosxomRenderer(RendererBase):
    def __init__(self, request, stdoutput = sys.stdout):
        RendererBase.__init__(self, request, stdoutput)
        config = request.getConfiguration()
        (e, d, sr, sw) = codecs.lookup(config.get('blog_encoding', 
                'iso-8859-1'))
        self._out = sw(self._out)
        self.dayFlag = 1
        self._request = request
        self._encoding = config.get("blog_encoding", "iso-8859-1")

    def _getFlavour(self, taste = 'html'):
        """
        Flavours, or views, or templates, as some may call it, defaults are
        given, but can be overidden with files on the datadir. Don't like the
        default html templates, add your own, head.html, story.html etc.
        """
        # Ugly default templates, have to though :(
        html = {'content_type' : 'text/html',
                'head' : """<html><head><link rel="alternate" type="application/rss+xml" title="RSS" href="$url/?flav=rss" /><title>$blog_title $pi_da $pi_mo $pi_yr</title></head><body><center><font size="+3">$blog_title</font><br />$pi_da $pi_mo $pi_yr</center><p />""",
                'date_head' : '<div class="blosxomDayDiv">\n<span class="blosxomDate">$date</span>',
                'story' : """<p><a name="$fn"><b>$title</b></a><br />$body<br /><br />posted at: $ti | path: <a href="$base_url/$absolute_path" title="path">/$absolute_path</a> | <a href="$base_url/$file_path.$flavour">permanent link to this entry</a></p>\n""",
                'date_foot' : '</div>',
                'foot' : """<p /><center><a href="http://roughingit.subtlehints.net/pyblosxom"><img src="http://roughingit.subtlehints.net/images/pb_pyblosxom.gif" border="0" /></body></html>"""}
        rss = {'content_type' : 'text/xml',
               'head' : """<?xml version="1.0"?>\n<!-- name="generator" content="$pyblosxom_name/$pyblosxom_version" -->\n<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n\n<rss version="0.91">\n  <channel>\n    <title>$blog_title $pi_da $pi_mo $pi_yr</title>\n    <link>$url</link>\n    <description>$blog_description</description>\n    <language>$blog_language</language>\n""",
               'story' : """<item>\n    <title>$title</title>\n    <link>$base_url/$file_path.html</link>\n    <description>$body</description>\n  </item>\n""",
               'foot' : '   </channel>\n</rss>'}
        rss3 = {'content_type' : 'text/plain',
                'head' : """title: $blog_title\ndescription: $blog_description\nlink: $url\ncreator: $blog_author\nerrorsTo: $blog_author\nlang: $blog_language\n\n\n""",
                'story' :  """title: $title\nlink: $base_url/$file_path.html\ncreated: $w3cdate\nsubject: $path\nguid: $file_path\n\n""",
                'foot' : ''}
        esf = {'content_type' : 'text/plain',
                'head' : """title: $blog_title\ncontact: contact@example.com (The Contact Person)\nlink: $url\n\n\n""",
                'story' :  """$mtime\t$title\t$base_url/$file_path\n""",
                'foot' : ''}
        error = {'content_type' : 'text/plain',
                 'head' : """ Error: I'm afraid this is the first I've heard of a "$flavour" flavoured pyblosxom.\n Try dropping the "?flav=$flavour" bit from the end of the URL.\n\n"""}
        flavours = {'html' : html, 'rss' : rss, 'error' : error, 'rss3' : rss3, 'esf' : esf}
        # End of ugly portion! Yucks :)
        # Look for flavours in datadir

        data = self._request.getData()
        config = self._request.getConfiguration()

        custom_flavours = config.get('blosxom_custom_flavours', [])
        if custom_flavours:
            custom_flavours = "|" + "|".join(custom_flavours)
        else:
            custom_flavours = ""
        
        pattern = re.compile(r'(content_type|head|date_head|date_foot|foot|story'+custom_flavours+')\.' 
                             + taste)
        flavourlist = tools.Walk(self._request, data['root_datadir'], 1, pattern)
        if not flavourlist:
            flavourlist = tools.Walk(self._request, config['datadir'], 1, pattern)

        for filename in flavourlist:
            flavouring = os.path.basename(filename).split('.')
            flav_template = unicode(open(filename).read(), 
                    config.get('blog_encoding', 'iso-8859-1'))
            if flavours.has_key(flavouring[1]):
                flavours[flavouring[1]][flavouring[0]] = flav_template
            else:
                flavours[flavouring[1]] = {flavouring[0]: flav_template}

        if not flavours.has_key(taste):
            taste = 'error'

        return flavours[taste]

    def _printTemplate(self, entry, template):
        """
        @param entry: either a dict or the Entry object
        @type  entry: dict or Entry

        @param template: the template string
        @type  template: string

        @returns: the content string
        @rtype: string
        """
        if template:
            template = unicode(template)
            finaltext = tools.parse(self._encoding, entry, template)
            return finaltext.replace(r'\$', '$')
        return ""

    def _processEntry(self, entry, current_date):
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
            quotes = {"'":"&apos;", '"':"&quot;"}
            entry['title'] = escape(entry['title'],quotes)
            entry.setData(escape(entry.getData(),quotes))

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
                self.outputTemplate(output, entry, 'date_foot')
            self.dayFlag = 0
            self.outputTemplate(output, entry, 'date_head')

        self.outputTemplate(output, entry, 'story', override=1)

        template = u""
        args = self._run_callback("story_end", { "entry": entry, "template": template }) 
            
        return "".join(output) + args['template'], current_date    

    def _processContent(self):
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

        elif content_type is type({}):
            # if the content is a dict, then we parse it as if it were an
            # entry--except it's distinctly not an EntryBase derivative
            self._content.update(data)
            output = tools.parse(self._encoding, self._content, self.flavour['story'])
            outputbuffer.append(output)

        elif content_type is type([]):
            current_date = ''

            maxcount = config['num_entries']
            if maxcount and len(self._content) > maxcount:
                self._content = self._content[:maxcount]

            for entry in self._content:
                # FIXME - commented this next line out
                # data.update(entry)
                output, current_date = self._processEntry(entry, current_date)
                outputbuffer.append(output)

        return self.write(u"".join(outputbuffer))

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

        self.flavour = self._getFlavour(data.get('flavour', 'html'))
        data['content-type'] = self.flavour['content_type'].strip()
        if header:
            if self._needs_content_type and data['content-type'] !="":
                self.addHeader('Content-type', '%(content-type)s' % data)

            self.showHeaders()
        
        if self._content:
            if self.flavour.has_key('head'):
                self._outputFlavour(parsevars,'head')
            if self.flavour.has_key('story'):
                self._processContent()
            if self.flavour.has_key('date_foot'): 
                self._outputFlavour(parsevars,'date_foot')                
            if self.flavour.has_key('foot'): 
                self._outputFlavour(parsevars,'foot')                
        
        self.rendered = 1

        # FIXME - we might want to do this at a later point?
        cache = tools.get_cache(self._request)
        if cache:
            cache.close()
                
    def _outputFlavour(self, entry, template_name):
        """
        Find the flavour template for template_name, run any blosxom callbacks, 
        substitute vars into it and write the template to the output
        
        @param entry: the EntryBase object
        @type entry: L{Pyblosxom.entries.base.EntryBase}

        @param template_name: - name of the flavour template 
        @type template_name: string
        """
        template = self.flavour[template_name]

        args = self._run_callback(template_name, { "entry": entry, "template": template }) 
        template = args["template"]
        entry = args["entry"]

        self.write(tools.parse(self._encoding, entry, template))
            
    def outputTemplate(self, output, entry, template_name, override=0):
        """
        Find the flavour template for template_name, run any blosxom callbacks,
        substitute entry into it and append the template to the output.

        If the entry has a "template_name" property and override is 1
        (this happens in the story template), then we'll use that
        template instead.
        
        @param output: list of strings of the output
        @type output: list

        @param entry: the entry to render with this flavour template
        @type entry: L{Pyblosxom.entries.base.EntryBase}

        @param template_name: name of the flavour template to use
        @type template_name: string

        @param override: whether (1) or not (0) this template can
            be overriden with the "template_name" property of the entry
        @type  override: boolean
        """
        template = ""
        if override == 1:
            # here we do a quick override...  if the entry has a template
            # field we use that instead of the template_name argument
            # passed in.
            actual_template_name = entry.get("template_name", template_name)
            template = self.flavour.get(actual_template_name, '')

        if not template:
            template = self.flavour.get(template_name, '')

        # we run this through the regular callbacks
        args = self._run_callback(template_name, { "entry": entry, "template": template })

        template = args["template"]
        entry = args["entry"]

        output.append(self._printTemplate(entry, template))

    def _run_callback(self, chain, input):
        """
        Makes calling blosxom callbacks a bit easier since they all have the
        same mechanics.  This function merely calls run_callback with
        the arguments given and a mappingfunc.
        
        The mappingfunc copies the "template" value from the output to the 
        input for the next function.
        
        Refer to run_callback for more details.
        """
        input.update( { "renderer": self } )
        input.update( { "request": self._request } )

        return tools.run_callback(chain, input, 
                            mappingfunc=lambda x,y: x,
                            defaultfunc=lambda x:x)
        
    def getContent(self):
        """
        Return the content field
        
        This is exposed for blosxom callbacks.
        
        @returns: content
        """
        return self._content
        
class Renderer(BlosxomRenderer):
    pass


# vim: shiftwidth=4 tabstop=4 expandtab
