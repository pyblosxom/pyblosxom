"""
This is the main module for PyBlosxom functionality.  PyBlosxom's setup 
and default handlers are defined here.
"""
from __future__ import nested_scopes
import os, time, re, sys, StringIO
import tools
from entries.fileentry import FileEntry

VERSION = "1.0.0"
VERSION_DATE = VERSION + " (May 24, 2004)"
VERSION_SPLIT = tuple(VERSION.split('.'))

class PyBlosxom:
    """
    This is the main class for PyBlosxom functionality.  It handles
    initialization, defines default behavior, and also pushes the
    request through all the steps until the output is rendered and
    we're complete.
    """
    def __init__(self, request):
        """
        Sets the request.

        @param request: A L{Pyblosxom.pyblosxom.Request} object
        @type request: L{Pyblosxom.pyblosxom.Request} object
        """
        self._request = request

    def initialize(self):
        """
        The initialize step further initializes the Request by setting
        additional information in the _data dict, registering plugins,
        and entryparsers.
        """
        global VERSION_DATE

        data = self._request.getData()
        pyhttp = self._request.getHttp()
        config = self._request.getConfiguration()

        data["pyblosxom_version"] = VERSION_DATE
        data['pi_bl'] = ''

        # Get our URL and configure the base_url param
        if pyhttp.has_key('SCRIPT_NAME'):
            if not config.has_key('base_url'):
                config['base_url'] = 'http://%s%s' % (pyhttp['HTTP_HOST'], pyhttp['SCRIPT_NAME'])
        else:
            config['base_url'] = config.get('base_url', '')

        if config["datadir"].endswith("\\") or config["datadir"].endswith("/"):
            config['datadir'] = config['datadir'][:-1]

        # import and initialize plugins
        import plugin_utils
        plugin_utils.initialize_plugins(config.get("plugin_dirs", []), config.get("load_plugins", None))

        # entryparser callback is run here first to allow other plugins
        # register what file extensions can be used
        data['extensions'] = tools.run_callback("entryparser",
                                        {'txt': blosxom_entry_parser},
                                        mappingfunc=lambda x,y:y,
                                        defaultfunc=lambda x:x)

    def run(self):
        """
        Main loop for pyblosxom.  This should be called _after_
        initialization.  This method will run the handle callback
        to allow registered handlers to handle the request.  If nothing
        handles the request, then we use the default_blosxom_handler.
        """
        self.initialize()

        # run the start callback
        tools.run_callback("start", {'request': self._request})

        data = self._request.getData()
        pyhttp = self._request.getHttp()
        config = self._request.getConfiguration()

        # allow anyone else to handle the request at this point
        handled = tools.run_callback("handle", 
                        {'request': self._request},
                        mappingfunc=lambda x,y:x,
                        donefunc=lambda x:x)

        if not handled == 1:
            blosxom_handler(self._request)

        # do end callback
        tools.run_callback("end", {'request': self._request})


    def runCallback(self, callback="help"):
        """
        Generic method to run the engine for a specific callback
        """
        self.initialize()

        # run the start callback
        tools.run_callback("start", {'request': self._request})

        config = self._request.getConfig()
        data = self._request.getData()

        # invoke all callbacks for the 'callback'
        handled = tools.run_callback(callback,
                        {'request': self._request},
                        mappingfunc=lambda x,y:x,
                        donefunc=lambda x:x)

        # do end callback
        tools.run_callback("end", {'request': request})


    def runStaticRenderer(self, incremental=0):
        """
        This will go through all possible things in the blog
        and statically render everything to the "static_dir"
        specified in the config file.

        This figures out all the possible path_info settings
        and calls self.run() a bazillion times saving each file.

        @param incremental: whether (1) or not (0) to incrementally
            render the pages.  if we're incrementally rendering pages,
            then we render only the ones that have changed.
        @type  incremental: boolean
        """
        self.initialize()

        config = self._request.getConfiguration()
        data = self._request.getData()
        print "Performing static rendering."
        if incremental:
            print "Incremental is set."

        staticdir = config.get("static_dir", "")
        datadir = config["datadir"]

        if not staticdir:
            raise Exception("You must set static_dir in your config file.")

        flavours = config.get("static_flavours", ["html"])

        renderme = []

        monthnames = config.get("static_monthnames", 1)
        monthnumbers = config.get("static_monthnumbers", 0)

        dates = {}
        categories = {}

        # first we handle entries and categories
        listing = tools.Walk(self._request, datadir)

        for mem in listing:
            # skip the ones that have bad extensions
            ext = mem[mem.rfind(".")+1:]
            if not ext in data["extensions"].keys():
                continue

            # grab the mtime of the entry file
            mtime = time.mktime(tools.filestat(self._request, mem))

            # remove the datadir from the front and the bit at the end
            mem = mem[len(datadir):mem.rfind(".")]

            # this is the static filename
            fn = os.path.normpath(staticdir + mem)

            # grab the mtime of one of the statically rendered file
            try:
                smtime = os.stat(fn + "." + flavours[0])[8]
            except:
                smtime = 0

            # if the entry is more recent than the static, we want to re-render
            if smtime < mtime or not incremental:

                # grab the categories
                temp = os.path.dirname(mem).split(os.sep)
                for i in range(len(temp)+1):
                    p = os.sep.join(temp[0:i])
                    categories[p] = 0

                # grab the date
                mtime = time.localtime(mtime)
                year = time.strftime("%Y", mtime)
                month = time.strftime("%m", mtime)
                day = time.strftime("%d", mtime)

                dates[year] = 1

                if monthnumbers:
                    dates[year + "/" + month] = 1
                    dates[year + "/" + month + "/" + day] = 1

                if monthnames:
                    monthname = tools.num2month[month]
                    dates[year + "/" + monthname] = 1
                    dates[year + "/" + monthname + "/" + day] = 1

                # toss in the render queue
                for f in flavours:
                    renderme.append( (mem + "." + f, "") )

        print "rendering %d entries." % len(renderme)

        # handle categories
        categories = categories.keys()
        categories.sort()

        print "rendering %d category indexes." % len(categories)

        for mem in categories:
            mem = os.path.normpath( mem + "/index." )
            for f in flavours:
                renderme.append( (mem + f, "") )

        # now we handle dates
        dates = dates.keys()
        dates.sort()

        print "rendering %d date indexes." % len(dates)

        for mem in dates:
            mem = os.path.normpath( mem + "/index." )
            for f in flavours:
                renderme.append( (mem + f, "") )
            
        # now we handle arbitrary urls
        additional_stuff = config.get("static_urls", [])
        print "rendering %d arbitrary urls." % len(additional_stuff)

        for mem in additional_stuff:
            if mem.find("?") != -1:
                url = mem[:mem.find("?")]
                query = mem[mem.find("?")+1:]
            else:
                url = mem
                query = ""

            renderme.append( (url, query) )

        # now we pass the complete render list to all the plugins
        # via cb_staticrender_filelist and they can add to the filelist
        # any ( url, query ) tuples they want rendered.
        print "(before) building %s files." % len(renderme)
        handled = tools.run_callback("staticrender_filelist",
                        {'request': self._request, 
                         'filelist': renderme,
                         'flavours': flavours})

        print "building %s files." % len(renderme)

        for url, q in renderme:
            print "rendering '%s' ..." % url
            tools.render_url(config, url, q)


