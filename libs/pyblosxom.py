# vim: shiftwidth=4 tabstop=4 expandtab
import os, time, string, re, cgi
import tools, api
from entries.fileentry import FileEntry
from entries.cachedecorator import CacheDecorator
import cPickle as pickle

class PyBlosxom:
    """
    This is the main class for PyBlosxom functionality.  It handles
    initialization, defines default behavior, and also pushes the
    request through all the steps until the output is rendered and
    we're complete.
    """
    def __init__(self, request):
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


    def defaultFileListHandler(self, args):
        """
        This is the default handler for getting entries.  It takes the
        request object in and figures out which entries based on the
        default behavior that we want to show and generates a list of
        EntryBase subclass objects which it returns.

        @param request: the incoming Request object
        @type request: libs.Request.Request

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
            entry = CacheDecorator(FileEntry(config, ourfile, data['root_datadir']))
            entrylist.append(entry)
        entrylist = tools.sortDictBy(entrylist, "mtime")
        
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
        Process path_info for URI according to path specifications, fill in data dict accordingly

        @param: path_info
        @type: array of components of uri, typically obtained by uri.split("/")
        
        The paths specification looks like this:
        /cat - category
        /2002 - year
        /2002/Feb (or 02) - Year and Month
        /2002/Feb/03#entry - Year, Month, Date, fragment id = entry name
        /cat/2002/Feb/31 - year and month day in category.
        /foo.html and /cat/foo.html - file foo.* in / and /cat
        To simplify checking, four digits directory name is not allowed.
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
                    data['pi_da'] = path_info[0][0:2] # grab date - must be 2 digits
                    # if there is a fragment identifier #entryname, place that in "pi_frag"
                    # the fragment identifier won't appear when this code is call via CGI, but
                    # will appear when called to processing string URI's for pingback
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

        # import entryparsers here to allow other plugins register what file
        # extensions can be used
        import libs.entryparsers.__init__
        libs.entryparsers.__init__.initialize_extensions()
        data['extensions'] = libs.entryparsers.__init__.ext
        
        # import plugins and allow them to register with the api
        import libs.plugins.__init__
        libs.plugins.__init__.initialize_plugins(config)

        api.fileListHandler.register(self.defaultFileListHandler, api.LAST)
        
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

        # process the path info to determine what kind of blog entry(ies) this is
        self.processPathInfo(path_info)

        # calling fileList will generate a list of entries from the
        # api.fileListHandler
        data["entry_list"] = tools.fileList(self._request)
        
        # we pass the request with the entry_list through the
        # plugins giving them a chance to transform the data.
        # plugins modify the request in-place--no need to return
        # things.
        api.prepareChain.executeHandler({"request": self._request})
        

        # now we pass the entry_list through the renderer
        entry_list = data["entry_list"]

        if renderer and not renderer.rendered:
            if entry_list:
                renderer.setContent(entry_list)
                tools.logRequest(config.get('logfile',''), '200')
            else:
                renderer.addHeader(['Status: 404 Not Found'])
                renderer.setContent(
                    {'title': 'The page you are looking for is not available',
                     'body': 'Somehow I cannot find the page you want. ' + 
                     'Go Back to <a href="%s">%s</a>?' 
                     % (config["base_url"], config["blog_title"])})
                tools.logRequest(config.get('logfile',''), '404')
            renderer.render()

        elif not renderer:
            print "Content-Type: text/plain\n\nThere is something wrong with your setup"
