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
    def __init__(self, request, xmlRpcCall=0):
        global myrequest
        myrequest = request

        self._request = request
        self.xmlRpcCall = xmlRpcCall
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


    def defaultFileListHandler(self, request):
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
        data = request.getData()
        config = request.getConfiguration()
        pyhttp = request.getHttp()

        path_info = data['path_info']

        # Python is unforgiving as perl in this case
        data['pi_yr'] = (len(path_info) > 0 and path_info.pop(0) or '')
        data['pi_mo'] = (len(path_info) > 0 and path_info.pop(0) or '')
        data['pi_da'] = (len(path_info) > 0 and path_info.pop(0) or '')

        if data['bl_type'] == 'dir':
            filelist = tools.Walk(data['root_datadir'], int(config['depth']))
        else:
            filelist = [data['root_datadir']]

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
        
        # CGI command handling
        tools.cgiRequest(self._request)

        # If we use XML-RPC, we don't need favours and GET/POST fields
        if not self.xmlRpcCall:
            form = self._request.getHttp()["form"]
            data['flavour'] = (form.has_key('flav') and form['flav'].value or 'html')

            path_info = []

            # Get the blog name if possible
            if pyhttp.get('PATH_INFO', ''):
                path_info = pyhttp['PATH_INFO'].split('/')
                if path_info[0] == '':
                    path_info.pop(0)

                while re.match(r'^[a-zA-Z]\w*', path_info[0]):
                    data['pi_bl'] += '/%s' % path_info.pop(0)
                    if len(path_info) == 0:
                        break

            data['path_info'] = list(path_info)

            data['root_datadir'] = config['datadir']
            if os.path.isdir(config['datadir'] + data['pi_bl']):
                if data['pi_bl'] != '':
                    config['blog_title'] += ' : %s' % data['pi_bl']
                data['root_datadir'] = config['datadir'] + data['pi_bl']
                data['bl_type'] = 'dir'

            elif os.path.isfile(config['datadir'] + data['pi_bl'] + '.txt'):
                config['blog_title'] += ' : %s' % re.sub(r'/[^/]+$','',data['pi_bl'])
                data['bl_type'] = 'file'
                data['root_datadir'] = "%s%s.txt" % (config['datadir'], data['pi_bl'])

            else:
                filename, ext = os.path.splitext(data['pi_bl'])
                probableFile = config['datadir'] + filename + '.txt'

                if ext and os.path.isfile(probableFile):
                    data['flavour'] = ext[1:]
                    data['root_datadir'] = probableFile
                    config['blog_title'] += ' : %s' % filename
                    data['bl_type'] = 'file'
                else:
                    data['pi_bl'] = ''
                    data['bl_type'] = 'dir'

        # calling fileList will generate a list of entries from the
        # api.fileListHandler
        data["entry_list"] = tools.fileList(self._request)
        
        # we pass the request with the entry_list through the
        # plugins giving them a chance to transform the data.
        # plugins modify the request in-place--no need to return
        # things.
        api.prepareChain.executeHandler((self._request,))
        

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