class Request:
    """
    This class holds the PyBlosxom request.  It holds configuration
    information, HTTP/CGI information, and data that we calculate
    and transform over the course of execution.

    There should be only one instance of this class floating around
    and it should get created by pyblosxom.cgi and passed into the
    PyBlosxom instance which will do further manipulation on the
    Request instance.
    """
    def __init__(self):
        # this holds configuration data that the user changes 
        # in config.py
        self._configuration = {}

        # this holds HTTP/CGI oriented data specific to the request
        # and the environment in which the request was created
        self._http = {}

        # this holds run-time data which gets created and transformed
        # by pyblosxom during execution
        self._data = {}

    def getConfiguration(self):
        """
        Returns the _actual_ configuration dict.  The configuration
        dict holds values that the user sets in their config.py file.

        Modifying the contents of the dict will affect all downstream 
        processing.

        @returns: dict
        """
        return self._configuration

    def getHttp(self):
        """
        Returns the _actual_ http dict.   Holds HTTP/CGI data derived 
        from the environment of execution.

        Modifying the contents of the dict will affect all downstream 
        processing. 

        @returns: dict
        """
        return self._http

    def getData(self):
        """
        Returns the _actual_ data dict.   Holds run-time data which is 
        created and transformed by pyblosxom during execution.

        Modifying the contents of the dict will affect all downstream 
        processing. 

        @returns: dict
        """
        return self._data

    def dumpRequest(self):
        # some dumping method here?  pprint?
        pass

    def __populateDict(self, currdict, newdict):
        for mem in newdict.keys():
            currdict[mem] = newdict[mem]

    def addHttp(self, d):
        """
        Takes in a dict and adds/overrides values in the existing
        http dict with the new values.

        @param d: the dict with the new keys/values to add
        @type  d: dict
        """
        self.__populateDict(self._http, d)

    def addData(self, d):
        """
        Takes in a dict and adds/overrides values in the existing
        data dict with the new values.

        @param d: the dict with the new keys/values to add
        @type  d: dict
        """
        self.__populateDict(self._data, d)

    def addConfiguration(self, d):
        """
        Takes in a dict and adds/overrides values in the existing
        configuration dict with the new values.

        @param d: the dict with the new keys/values to add
        @type  d: dict
        """
        self.__populateDict(self._configuration, d)

    def __getattr__(self, name, default=None):
        """
        Sort of simulates the dict except we only have three
        valid attributes: config, data, and http.

        @param name: the name of the attribute to get
        @type  name: string

        @param default: varies
        @type  default: varies
        """
        if name in ["config", "configuration", "conf"]:
            return self._configuration

        if name == "data":
            return self._data

        if name == "http":
            return self._http

        return default

    def __repr__(self):
        return "Request"


