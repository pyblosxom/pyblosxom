"""
This is the default renderer.  It tries to match the behavior of the
blosxom renderer.
"""

from Pyblosxom import tools
from Pyblosxom.renderers.base import RendererBase
import re, os, sys, codecs

class NoSuchFlavourException(Exception):
    def __init__(self, msg):
        self._msg = msg

def get_included_flavour(taste):
    """
    PyBlosxom comes with flavours in taste.flav directories in the flavours
    subdirectory of the Pyblosxom package.  This method pulls the template
    files for the associated taste (assuming it exists) or None if it
    doesn't.

    @param taste The name of the taste.  e.g. "html", "rss", ...
    @type  taste string

    @returns The list of template full filenames or None
    @rtype list of strings or None
    """
    template_files = None

    path = __file__[:__file__.rfind(os.sep)]
    path = path[:path.rfind(os.sep)+1] + "flavours" + os.sep

    path = path + taste + ".flav"

    if os.path.isdir(path):
        template_files = os.listdir(path)
        template_files = [path + os.sep + m for m in template_files if m.endswith("." + taste)]

    return template_files

def get_flavour_from_dir(path, taste):
    template_files = None
    # if we have a taste.flav directory, we check there
    if os.path.isdir(path + os.sep + taste + ".flav"):
        newpath = path + os.sep + taste + ".flav"
        template_files = os.listdir(newpath)
        template_files = [newpath + os.sep + m for m in template_files if m.endswith("." + taste)]

    # now we check the directory itself for flavour templates
    if not template_files:
        template_files = os.listdir(path)
        template_files = [path + os.sep + m for m in template_files if m.endswith("." + taste)]

    return template_files

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
        datadir = config["datadir"]

        pattern = re.compile(r'.+?\.(?<!config\.)' + taste + '$')

        template_files = {}

        # if they have flavourdir set, then we look there.  otherwise
        # we look in the datadir
        flavourdir = config.get("flavourdir", datadir)

        # walk through the request looking in directory hierarchies
        # until we find the templates we want.

        dirname = data["root_datadir"]
        if os.path.isfile(dirname):
            dirname = os.path.dirname(dirname)

        # the dirname at this point is a complete file path.  so we need to
        # pluck the datadir portion off the front reducing it to a category
        dirname = dirname[len(datadir):]

        template_files = None
        while len(dirname) > 0:
            path = flavourdir + dirname

            template_files = get_flavour_from_dir(path, taste)

            # if we found template files, then we break out and move along
            if len(template_files) > 0:
                break

            # otherwise we peel off another piece of the category and continue
            # looping
            newdirname = os.path.split(dirname)[0]
            if newdirname == dirname:
                break
            dirname = newdirname

        # we haven't found the flavour files yet, so we try the root
        if not template_files:
            template_files = get_flavour_from_dir(flavourdir, taste)

        # if we haven't found the template files yet, we check our
        # contributed flavours directory--these are always in taste.flav
        # directories
        if not template_files:
            template_files = get_included_flavour(taste)

        # if we still haven't found our flavour files, we raise an exception
        if not template_files:
            raise NoSuchFlavourException("Flavour '" + taste + "' does not exist.")

        # we grab a copy of the templates for the taste we want
        flavour = {}

        # we load the flavour templates into our flavour dict
        for filename in template_files:
            flavouring = os.path.basename(filename).split('.')
            flav_template = unicode(open(filename).read(), 
                    config.get('blog_encoding', 'iso-8859-1'))

            flavour[flavouring[0]] = flav_template

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

        if data['content-type'] == 'text/plain':
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

        if callable(self._content):
            # if the content is a callable function, then we just spit out
            # whatever it returns as a string
            outputbuffer.append(self._content())

        elif isinstance(self._content, dict):
            # if the content is a dict, then we parse it as if it were an
            # entry--except it's distinctly not an EntryBase derivative
            self._content.update(data)
            output = tools.parse(self._request, self._encoding, self._content, self.flavour['story'])
            outputbuffer.append(output)

        elif isinstance(self._content, list):
            current_date = ''

            for entry in self._content:
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
        # if we've already rendered, then we don't want to do so again
        if self.rendered == 1:
            return

        data = self._request.getData()
        config = self._request.getConfiguration()

        # FIXME
        parsevars = tools.VariableDict()
        parsevars.update(config)
        parsevars.update(data)

        try:
            self.flavour = self._getFlavour(data.get("flavour", "html"))

        except NoSuchFlavourException, nsfe:
            error_msg = nsfe._msg
            try:
                self.flavour = self._getFlavour("error")
            except NoSuchFlavourException, nsfe2:
                self.flavour = get_included_flavour("error")
                error_msg = error_msg + "And your error flavour doesn't exist."

            self._content = { "title": "Flavour error", 
                              "body": error_msg }
        
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
