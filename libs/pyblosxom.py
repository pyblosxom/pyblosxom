# vim: shiftwidth=4 tabstop=4 expandtab
import os, time, string, re, cgi
import tools, api
import cPickle as pickle

class PyBlosxom:
    def __init__(self, request, xmlRpcCall=0):
        self._request = request
        self.xmlRpcCall = xmlRpcCall
        self.flavour = {}
        self.dayFlag = 1 # Used to print valid date footers
        
    def startup(self):
        data = self._request.getData()
        pyhttp = self._request.getHttp()
        config = self._request.getConfiguration()

        data['pi_bl'] = ''
        path_info = []

        # If we use XML-RPC, we don't need favours and GET/POST fields
        if not self.xmlRpcCall:
            form = self._request.getHttp()["form"]
            data['flavour'] = (form.has_key('flav') and form['flav'].value or 'html')

            # Get the blog name if possible
            if pyhttp.get('PATH_INFO', ''):
                path_info = pyhttp['PATH_INFO'].split('/')
                if path_info[0] == '':
                    path_info.pop(0)
                while re.match(r'^[a-zA-Z]\w*', path_info[0]):
                    data['pi_bl'] += '/%s' % path_info.pop(0)
                    if len(path_info) == 0:
                        break

            data['root_datadir'] = config['datadir']
            if os.path.isdir(config['datadir'] + data['pi_bl']):
                if data['pi_bl'] != '':
                    config['blog_title'] += ' : %s' % data['pi_bl']
                data['root_datadir'] = config['datadir'] + data['pi_bl']
                data['bl_type'] = 'dir'

            elif os.path.isfile(config['datadir'] + data['pi_bl'] + '.txt'):
                config['blog_title'] += ' : %s' % re.sub(r'/[^/]+$','',data['pi_bl'])
                data['bl_type'] = 'file'
                data['root_datadir'] = config['datadir'] + data['pi_bl'] + '.txt'

            else:
                match = re.search(r'\.(\w+)$',data['pi_bl'])
                probableFile = config['datadir'] + re.sub(r'\.\w+$','',data['pi_bl']) + '.txt'
                if match and os.path.isfile(probableFile):
                    data['flavour'] = match.groups()[0]
                    data['root_datadir'] = probableFile
                    config['blog_title'] += ' : %s' % re.sub(r'/[^/]+\.\w+$','',data['pi_bl'])
                    data['bl_type'] = 'file'
                else:
                    data['pi_bl'] = ''
                    data['bl_type'] = 'dir'

        # Get our URL
        if pyhttp.has_key('SCRIPT_NAME'):
            if not config.has_key('base_url'):
                config['base_url'] = 'http://%s%s' % (pyhttp['HTTP_HOST'], pyhttp['SCRIPT_NAME'])

            data['url'] = '%s%s' % (config['base_url'], data['pi_bl'])

        # Python is unforgiving as perl in this case
        data['pi_yr'] = (len(path_info) > 0 and path_info.pop(0) or '')
        data['pi_mo'] = (len(path_info) > 0 and path_info.pop(0) or '')
        data['pi_da'] = (len(path_info) > 0 and path_info.pop(0) or '')

    def getProperties(self, filename, root):
        """Returns a dictionary of file related contents"""
        config = self._request.getConfiguration()

        mtime = tools.filestat(filename)[8]
        timetuple = time.localtime(mtime)
        path = string.replace(filename, root, '')
        path = string.replace(path, os.path.basename(filename), '')
        path = path[1:][:-1]
        absolute_path = string.replace(filename, config['datadir'], '')
        absolute_path = string.replace(absolute_path, os.path.basename(filename), '')
        absolute_path = absolute_path[1:][:-1]
        fn = re.sub(r'\.txt$', '', os.path.basename(filename))
        if absolute_path == '':
            file_path = fn
        else:
            file_path = absolute_path+'/'+fn
        tb = '-'
        tb_id = '%s/%s' % (absolute_path, fn)
        tb_id = re.sub(r'[^A-Za-z0-9]', '_', tb_id)
        if os.path.isfile('%s/%s.stor' % (config.get('tb_data', ''), tb_id)):
            tb = '+'

        return {'mtime' : mtime, 
                'path' : path,
                'tb' : tb,
                'tb_id' : tb_id,
                'absolute_path' : absolute_path,
                'file_path' : file_path,
                'fn' : fn,
                'filename' : filename,
                'ti' : time.strftime('%H:%M',timetuple),
                'mo' : time.strftime('%b',timetuple),
                'mo_num' : time.strftime('%m',timetuple),
                'da' : time.strftime('%d',timetuple),
                'yr' : time.strftime('%Y',timetuple),
                'timetuple' : timetuple,
                'fulltime' : time.strftime('%Y%m%d%H%M%S',timetuple),
                'w3cdate' : time.strftime('%Y-%m-%dT%H:%M:%S%Z',timetuple), # YYYY-MM-DDThh:mm:ssTZD
                'date' : time.strftime('%a, %d %b %Y',timetuple)}

    def defaultFileListHandler(self, request):
        data = request.getData()
        config = request.getConfiguration()
        return (data['bl_type'] == 'dir' and 
                tools.Walk(data['root_datadir'], int(config['depth'])) or 
                [data['root_datadir']])

    def run(self):
        """Main loop for pyblosxom"""
        config = self._request.getConfiguration()
        data = self._request.getData()

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
        libs.plugins.__init__.initialize_plugins()

        api.fileListHandler.register(self.defaultFileListHandler, api.LAST)
        
        # CGI command handling
        tools.cgiRequest(self._request)
        filelist = tools.fileList(self._request)
        
        dataList = []
        for ourfile in filelist:
            dataList.append(self.getProperties(ourfile, data['root_datadir']))
        dataList = tools.sortDictBy(dataList,"mtime")
        
        # Match dates with files if applicable
        if not data['pi_yr'] == '':
            month = (data['pi_mo'] in tools.month2num.keys() and tools.month2num[data['pi_mo']] or data['pi_mo'])
            matchstr = "^" + data["pi_yr"] + month + data["pi_da"]
            valid_list = ([x for x in dataList
                       if re.match(matchstr, x['fulltime'])])
        else:
            valid_list = dataList

        data["entry_list"] = valid_list

        # we pass the request with the entry_list through the
        # plugins giving them a chance to transform the data.
        # plugins modify the request in-place--no need to return
        # things.
        api.prepareChain.executeHandler((self._request,))
        
        valid_list = data["entry_list"]

        if renderer and not renderer.rendered:
            if valid_list:
                renderer.setContent(valid_list)
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