def blosxom_handler(request):
    """
    This is the default blosxom handler.
    """
    import cgi

    config = request.getConfiguration()
    data = request.getData()

    # go through the renderer callback to see if anyone else
    # wants to render.  this renderer gets stored in the data dict 
    # for downstream processing.
    r = tools.run_callback('renderer', 
                           {'request': request},
                           donefunc = lambda x: x != None, 
                           defaultfunc = lambda x: None)

    if not r:
        # get the renderer we want to use
        r = config.get("renderer", "blosxom")

        # import the renderer
        r = tools.importName("Pyblosxom.renderers", r)

        # get the renderer object
        r = r.Renderer(request, config.get("stdoutput", sys.stdout))

    data['renderer'] = r

    request.addHttp( {"form": cgi.FieldStorage() } )
    # process the path info to determine what kind of blog entry(ies) 
    # this is
    tools.run_callback("pathinfo",
                           {"request": request},
                           donefunc=lambda x:x != None,
                           defaultfunc=blosxom_process_path_info)

    # call the filelist callback to generate a list of entries
    data["entry_list"] = tools.run_callback("filelist",
                               {"request": request},
                               donefunc=lambda x:x != None,
                               defaultfunc=blosxom_file_list_handler)
    
    # we pass the request with the entry_list through the prepare callback
    # giving everyone a chance to transform the data.  the request is
    # modified in place.
    tools.run_callback("prepare", {"request": request})

    # now we pass the entry_list through the renderer
    entry_list = data["entry_list"]
    renderer = data['renderer']

    if renderer and not renderer.rendered:
        if entry_list:
            renderer.setContent(entry_list)
            # Log it as success
            tools.run_callback("logrequest", 
                    {'filename':config.get('logfile',''), 
                     'return_code': '200', 
                     'request': request})
        else:
            renderer.addHeader('Status', '404 Not Found')
            renderer.setContent(
                {'title': 'The page you are looking for is not available',
                 'body': 'Somehow I cannot find the page you want. ' + 
                 'Go Back to <a href="%s">%s</a>?' 
                 % (config["base_url"], config["blog_title"])})
            # Log it as failure
            tools.run_callback("logrequest", 
                    {'filename':config.get('logfile',''), 
                     'return_code': '404', 
                     'request': request})
        renderer.render()

    elif not renderer:
        output = config.get('stdoutput', sys.stdout)
        output.write("Content-Type: text/plain\n\nThere is something wrong with your setup.\n  Check your config files and verify that your configuration is correct.\n")


def blosxom_entry_parser(filename, request):
    """
    Open up a *.txt file and read its contents.  The first line
    becomes the title of the entry.  The other lines are the
    body of the entry.

    @param filename: A filename to extract data and metadata from
    @type filename: string

    @param request: A standard request object
    @type request: L{Pyblosxom.pyblosxom.Request} object

    @returns: A dict containing parsed data and meta data with the 
            particular file (and plugin)
    @rtype: dict
    """
    config = request.getConfiguration()

    entryData = {}

    try:
        story = open(filename).readlines()
    except IOError:
        raise IOError

    if len(story) > 0:
        entryData['title'] = story.pop(0).strip()

    # this handles properties of the entry that are between
    # the title and the body and start with a #
    while len(story) > 0:
        match = re.match(r'^#(\w+)\s+(.*)', story[0])
        if match:
            story.pop(0)
            entryData[match.groups()[0]] = match.groups()[1].strip()
        else:
            break

    # Call the preformat function
    entryData['body'] = tools.run_callback('preformat',
            {'parser': (entryData.get('parser', '') 
                    or config.get('parser', 'plain')),
             'story': story,
             'request': request},
            donefunc = lambda x:x != None,
            defaultfunc = lambda x: ''.join(x['story']))

    # Call the postformat callbacks
    tools.run_callback('postformat',
            {'request': request,
             'entry_data': entryData})
        
    return entryData


