# vim: shiftwidth=4 tabstop=4 expandtab
import os, time, string, re, cgi
import tools
from entries.fileentry import FileEntry
import cPickle as pickle

class PyBlosxom:
    """
    This is the main class for PyBlosxom functionality.  It handles
    initialization, defines default behavior, and also pushes the
    request through all the steps until the output is rendered and
    we're complete.
    """
    def __init__(self, request):
        """
        Initializes the PyBlosxom class

        @param request: A L{libs.Request.Request} object
        @type request: L{libs.Request.Request} object
        """

        global myrequest
        myrequest = request

        self._request = request
        self.flavour = {}
        self.dayFlag = 1 # Used to print valid date footers

        registry = tools.get_registry()
        registry["request"] = request
        
    def startup(self):
        """
        The startup step further initializes the Request by setting
        additional information in the _data dict.
        """
        data = self._request.getData()
        pyhttp = self._request.getHttp()
        config = self._request.getConfiguration()

        data['pi_bl'] = ''

        # Get our URL and configure the base_url param
        if pyhttp.has_key('SCRIPT_NAME'):
            if not config.has_key('base_url'):
                config['base_url'] = 'http://%s%s' % (pyhttp['HTTP_HOST'], pyhttp['SCRIPT_NAME'])

            data['url'] = '%s%s' % (config['base_url'], data['pi_bl'])


    def defaultEntryParser(self, filename, request):
        """
        Open up a *.txt file and read its contents

        @param filename: A filename to extra data and meta data from
        @type filename: string
        @param request: A standard request object
        @type request: L{libs.Request.Request} object
        @returns: A dict containing parsed data and meta data with the particular
                file (and plugin)
        @rtype: dict
        """
        config = request.getConfiguration()

        entryData = {}

        try:
            story = file(filename).readlines()
        except IOError:
            raise IOError

        if len(story) > 0:
            entryData['title'] = story.pop(0).strip()

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


    def defaultFileListHandler(self, args):
        """
        This is the default handler for getting entries.  It takes the
        request object in and figures out which entries based on the
        default behavior that we want to show and generates a list of
        EntryBase subclass objects which it returns.

        @param args: dict containing the incoming Request object
        @type args: L{libs.Request.Request}

        @returns: the content we want to render
        @rtype: list of EntryBase objects
        """
        request = args["request"]

        data = request.getData()
        config = request.getConfiguration()
        pyhttp = request.getHttp()

        path_info = data['path_info']

        if data['bl_type'] == 'dir':
            filelist = tools.Walk(data['root_datadir'], int(config['depth']))
        elif data['bl_type'] == 'file':
            filelist = [data['root_datadir']]
        else:
            filelist = []

        entrylist = []
        for ourfile in filelist:
            entry = FileEntry(config, ourfile, data['root_datadir'])
            entrylist.append(entry)

        # this sorts entries by mtime in reverse order.  entries that have
        # no mtime get sorted to the top.
        BIGNUM = 2000000000
        entrylist.sort(lambda x,y: cmp(y.get("mtime", BIGNUM), x.get("mtime", BIGNUM)))
        
        # Match dates with files if applicable
        if data['pi_yr']:
            month = (data['pi_mo'] in tools.month2num.keys() and tools.month2num[data['pi_mo']] or data['pi_mo'])
            matchstr = "^" + data["pi_yr"] + month + data["pi_da"]
            valid_list = [x for x in entrylist if re.match(matchstr, x['fulltime'])]
        else:
            valid_list = entrylist

        return valid_list

    def processPathInfo(self, path_info):
        """ 
        Process path_info for URI according to path specifications, fill in
        data dict accordingly
        
        The paths specification looks like this:
            - C{/cat} - category
            - C{/2002} - year
            - C{/2002/Feb} (or 02) - Year and Month
            - C{/2002/Feb/03#entry} - Year, Month, Date, fragment id = entry name
            - C{/cat/2002/Feb/31} - year and month day in category.
            - C{/foo.html} and C{/cat/foo.html} - file foo.* in / and /cat
        To simplify checking, four digits directory name is not allowed.
        
        @param path_info: array of components of uri, typically obtained by C{uri.split("/")}
        @type path_info: list
        """
        config = self._request.getConfiguration()
        data = self._request.getData()

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
                    data['pi_da'] = path_info[0][0:2]
                    # grab date - must be 2 digits if there is a fragment 
                    # identifier #entryname, place that in "pi_frag"
                    # the fragment identifier won't appear when this code 
                    # is call via CGI, but will appear when called to 
                    # processing string URI's for pingback
                    match = re.search("(?P<frag>\#.+)",path_info[0])
                    if match != None and match.lastgroup == 'frag':
                        data['pi_frag'] = match.group('frag')
                    path_info.pop(0)

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
            def what_ext(path):
                for ext in data['extensions'].keys():
                    if os.path.isfile(path + '.' + ext):
                        return ext
                return None

            ext = what_ext(blog_result)
            if ext:
                config['blog_title'] += ' : %s' % data['pi_bl']
                data['bl_type'] = 'file'
                data['root_datadir'] = blog_result + '.' + ext
            else:
                # We may have flavour embedded here
                filename, ext = os.path.splitext(blog_result)
                fileext = what_ext(filename)
                dirname = os.path.dirname(filename)

                if fileext:
                    data['flavour'] = ext[1:]
                    data['root_datadir'] = filename + '.' + fileext
                    config['blog_title'] += ' : %s' % data['pi_bl']
                    data['bl_type'] = 'file'
                elif (os.path.basename(filename) == 'index' and 
                        os.path.isdir(dirname)):
                    # blanket flavours?
                    data['flavour'] = ext[1:]
                    if data['pi_bl'] != '':
                        config['blog_title'] += ' : %s' % os.path.dirname(data['pi_bl'])
                    data['root_datadir'] = dirname
                    data['bl_type'] = 'dir'
                    
    
    def run(self):
        """
        Main loop for pyblosxom.
        """
        config = self._request.getConfiguration()
        data = self._request.getData()
        pyhttp = self._request.getHttp()

        # instantiate the renderer with the current request and store it
        # in the data dict
        renderer = tools.importName('libs.renderers', 
                config.get('renderer', 'blosxom')).Renderer(self._request)
        data["renderer"] = renderer

        # import plugins
        import libs.plugins.__init__
        libs.plugins.__init__.initialize_plugins(config)
        
        # do start callback
        tools.run_callback("start", {'request': self._request}, mappingfunc=lambda x,y:y)

        # entryparser callback is runned first here to allow other plugins
        # register what file extensions can be used
        data['extensions'] = tools.run_callback("entryparser",
                                        {'txt': self.defaultEntryParser},
                                        mappingfunc=lambda x,y:y,
                                        defaultfunc=lambda x:x)

        form = self._request.getHttp()["form"]
        data['flavour'] = (form.has_key('flav') and 
                form['flav'].value or 
                config.get('defaultFlavour', 'html'))

        path_info = []
        data['pi_yr'] = ''
        data['pi_mo'] = ''
        data['pi_da'] = ''
        data['pi_frag'] = ''
        
        if pyhttp.get('PATH_INFO', ''):
            path_info = pyhttp['PATH_INFO'].split('/')

        # process the path info to determine what kind of blog entry(ies) 
        # this is
        self.processPathInfo(path_info)

        # call the filelist callback to generate a list of entries
        data["entry_list"] = tools.run_callback("filelist",
                                   {"request": self._request},
                                   donefunc=lambda x:x != None,
                                   defaultfunc=self.defaultFileListHandler)
        
        # we pass the request with the entry_list through the prepare callback
        # giving everyone a chance to transform the data.  the request is
        # modified in place.
        tools.run_callback("prepare", {"request": self._request})
        

        # now we pass the entry_list through the renderer
        entry_list = data["entry_list"]

        if renderer and not renderer.rendered:
            if entry_list:
                renderer.setContent(entry_list)
                # Log it as success
                tools.run_callback("logrequest", 
                        {'filename':config.get('logfile',''), 
                         'return_code': '200', 
                         'request': self._request})
            else:
                renderer.addHeader(['Status: 404 Not Found'])
                renderer.setContent(
                    {'title': 'The page you are looking for is not available',
                     'body': 'Somehow I cannot find the page you want. ' + 
                     'Go Back to <a href="%s">%s</a>?' 
                     % (config["base_url"], config["blog_title"])})
                # Log it as failure
                tools.run_callback("logrequest", 
                        {'filename':config.get('logfile',''), 
                         'return_code': '404', 
                         'request': self._request})
            renderer.render()
            # do end callback
            tools.run_callback("end", {'request':self._request}, mappingfunc=lambda x,y:y)

        elif not renderer:
            print "Content-Type: text/plain\n\nThere is something wrong with your setup"
