#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003, 2004, 2005, 2006 Wari Wahab
# 
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#
# $Id$
#######################################################################
"""
This is the default blosxom renderer.  It tries to match the behavior 
of the blosxom renderer.
"""

from Pyblosxom import tools
from Pyblosxom.renderers.base import RendererBase
import os, sys, codecs

class NoSuchFlavourException(Exception):
    """
    This exception gets thrown when the flavour requested is not
    available in this blog.
    """
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

    @returns A dict of template type to template file or None
    @rtype dict or None
    """
    path = __file__[:__file__.rfind(os.sep)]
    path = path[:path.rfind(os.sep)+1] + "flavours" + os.sep

    path = path + taste + ".flav"

    if os.path.isdir(path):
        template_files = os.listdir(path)
        template_d = {}
        for mem in template_files:
            if not mem.endswith("." + taste):
                continue
            template_d[os.path.splitext(mem)[0]] = path + os.sep + mem
        return template_d

    return None

def get_flavour_from_dir(path, taste):
    """
    Tries to get the template files for the flavour of a certain
    taste (html, rss, atom10, ...) in a directory.  The files could
    be in the directory or in a taste.flav subdirectory.

    @param path: the path of the directory to look for the flavour
                 templates in
    @type  path: string

    @param taste: the flavour files to look for (e.g. html, rss, atom10, ...)
    @type  taste: string

    @returns: the map of template name to template file path
    @rtype: map
    """
    template_d = {}

    # if we have a taste.flav directory, we check there
    if os.path.isdir(path + os.sep + taste + ".flav"):
        newpath = path + os.sep + taste + ".flav"
        template_files = os.listdir(newpath)
        for mem in template_files:
            if not mem.endswith("." + taste):
                continue
            template_d[os.path.splitext(mem)[0]] = newpath + os.sep + mem
        return template_d

    # now we check the directory itself for flavour templates
    template_files = os.listdir(path)
    for mem in template_files:
        if not mem.endswith("." + taste):
            continue
        template_d[os.path.splitext(mem)[0]] = path + os.sep + mem

    if template_d:
        return template_d

    return None

class BlosxomRenderer(RendererBase):
    """
    This is the default blosxom renderer.  It tries to match the behavior 
    of the blosxom renderer.
    """
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
        This retrieves all the template files for a given flavour taste.
        This will first pull the templates for the default flavour
        of this taste if there are any.  Then it looks at EITHER
        the configured datadir OR the flavourdir (if configured).  It'll
        go through directories overriding the template files it has
        already picked up descending the category path of the PyBlosxom
        request.

        For example, if the user requested the "html" flavour and is
        looking at an entry in the category "dev/pyblosxom", then
        _getFlavour will:

        1. pick up the flavour files in the default html flavour
        2. start in EITHER datadir OR flavourdir (if configured)
        3. override the default html flavour files with html flavour
           files in this directory or in html.flav/ subdirectory
        4. override the html flavour files it's picked up so far
           with html files in dev/ or dev/html.flav/
        5. override the html flavour files it's picked up so far
           with html files in dev/pyblosxom/ or 
           dev/pyblosxom/html.flav/

        If it doesn't find any flavour files at all, then it returns
        None which indicates the flavour doesn't exist in this blog.

        @param taste: the taste to retrieve flavour files for.
        @type  taste: string

        @returns: mapping of template name to template file data
        @rtype: map
        """
        data = self._request.getData()
        config = self._request.getConfiguration()
        datadir = config["datadir"]

        # if they have flavourdir set, then we look there.  otherwise
        # we look in the datadir.
        flavourdir = config.get("flavourdir", datadir)

        # first we grab the flavour files for the included flavour (if
        # we have one).
        template_d = get_included_flavour(taste)
        if not template_d:
            template_d = {}

        pathinfo = list(data["path_info"])

        # check the root of flavourdir for templates
        new_files = get_flavour_from_dir(flavourdir, taste)
        if new_files:
            template_d.update(new_files)

        # go through all the directories from the flavourdir all
        # the way up to the root_datadir.  this way template files
        # can override template files in parent directories.
        while len(pathinfo) > 0:
            flavourdir = os.path.join(flavourdir, pathinfo.pop(0))
            if os.path.isfile(flavourdir):
                break

            if not os.path.isdir(flavourdir):
                break

            new_files = get_flavour_from_dir(flavourdir, taste)
            if new_files:
                template_d.update(new_files)

        # if we still haven't found our flavour files, we raise an exception
        if not template_d:
            raise NoSuchFlavourException("Flavour '" + taste + "' does not exist.")

        for k in template_d.keys():
            flav_template = unicode(open(template_d[k]).read(), 
                    config.get('blog_encoding', 'iso-8859-1'))
            template_d[k] = flav_template

        return template_d

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

        @param current_date: the date of entries we're looking at
        @type  string

        @returns: the output string and the new current date
        @rtype: (string, string)
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