def blosxom_file_list_handler(args):
    """
    This is the default handler for getting entries.  It takes the
    request object in and figures out which entries based on the
    default behavior that we want to show and generates a list of
    EntryBase subclass objects which it returns.

    @param args: dict containing the incoming Request object
    @type args: L{Pyblosxom.pyblosxom.Request}

    @returns: the content we want to render
    @rtype: list of EntryBase objects
    """
    request = args["request"]

    data = request.getData()
    config = request.getConfiguration()

    if data['bl_type'] == 'dir':
        filelist = tools.Walk(request, data['root_datadir'], int(config['depth']))
    elif data['bl_type'] == 'file':
        filelist = [data['root_datadir']]
    else:
        filelist = []

    entrylist = []
    for ourfile in filelist:
        entry = FileEntry(request, ourfile, data['root_datadir'])
        entrylist.append((entry._mtime, entry))

    # this sorts entries by mtime in reverse order.  entries that have
    # no mtime get sorted to the top.
    entrylist.sort()
    entrylist.reverse()
    entrylist = [x[1] for x in entrylist]
    
    # Match dates with files if applicable
    if data['pi_yr']:
        month = (data['pi_mo'] in tools.month2num.keys() and tools.month2num[data['pi_mo']] or data['pi_mo'])
        matchstr = "^" + data["pi_yr"] + month + data["pi_da"]
        valid_list = [x for x in entrylist if re.match(matchstr, x['fulltime'])]
    else:
        valid_list = entrylist

    return valid_list

def blosxom_process_path_info(args):
    """ 
    Process HTTP PATH_INFO for URI according to path specifications, fill in
    data dict accordingly
    
    The paths specification looks like this:
        - C{/cat} - category
        - C{/2002} - year
        - C{/2002/Feb} (or 02) - Year and Month
        - C{/cat/2002/Feb/31} - year and month day in category.
        - C{/foo.html} and C{/cat/foo.html} - file foo.* in / and /cat
    To simplify checking, four digits directory name is not allowed.

    @param args: dict containing the incoming Request object
    @type args: L{Pyblosxom.pyblosxom.Request}
    """
    request = args['request']
    config = request.getConfiguration()
    data = request.getData()
    pyhttp = request.getHttp()

    form = pyhttp["form"]
    data['flavour'] = (form.has_key('flav') and form['flav'].value or 
            config.get('defaultFlavour', 'html'))

    path_info = []
    data['pi_yr'] = ''
    data['pi_mo'] = ''
    data['pi_da'] = ''
    
    if pyhttp.get('PATH_INFO', ''):
        path_info = pyhttp['PATH_INFO'].split('/')
    path_info = [x for x in path_info if x != '']

    data['path_info'] = list(path_info)
    data['root_datadir'] = config['datadir']

    got_date = 0
    for path_data in path_info:
        if not path_data:
            continue
        elif len(path_data) == 4 and path_data.isdigit():
            # We got a hot date here guys :)
            got_date = 1
            break
        else:
            data['pi_bl'] = os.path.join(data['pi_bl'], path_data)

    if got_date:
        # Get messy with dates
        while not (len(path_info[0]) == 4 and path_info[0].isdigit()):
            path_info.pop(0)
        # Year
        data['pi_yr'] = path_info.pop(0)
        # Month
        if path_info and path_info[0] in tools.MONTHS:
            data['pi_mo'] = path_info.pop(0)
            # Day
            if path_info and re.match("^([0-2][0-9]|3[0-1])", path_info[0]):
                # Potential day here
                data['pi_da'] = path_info.pop(0)

        if path_info and path_info[0]:
            # Potential flavour after date
            filename, ext = os.path.splitext(path_info[0])
            if filename == 'index':
                data['flavour'] = ext[1:]

    blog_result = os.path.join(config['datadir'], data['pi_bl'])
    
    data['bl_type'] = ''

    # If all we've got is a directory, things are simple
    if os.path.isdir(blog_result):
        if data['pi_bl'] != '':
            config['blog_title'] += ' : %s' % data['pi_bl']
        data['root_datadir'] = blog_result
        data['bl_type'] = 'dir'

    # Else we may have a file
    if not data['bl_type']:
        # Try for file

        ext = tools.what_ext(data["extensions"].keys(), blog_result)
        if ext:
            config['blog_title'] += ' : %s' % data['pi_bl']
            data['bl_type'] = 'file'
            data['root_datadir'] = blog_result + '.' + ext

        else:
            # We may have flavour embedded here
            filename, ext = os.path.splitext(blog_result)
            fileext = tools.what_ext(data["extensions"].keys(), filename)
            dirname = os.path.dirname(filename)

            if fileext:
                data['flavour'] = ext[1:]
                data['root_datadir'] = filename + '.' + fileext
                config['blog_title'] += ' : %s' % data['pi_bl']
                data['bl_type'] = 'file'

            elif (os.path.basename(filename) == 'index' and os.path.isdir(dirname)):
                # blanket flavours?
                data['flavour'] = ext[1:]
                if data['pi_bl'] != '':
                    config['blog_title'] += ' : %s' % os.path.dirname(data['pi_bl'])
                data['root_datadir'] = dirname
                data['bl_type'] = 'dir'
                
    # Construct our final URL
    data['url'] = '%s/%s' % (config['base_url'], data['pi_bl'])


