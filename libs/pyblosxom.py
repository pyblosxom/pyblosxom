# vim: shiftwidth=4 tabstop=4 expandtab
import os, time, string, re, cgi
import tools, api
import cPickle as pickle

class PyBlosxom:
    def __init__(self, py, xmlrpc, xmlRpcCall=0):
        self.py = py
        self.xmlrpc = xmlrpc
        self.xmlRpcCall = xmlRpcCall
        self.flavour = {}
        self.dayFlag = 1 # Used to print valid date footers
        
    def startup(self):
        self.py['pi_bl'] = ''
        path_info = []

        # If we use XML-RPC, we don't need favours and GET/POST fields
        if not self.xmlRpcCall:
            form = cgi.FieldStorage()
            self.py['flavour'] = (form.has_key('flav') and form['flav'].value or 'html')

            # Get the blog name if possible
            if os.environ.get('PATH_INFO', ''):
                path_info = os.environ['PATH_INFO'].split('/')
                if path_info[0] == '':
                    path_info.pop(0)
                while re.match(r'^[a-zA-Z]\w*', path_info[0]):
                    self.py['pi_bl'] += '/%s' % path_info.pop(0)
                    if len(path_info) == 0:
                        break

            self.py['root_datadir'] = self.py['datadir']
            if os.path.isdir(self.py['datadir'] + self.py['pi_bl']):
                if self.py['pi_bl'] != '':
                    self.py['blog_title'] += ' : %s' % self.py['pi_bl']
                self.py['root_datadir'] = self.py['datadir'] + self.py['pi_bl']
                self.py['bl_type'] = 'dir'
            elif os.path.isfile(self.py['datadir'] + self.py['pi_bl'] + '.txt'):
                self.py['blog_title'] += ' : %s' % re.sub(r'/[^/]+$','',self.py['pi_bl'])
                self.py['bl_type'] = 'file'
                self.py['root_datadir'] = self.py['datadir'] + self.py['pi_bl'] + '.txt'
            else:
                match = re.search(r'\.(\w+)$',self.py['pi_bl'])
                probableFile = self.py['datadir'] + re.sub(r'\.\w+$','',self.py['pi_bl']) + '.txt'
                if match and os.path.isfile(probableFile):
                    self.py['flavour'] = match.groups()[0]
                    self.py['root_datadir'] = probableFile
                    self.py['blog_title'] += ' : %s' % re.sub(r'/[^/]+\.\w+$','',self.py['pi_bl'])
                    self.py['bl_type'] = 'file'
                else:
                    self.py['pi_bl'] = ''
                    self.py['bl_type'] = 'dir'

        # Get our URL
        if os.environ.has_key('SCRIPT_NAME'):
            self.py['url'] = 'http://%s%s%s' % (os.environ['HTTP_HOST'], os.environ['SCRIPT_NAME'], self.py['pi_bl'])
            self.py['base_url'] = 'http://%s%s' % (os.environ['HTTP_HOST'], os.environ['SCRIPT_NAME'])

        # Python is unforgiving as perl in this case
        self.py['pi_yr'] = (len(path_info) > 0 and path_info.pop(0) or '')
        self.py['pi_mo'] = (len(path_info) > 0 and path_info.pop(0) or '')
        self.py['pi_da'] = (len(path_info) > 0 and path_info.pop(0) or '')


    def getProperties(self, filename, root):
        """Returns a dictionary of file related contents"""
        mtime = tools.filestat(filename)[8]
        timetuple = time.localtime(mtime)
        path = string.replace(filename, root, '')
        path = string.replace(path, os.path.basename(filename), '')
        path = path[1:][:-1]
        absolute_path = string.replace(filename, self.py['datadir'], '')
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
        if os.path.isfile('%s/%s.stor' % (self.py.get('tb_data', ''), tb_id)):
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

    def defaultFileListHandler(self, py):
        return (py['bl_type'] == 'dir' and 
                tools.Walk(py['root_datadir'], 
                    int(py['depth'])) or 
                [py['root_datadir']])

    def run(self):
        """Main loop for pyblosxom"""
        renderer = tools.importName('libs.renderers', 
                self.py.get('renderer', 'blosxom')).Renderer(self.py)
        # import entryparsers here to allow other plugins register what file
        # extensions can be used
        import libs.entryparsers.__init__
        libs.entryparsers.__init__.initialize_extensions()
        self.py['extensions'] = libs.entryparsers.__init__.ext
        
        # import plugins and allow them to register with the api
        import libs.plugins.__init__
        libs.plugins.__init__.initialize_plugins()

        api.fileListHandler.register(self.defaultFileListHandler, api.LAST)
        
        # CGI command handling
        tools.cgiRequest(self.py)
        filelist = tools.fileList(self.py)
        
        dataList = []
        for ourfile in filelist:
            dataList.append(self.getProperties(ourfile, self.py['root_datadir']))
        dataList = tools.sortDictBy(dataList,"mtime")
        
        # Match dates with files if applicable
        if not self.py['pi_yr'] == '':
            month = (self.py['pi_mo'] in tools.month2num.keys() and tools.month2num[self.py['pi_mo']] or self.py['pi_mo'])
            valid_list = ([x for x in dataList
                       if re.match('^' + self.py['pi_yr'] + month + self.py['pi_da'], x['fulltime'])])
        else:
            valid_list = dataList

        # load the plugins that have load methods
        libs.plugins.__init__.load_plugins(self.py, valid_list, renderer)
        
        if renderer and not renderer.rendered:
            if valid_list:
                renderer.setContent(valid_list)
                tools.logRequest(self.py.get('logfile',''), '200')
            else:
                renderer.addHeader(['Status: 404 Not Found'])
                renderer.setContent(
                    {'title': 'The page you are looking for is not available',
                     'body': 'Somehow I cannot find the page you want. ' + 
                     'Go Back to <a href="%(base_url)s">%(blog_title)s</a>?' 
                     % self.py})
                tools.logRequest(self.py.get('logfile',''), '404')
            renderer.render()

        elif not renderer:
            print "Content-Type: text/plain\n\nThere is something wrong with your setup"
