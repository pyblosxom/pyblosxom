"""
This is the main module for PyBlosxom functionality.  PyBlosxom's setup 
and default handlers are defined here.
"""
from __future__ import nested_scopes
import os, time, re, sys
import tools
from entries.fileentry import FileEntry

VERSION = "0.9.1"
VERSION_DATE = VERSION + " April 05, 2004"
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
        Initializes the PyBlosxom class

        @param request: A L{Pyblosxom.Request.Request} object
        @type request: L{Pyblosxom.Request.Request} object
        """
        self._request = request

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
        else:
            config['base_url'] = config.get('base_url', '')

        if len(config['datadir']) > 0 and config['datadir'][-1] == os.sep:
            config['datadir'] = config['datadir'][:-1]

   
    def common_start(self, start_callbacks=1, render=1):
        """
        Common pyblosxom initialization used by other CGI scripts.

        @param start_callbacks: whether (1) or not (0) we add Pyblosxom
            startup method to the startup callback.
        @type  start_callbacks: boolean

        @param render: whether (1) or not (0) we instantiate a renderer
        @type  render: boolean

        @returns: a tuple containing the config and data dicts
        @rtype: (config dict, data dict)
        """
        config = self._request.getConfiguration()
        data = self._request.getData()

        # import and initialize plugins
        import plugin_utils
        plugin_utils.initialize_plugins(config.get("plugin_dirs", []), config.get("load_plugins", None))

        # inject our own startup into the callback thing
        if start_callbacks:
            plugin_utils.callbacks.setdefault("startup", []).append(self.startup)

        if render:
            # get the renderer we want to use
            r = config.get("renderer", "blosxom")

            # import the renderer
            r = tools.importName("Pyblosxom.renderers", r)

            # get the renderer object
            r = r.Renderer(self._request, config.get("stdoutput", sys.stdout))

            # go through the renderer callback to see if anyone else
            # wants to render.  the default is the renderer object we
            # figured out from above.  this renderer gets stored in
            # the data dict for downstream processing.
            data['renderer'] = tools.run_callback('renderer', 
                                                  {'request': self._request},
                                                  donefunc = lambda x: x != None, 
                                                  defaultfunc = lambda x: r)
        
        # do start callback
        tools.run_callback("start", {'request': self._request})

        # entryparser callback is runned first here to allow other plugins
        # register what file extensions can be used
        data['extensions'] = tools.run_callback("entryparser",
                                        {'txt': blosxom_entry_parser},
                                        mappingfunc=lambda x,y:y,
                                        defaultfunc=lambda x:x)
        return (config, data)
        
    def run(self):
        """
        Main loop for pyblosxom.
        """
        config, data = self.common_start()
        
        # allow anyone else to handle the request at this point
        handled = tools.run_callback("handle", 
                        {'request': self._request},
                        mappingfunc=lambda x,y:x,
                        donefunc=lambda x:x)

        if not handled == 1:
            self.defaultHandler(config, data)

        # do end callback
        tools.run_callback("end", {'request':self._request})

    def defaultHandler(self, config, data):
        import cgi

        self._request.addHttp( {"form": cgi.FieldStorage() } )
        # process the path info to determine what kind of blog entry(ies) 
        # this is
        tools.run_callback("pathinfo",
                               {"request": self._request},
                               donefunc=lambda x:x != None,
                               defaultfunc=blosxom_process_path_info)

        # call the filelist callback to generate a list of entries
        data["entry_list"] = tools.run_callback("filelist",
                                   {"request": self._request},
                                   donefunc=lambda x:x != None,
                                   defaultfunc=blosxom_file_list_handler)
        
        # we pass the request with the entry_list through the prepare callback
        # giving everyone a chance to transform the data.  the request is
        # modified in place.
        tools.run_callback("prepare", {"request": self._request})

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
                         'request': self._request})
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
                         'request': self._request})
            renderer.render()

        elif not renderer:
            output = config.get('stdoutput', sys.stdout)
            output.write("Content-Type: text/plain\n\nThere is something wrong with your setup.\n  Check your config files and verify that your configuration is correct.\n")

    def runCallback(self, callback="help"):
        """
        Generic method to run the engine for a specific callback
        """
        # treated as a non-rendering startup
        config, data = self.common_start(render=0)

        # invoke all callbacks for the 'callback'
        handled = tools.run_callback(callback,
                        {'request': self._request},
                        mappingfunc=lambda x,y:x,
                        donefunc=lambda x:x)

def blosxom_entry_parser(filename, request):
    """
    Open up a *.txt file and read its contents

    @param filename: A filename to extra data and meta data from
    @type filename: string

    @param request: A standard request object
    @type request: L{Pyblosxom.Request.Request} object

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
    @type args: L{Pyblosxom.Request.Request}

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
    @type args: L{Pyblosxom.Request.Request}
    """
    request = args['request']
    config = request.getConfiguration()
    data = request.getData()
    pyhttp = request.getHttp()

    form = pyhttp["form"]
    data['flavour'] = (form.has_key('flav') and 
            form['flav'].value or 
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
            elif (os.path.basename(filename) == 'index' and 
                    os.path.isdir(dirname)):
                # blanket flavours?
                data['flavour'] = ext[1:]
                if data['pi_bl'] != '':
                    config['blog_title'] += ' : %s' % os.path.dirname(data['pi_bl'])
                data['root_datadir'] = dirname
                data['bl_type'] = 'dir'
                
    # Construct our final URL
    data['url'] = '%s/%s' % (config['base_url'], data['pi_bl'])

# vim: shiftwidth=4 tabstop=4 expandtab