def test_installation(request):
    """
    This function gets called when someone starts up pyblosxom.cgi
    from the command line with no REQUEST_METHOD environment variable.

    It:

      1. tests properties in their config.py file
      2. verifies they have a datadir and that it exists
      3. initializes all the plugins they have installed
      4. runs "cb_verify_installation"--plugins can print out whether
         they are installed correctly (i.e. have valid config property
         settings and can read/write to data files)
      5. exits

    The goal is to be as useful and informative to the user as we can be
    without being overly verbose and confusing.

    This is designed to make it much much much easier for a user to
    verify their PyBlosxom installation is working and also to install
    new plugins and verify that their configuration is correct.
    """
    import sys, os, os.path
    from Pyblosxom import pyblosxom

    config = request.getConfiguration()

    # BASE STUFF
    print "Welcome to PyBlosxom's installation verification system."
    print "------"
    print "]] printing diagnostics [["
    print "pyblosxom:   %s" % pyblosxom.VERSION_DATE
    print "sys.version: %s" % sys.version.replace("\n", " ")
    print "os.name:     %s" % os.name
    print "codebase:    %s" % config.get("codebase", "--default--")
    print "------"

    # CONFIG FILE
    print "]] checking config file [["
    print "config has %s properties set." % len(config)
    print ""
    required_config = ["datadir"]

    nice_to_have_config = ["blog_title", "blog_author", "blog_description",
                           "blog_language", "blog_encoding", 
                           "base_url", "depth", "num_entries", "renderer", 
                           "cacheDriver", "cacheConfig", "plugin_dirs", 
                           "load_plugins"]
    missing_properties = 0
    for mem in required_config:
        if not config.has_key(mem):
            print "   missing required property: '%s'" % mem
            missing_properties = 1

    for mem in nice_to_have_config:
        if not config.has_key(mem):
            print "   missing optional property: '%s'" % mem

    print ""
    print "Refer to the documentation for what properties are available"
    print "and what they do."

    if missing_properties:
        print ""
        print "Missing properties must be set in order for your blog to"
        print "work."
        print ""
        print "This must be done before we can go further.  Exiting."
        return

    print "PASS: config file is fine."

    print "------"
    print "]] checking datadir [["

    # DATADIR
    # FIXME - we should check permissions here?
    if not os.path.isdir(config["datadir"]):
        print "datadir '%s' does not exist." % config["datadir"]          
        print "You need to create your datadir and give it appropriate"
        print "permissions."
        print ""
        print "This must be done before we can go further.  Exiting."
        return

    print "PASS: datadir is fine."

    print "------"
    print "Now we're going to verify your plugin configuration."

    if config.has_key("plugin_dirs"):

        from Pyblosxom import plugin_utils
        plugin_utils.initialize_plugins(config["plugin_dirs"],
                                        config.get("load_plugins", None))

        no_verification_support = []

        for mem in plugin_utils.plugins:
            if "verify_installation" in dir(mem):
                print "=== plugin: '%s'" % mem.__name__
                print "    file: %s" % mem.__file__

                if "__version__" in dir(mem):
                    print "    version: %s" % mem.__version__
                else:
                    print "    plugin has no version."

                try:
                    if mem.verify_installation(request) == 1:
                        print "    PASS"
                    else:
                        print "    FAIL!!!"
                except AssertionError, error_message:
                    print " FAIL!!! ", error_message

            else:
                no_verification_support.append( "'%s' (%s)" % (mem.__name__, mem.__file__))

        if len(no_verification_support) > 0:
            print ""
            print "The following plugins do not support installation verification:"
            for mem in no_verification_support:
                print "   %s" % mem
    else:
        print "You have chosen not to load any plugins."

# vim: shiftwidth=4 tabstop=4 expandtab
