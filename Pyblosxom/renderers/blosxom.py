"""
This is the default renderer.  It tries to match the behavior of the
blosxom renderer.
"""

from Pyblosxom import tools
from Pyblosxom.renderers.base import RendererBase
import re, os, sys, codecs
try:
    from xml.sax.saxutils import escape
except ImportError:
    from cgi import escape

# Ugly default templates, have to though :(
HTML = {'content_type' : 'text/html',
        'head' : """<html><head><title>$blog_title_with_path $pi_da $pi_mo $pi_yr</title></head><body><h1>$blog_title</h1><p>$pi_da $pi_mo $pi_yr</p>""",
        'date_head' : '<h2>$date</h2>',
        'story' : """<h3><a name="$fn">$title</a></h3><div class="blosxomStory">$body<p>posted at: $ti | path: <a href="$base_url/$absolute_path" title="path">/$absolute_path</a> | <a href="$base_url/$file_path.$flavour">permanent link to this entry</a></p></div>\n""",
        'date_foot' : '',
        'foot' : """<p><a href="http://roughingit.subtlehints.net/pyblosxom"><img src="http://roughingit.subtlehints.net/images/pb_pyblosxom.gif" alt="Made with PyBlosxom" border="0" /></a></p></body></html>"""}

RSS = {'content_type' : 'text/xml',
       'head' : """<?xml version="1.0" encoding="$blog_encoding"?>\n<!-- name="generator" content="$pyblosxom_name/$pyblosxom_version" -->\n<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n\n<rss version="0.91">\n<channel>\n<title>$blog_title $pi_da $pi_mo $pi_yr</title>\n<link>$url</link>\n<description>$blog_description</description>\n<language>$blog_language</language>\n""",
       'story' : """<item>\n    <title>$title</title>\n    <link>$base_url/$file_path.html</link>\n    <description>$body</description>\n  </item>\n""",
       'foot' : '   </channel>\n</rss>'}

ERROR = {'content_type' : 'text/plain',
         'head' : """Error: I'm afraid this is the first I've heard of a "$flavour" flavoured pyblosxom.\n Try dropping the "?flav=$flavour" bit from the end of the URL.\n\n"""}

DEFAULT_FLAVOURS = {'html' : HTML, 
                    'rss' : RSS,
                    'error' : ERROR}

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

    def _getFlavour(self, taste='html'):
        """
        Flavours, or views, or templates, as some may call it, defaults are
        given, but can be overidden with files on the datadir. Don't like the
        default html templates, add your own, head.html, story.html etc.
        """
        data = self._request.getData()
        config = self._request.getConfiguration()

        pattern = re.compile(r'.+?\.(?<!config\.)' + taste + '$')

        template_files = {}

        # first we try the flavourdir if they have one specified.
        if config.has_key("flavourdir"):
            template_files = tools.Walk(self._request, config["flavourdir"], 1, pattern)

        # next we try the directory being requested and work our way
        # back to the datadir.
        if not template_files:
            datadir = config["datadir"]

            dirname = data["root_datadir"]
            if os.path.isfile(dirname):
                dirname = os.path.dirname(dirname)

            template_files = None
            while len(dirname) >= len(datadir):
                template_files = tools.Walk(self._request, dirname, 1, pattern)
                if template_files: break
                dirname = os.path.split(dirname)[0]

        # hmm...  guess we'll try the datadir.
        if not template_files:
            template_files = tools.Walk(self._request, config['datadir'], 1, pattern)

        # we grab a copy of the templates for the taste we want
        flavour = {}
        flavour.update(DEFAULT_FLAVOURS.get(taste, {}))

        # we update the flavours dict with what we found
        for filename in template_files:
            flavouring = os.path.basename(filename).split('.')
            flav_template = unicode(open(filename).read(), 
                    config.get('blog_encoding', 'iso-8859-1'))

            flavour[flavouring[0]] = flav_template

        if not flavour:
            return DEFAULT_FLAVOURS["error"]

        return flavour

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
            finaltext = tools.parse(self._request, self._encoding, entry, template)
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

        if data["content-type"].endswith("xml"):
            quotes = {"'": "&apos;", '"': "&quot;"}
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

        if entry["date"] and entry['date'] != current_date:
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
            output = tools.parse(self._request, self._encoding, self._content, self.flavour['story'])
            outputbuffer.append(output)

        elif content_type is type([]):
            current_date = ''

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

        self.write(tools.parse(self._request, self._encoding, entry, template))
            
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
