from __future__ import nested_scopes, generators
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
This is the main module for PyBlosxom functionality.  PyBlosxom's setup 
and default handlers are defined here.
"""

__revision__ = "$Revision$"

import os
import time
import re
import locale
import sys
import os.path
import cgi
try: 
    from cStringIO import StringIO
except ImportError: 
    from StringIO import StringIO

from Pyblosxom import tools, plugin_utils
from Pyblosxom.entries.fileentry import FileEntry

VERSION = "2.0"
VERSION_DATE = VERSION + " dev"
VERSION_SPLIT = tuple(VERSION.split('.'))


class PyBlosxom:
    """
    This is the main class for PyBlosxom functionality.  It handles
    initialization, defines default behavior, and also pushes the
    request through all the steps until the output is rendered and
    we're complete.
    """
    def __init__(self, config, environ, data=None):
        """
        Sets configuration and environment.
        Creates the L{Request} object.

        @param config: A dict containing the configuration variables.
        @type config: dict

        @param environ: A dict containing the environment variables.
        @type environ: dict

        @param data: A dict containing data variables.
        @type data: dict
        """
        config['pyblosxom_name'] = "pyblosxom"
        config['pyblosxom_version'] = VERSION_DATE

        # wbg 10/6/2005 - the plugin changes won't happen until
        # PyBlosxom 1.4.  so i'm commenting this out until then.
        # add the included plugins directory
        # p = config.get("plugin_dirs", [])
        # f = __file__[:__file__.rfind(os.sep)] + os.sep + "plugins"
        # p.append(f)
        # config['plugin_dirs'] = p

        self._configuration = config
        self._request = Request(config, environ, data)

    def initialize(self):
        """
        The initialize step further initializes the Request by setting
        additional information in the _data dict, registering plugins,
        and entryparsers.
        """
        data = self._request.data
        pyhttp = self._request.http
        config = self._request.configuration

        # Initialize the locale, if wanted (will silently fail if locale 
        # is not available)
        if config.get('locale'):
            try: 
                locale.setlocale(locale.LC_ALL, config['locale'])
            except locale.Error: 
                # Invalid locale 
                pass 

        # initialize the tools module
        tools.initialize(config)

        data["pyblosxom_version"] = VERSION_DATE
        data['pi_bl'] = ''

        # Get our URL and configure the base_url param
        if 'SCRIPT_NAME' in pyhttp:
            if not 'base_url' in config:
                # allow http and https
                config['base_url'] = '%s://%s%s' % \
                                     (pyhttp['wsgi.url_scheme'], 
                                      pyhttp['HTTP_HOST'], 
                                      pyhttp['SCRIPT_NAME'])
        else:
            config['base_url'] = config.get('base_url', '')

        # take off the trailing slash for base_url
        if config['base_url'].endswith("/"):
            config['base_url'] = config['base_url'][:-1]

        datadir = config["datadir"]
        if datadir.endswith("/") or datadir.endswith("\\"):
            datadir = datadir[:-1]
            config['datadir'] = datadir

        # import and initialize plugins
        plugin_utils.initialize_plugins(config.get("plugin_dirs", []), 
                                        config.get("load_plugins", None))

        # entryparser callback is run here first to allow other plugins
        # register what file extensions can be used
        data['extensions'] = tools.run_callback("entryparser",
                                        {'txt': blosxom_entry_parser},
                                        mappingfunc=lambda x,y:y,
                                        defaultfunc=lambda x:x)

    def cleanup(self):
        """
        This cleans up PyBlosxom after a run.  Mostly it calls
        tools.cleanup which in turn shuts down the logging.

        This should be called when Pyblosxom has done all its work
        right before exiting.
        """
        # log some useful stuff for debugging
        # this will only be logged if the log_level is "debug"
        log = tools.getLogger()
        response = self.getResponse()
        log.debug("status = %s" % response.status)
        log.debug("headers = %s" % response.headers)

        tools.cleanup()

    def getRequest(self):
        """
        Returns the L{Request} object for this PyBlosxom instance.
        
        @returns: the request object 
        @rtype: L{Request}
        """
        return self._request

    def getResponse(self):
        """
        Returns the L{Response} object which handles all output 
        related functionality for this PyBlosxom instance.
        
        @see: L{Response}

        @returns: the reponse object 
        @rtype: L{Response}
        """
        return self._request.getResponse()

    def run(self, static=False):
        """
        This is the main loop for PyBlosxom.  This method will run the 
        handle callback to allow registered handlers to handle the request.  
        If nothing handles the request, then we use the
        default_blosxom_handler.

        @param static: True if we should execute in "static rendering mode"
            and False otherwise
        @type  static: boolean
        """
        self.initialize()

        # buffer the input stream in a StringIO instance if dynamic rendering 
        # is used.  This is done to have a known/consistent way of accessing 
        # incomming data.
        if static == False:
            self.getRequest().buffer_input_stream()

        # run the start callback
        tools.run_callback("start", {'request': self._request})

        # allow anyone else to handle the request at this point
        handled = tools.run_callback("handle", 
                        {'request': self._request},
                        mappingfunc=lambda x,y:x,
                        donefunc=lambda x:x)

        if not handled == 1:
            blosxom_handler(self._request)

        # do end callback
        tools.run_callback("end", {'request': self._request})

        # we're done, clean up.
        # only call this if we're not in static rendering mode.
        if static == False:
            self.cleanup()

    def runCallback(self, callback="help"):
        """
        This method executes the start callback (initializing plugins),
        executes the requested callback, and then executes the end
        callback.  This is useful for scripts outside of PyBlosxom that
        need to do things inside of the PyBlosxom framework.

        @param callback: the callback to execute
        @type  callback: string

        @returns: the result of calling the callback
        @rtype: varies
        """
        self.initialize()

        # run the start callback
        tools.run_callback("start", {'request': self._request})

        # invoke all callbacks for the 'callback'
        handled = tools.run_callback(callback,
                        {'request': self._request},
                        mappingfunc=lambda x,y:x,
                        donefunc=lambda x:x)

        # do end callback
        tools.run_callback("end", {'request': self._request})

        return handled

    def runRenderOne(self, url, headers):
        """
        Renders a single page from the blog.

        @param url: the url to render--this has to be relative to
        PyBlosxom
        @type url: string

        @param headers: 1 if you want the headers rendered and 0 if not.
        @type headers: int
        """ 
        self.initialize()

        config = self._request.configuration
        data = self._request.data

        if url.find("?") != -1:
            url = url[:url.find("?")]
            query = url[url.find("?")+1:]
        else:
            query = ""

        url = url.replace(os.sep, "/")
        response = tools.render_url(config, url, query)
        response.sendHeaders(sys.stdout)
        response.sendBody(sys.stdout)

        print response.read()

        # we're done, clean up
        self.cleanup()
 
    def runStaticRenderer(self, incremental=0):
        """
        This will go through all possible things in the blog and statically 
        render everything to the "static_dir" specified in the config file.

        This figures out all the possible path_info settings and calls 
        self.run() a bazillion times saving each file.

        @param incremental: whether (1) or not (0) to incrementally
            render the pages.  if we're incrementally rendering pages,
            then we render only the ones that have changed.
        @type  incremental: boolean
        """
        self.initialize()

        config = self._request.config
        data = self._request.data
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
            # FIXME - if not ext in data["extensions"].keys():
            if not ext in data["extensions"]:
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

            # if the entry is more recent than the static, we want to
            # re-render
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

        # if they have stuff in their root category, it'll add a "/"
        # to the category list and we want to remove that because it's
        # a duplicate of "".
        if "/" in categories:
            categories.remove("/")

        print "rendering %d category indexes." % len(categories)

        for mem in categories:
            mem = os.path.normpath( mem + "/index." )
            for f in flavours:
                renderme.append( (mem + f, "") )

        # now we handle dates
        dates = dates.keys()
        dates.sort()

        dates = ["/" + d for d in dates]

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
        tools.run_callback("staticrender_filelist",
                           {'request': self._request, 
                            'filelist': renderme,
                            'flavours': flavours})

        print "building %s files." % len(renderme)

        for url, q in renderme:
            url = url.replace(os.sep, "/")
            print "rendering '%s' ..." % url

            tools.render_url_statically(config, url, q)

        # we're done, clean up
        self.cleanup()

    def testInstallation(self):
        """
        Goes through and runs some basic tests of the installation
        to make sure things are working.

        FIXME - This could probably use some work.  Maybe make this like
        MoinMoin's SystemInfo page?
        """
        tools.initialize(self._configuration)
        test_installation(self._request)
        tools.cleanup()


class PyBlosxomWSGIApp:
    """
    This class is the WSGI application for PyBlosxom.
    """
    def __init__(self, configini=None):
        """
        Make WSGI app for PyBlosxom

        @param configini: dict encapsulating information from a config.ini
            file or any other property file that will override the config.py
            file.
        @type  configini: dict
        """
        if configini == None:
            configini = {}

        _config = {}
        for key, value in configini.items():
            if isinstance(value, basestring) and value.isdigit():
                _config[key] = int(value)
            else:
                _config[key] = value

        import config
        self.config = dict(config.py)

        self.config.update(_config)
        if "codebase" in _config:
            sys.path.insert(0, _config["codebase"])

    def __call__(self, env, start_response):
        """
        Runs the WSGI app.
        """
        # ensure that PATH_INFO exists. a few plugins break if this is 
        # missing.
        if "PATH_INFO" not in env:
            env["PATH_INFO"] = ""

        p = PyBlosxom(self.config, env)
        p.run()

        pyresponse = p.getResponse()
        start_response(pyresponse.status, list(pyresponse.headers.items()))
        pyresponse.seek(0)
        return [pyresponse.read()]

def pyblosxom_app_factory(global_config, **local_config):
    """
    App factory for paste.
    """
    from paste import cgitb_catcher

    conf = global_config.copy()
    conf.update(local_config)
    conf.update(dict(local_config=local_config, global_config=global_config))

    if "configpydir" in conf:
        sys.path.insert(0, conf["configpydir"])

    return cgitb_catcher.make_cgitb_middleware(PyBlosxomWSGIApp(conf),
                                               global_config)


class EnvironmentDict(dict):
    """
    Extends dict with the environ and adds a "form" item that is a
    cgi.FieldStorage created on-demand.
    """
    def __init__(self, request, environ):
        dict.__init__(self)
        self._request = request
        self.update(environ)

    def __getitem__(self, k):
        """
        If the key argument is "form", we return the _request.getForm().
        Otherwise this returns the item for that key in the wrapped
        dict.
        """
        if k == "form":
            return self._request.getForm()

        return dict.__getitem__(self, k)

class Request(object):
    """
    This class holds the PyBlosxom request.  It holds configuration
    information, HTTP/CGI information, and data that we calculate
    and transform over the course of execution.

    There should be only one instance of this class floating around
    and it should get created by pyblosxom.cgi and passed into the
    PyBlosxom instance which will do further manipulation on the
    Request instance.
    """
    def __init__(self, config, environ, data):
        """
        Sets configuration and environment.
        Creates the L{Response} object which handles all output 
        related functionality.
        
        @param config: A dict containing the configuration variables.
        @type config: dict

        @param environ: A dict containing the environment variables.
        @type environ: dict

        @param data: A dict containing data variables.
        @type data: dict
        """
        # this holds configuration data that the user changes 
        # in config.py
        self._config = config

        # this holds HTTP/CGI oriented data specific to the request
        # and the environment in which the request was created
        self._http = EnvironmentDict(self, environ)

        # this holds run-time data which gets created and transformed
        # by pyblosxom during execution
        if data == None:
            data = dict()
        self._data = data

        # this holds the input stream.
        # initialized for dynamic rendering in Pyblosxom.run.
        # for static rendering there is no input stream.
        self._in = StringIO()

        # copy methods to the Request object.
        self.read = self._in.read
        self.readline = self._in.readline
        self.readlines = self._in.readlines
        self.seek = self._in.seek
        self.tell = self._in.tell

        # this holds the FieldStorage instance.
        # initialized when request.getForm is called the first time
        self._form = None

        self._response = None
        
        # create and set the Response
        self.setResponse(Response(self))

    def __iter__(self):
        """
        Can't copy the __iter__ method over from the StringIO instance cause
        iter looks for the method in the class instead of the instance.

        See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252151
        """
        return self._in

    def buffer_input_stream(self):
        """
        Buffer the input stream in a StringIO instance.
        This is done to have a known/consistent way of accessing incoming 
        data.  For example the input stream passed by mod_python does not 
        offer the same functionallity as sys.stdin.
        """
        # TODO: tests on memory consumption when uploading huge files
        pyhttp = self.http
        winput = pyhttp['wsgi.input']
        method = pyhttp["REQUEST_METHOD"]

        # there's no data on stdin for a GET request.  pyblosxom
        # will block indefinitely on the read for a GET request with
        # thttpd.
        if method != "GET":
            try:
                length = int(pyhttp.get("CONTENT_LENGTH", 0))
            except ValueError:
                length = 0

            if length > 0:
                self._in.write(winput.read(length))
                # rewind to start
                self._in.seek(0)

    def setResponse(self, response):
        """
        Sets the L{Response} object.

        @param response: A pyblosxom Response object
        @type response: L{Response}
        """
        self._response = response
        # for backwards compatibility
        self.config['stdoutput'] = response

    def getResponse(self):
        """
        Returns the L{Response} object which handles all output 
        related functionality.
        
        @returns: L{Response}
        @rtype: object
        """
        return self._response

    def getForm(self):
        """
        Returns the form data submitted by the client.
        The L{form<cgi.FieldStorage>} instance is created
        only when requested to prevent overhead and unnecessary
        consumption of the input stream.

        @returns: L{cgi.FieldStorage}
        @rtype: object
        """
        if self._form == None:
            # parse the form on-demand
            form = cgi.FieldStorage(fp=self._in,
                                    environ=dict(self._http), 
                                    keep_blank_values=0)
            # rewind the input buffer
            self._in.seek(0)
            self._form = form

        return self._form

    def getConfiguration(self):
        """
        Returns the configuration dict generated by config.py.
        """
        return self._config
    
    def getHttp(self):
        """
        Returns the http dict generated by environ and wsgi variables.
        """
        return self._http

    def getData(self):
        """
        Returns the data dict generated during the course of handling
        a PyBlosxom request.
        """
        return self._data

    configuration = property(getConfiguration)
    config = configuration
    conf = configuration
    http = property(getHttp)
    data = property(getData)

    def addHttp(self, d):
        """
        Takes in a dict and adds/overrides values in the existing
        http dict with the new values.

        @param d: the dict with the new keys/values to add
        @type  d: dict
        """
        self._http.update(d)

    def addData(self, d):
        """
        Takes in a dict and adds/overrides values in the existing
        data dict with the new values.

        @param d: the dict with the new keys/values to add
        @type  d: dict
        """
        self._data.update(d)

    def addConfiguration(self, newdict):
        """
        Takes in a dict and adds/overrides values in the existing
        configuration dict with the new values.

        @param newdict: the dict with the new keys/values to add
        @type  newdict: dict
        """
        self._configuration.update(newdict)


class Response(object):
    """
    Response class to handle all output related tasks in one place.

    This class is basically a wrapper arround a StringIO instance.
    It also provides methods for managing http headers.
    """
    def __init__(self, request):
        """
        Sets the L{Request} object that leaded to this response.
        Creates a L{StringIO} that is used as a output buffer.
        
        @param request: request object.
        @type request: L{Request}
        """
        self._request = request
        self._out = StringIO()
        self._headers_sent = False
        self.headers = {}
        self.status = "200 OK"

        self.close = self._out.close
        self.flush = self._out.flush
        self.read = self._out.read
        self.readline = self._out.readline
        self.readlines = self._out.readlines
        self.seek = self._out.seek
        self.tell = self._out.tell
        self.write = self._out.write
        self.writelines = self._out.writelines
    
    def __iter__(self):
        """
        Can't copy the __iter__ method over from the StringIO instance cause
        iter looks for the method in the class instead of the instance.

        See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252151
        """
        return self._out

    def setStatus(self, status):
        """
        Sets the status code for this response.
        
        @param status: A status code and message like '200 OK'.
        @type status: str
        """
        self.status = status

    def getStatus(self):
        """
        Returns the status code and message of this response.
        
        @returns: str
        """
        return self.status

    def addHeader(self, *args):
        """
        Populates the HTTP header with lines of text.
        Sets the status code on this response object if the given argument
        list containes a 'Status' header.

        @param args: Paired list of headers
        @type args: argument lists
        @raises ValueError: This happens when the parameters are not correct
        """
        args = list(args)

        if len(args) % 2 == 1:
            raise ValueError, "Headers recieved are not in the correct form"
            
        while args:
            key = args.pop(0).strip()
            if key.find(' ') != -1 or key.find(':') != -1:
                raise ValueError, "There should be no spaces in header keys"

            value = args.pop(0).strip()
            
            if key.lower() == "status":
                self.setStatus(str(value))
            else:
                self.headers.update({key: str(value)})

    def getHeaders(self):
        """
        Returns the headers of this response.
        
        @returns: the HTTP response headers
        @rtype: dict
        """
        return self.headers

    def sendHeaders(self, out):
        """
        Send HTTP Headers to the given output stream.

        @param out: File like object
        @type out: file
        """
        out.write("Status: %s\n" % self.status)
        # FIXME - out.write('\n'.join(['%s: %s' % (hkey, self.headers[hkey]) 
        #                     for hkey in self.headers.keys()]))
        out.write('\n'.join(['%s: %s' % (hkey, self.headers[hkey]) 
                             for hkey in self.headers]))
        out.write('\n\n')
        self._headers_sent = True

    def sendBody(self, out):
        """
        Send the response body to the given output stream.

        @param out: File like object
        @type out: file
        """
        self.seek(0)
        try:
            out.write(self.read())
        except IOError:
            # this is usually a Broken Pipe because the client dropped the
            # connection.  so we skip it.
            pass


#
# blosxom behavior stuff
# 

def blosxom_handler(request):
    """
    This is the default blosxom handler.

    It calls the renderer callback to get a renderer.  If there is 
    no renderer, it uses the blosxom renderer.

    It calls the pathinfo callback to process the path_info http
    variable.

    It calls the filelist callback to build a list of entries to
    display.

    It calls the prepare callback to do any additional preparation
    before rendering the entries.

    Then it tells the renderer to render the entries.

    @param request: A standard request object
    @type request: L{Pyblosxom.pyblosxom.Request} object
    """
    config = request.config
    data = request.data

    # go through the renderer callback to see if anyone else
    # wants to render.  this renderer gets stored in the data dict 
    # for downstream processing.
    rend = tools.run_callback('renderer', 
                              {'request': request},
                              donefunc = lambda x: x != None, 
                              defaultfunc = lambda x: None)

    if not rend:
        # get the renderer we want to use
        rend = config.get("renderer", "blosxom")

        # import the renderer
        rend = tools.importname("Pyblosxom.renderers", rend)

        # get the renderer object
        rend = rend.Renderer(request, config.get("stdoutput", sys.stdout))

    data['renderer'] = rend

    # generate the timezone variable
    data["timezone"] = time.tzname[time.localtime()[8]]

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

    # figure out the blog-level mtime which is the mtime of the head of
    # the entry_list
    entry_list = data["entry_list"]
    if isinstance(entry_list, list) and len(entry_list) > 0:
        mtime = entry_list[0].get("mtime", time.time())
    else:
        mtime = time.time()
    mtime_tuple = time.localtime(mtime)
    mtime_gmtuple = time.gmtime(mtime)

    data["latest_date"] = time.strftime('%a, %d %b %Y', mtime_tuple)

    # Make sure we get proper 'English' dates when using standards 
    loc = locale.getlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, 'C')

    data["latest_w3cdate"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', 
                                           mtime_gmtuple)
    data['latest_rfc822date'] = time.strftime('%a, %d %b %Y %H:%M GMT', 
                                              mtime_gmtuple)

    # set the locale back
    locale.setlocale(locale.LC_ALL, loc)

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
        output.write("Content-Type: text/plain\n\n" + \
                     "There is something wrong with your setup.\n" + \
                     "Check your config files and verify that your " + \
                     "configuration is correct.\n")


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
    config = request.config

    entryData = {}

    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    # the file has nothing in it...  so we're going to return
    # a blank entry data object.
    if len(lines) == 0:
        return { "title": "", "body": "" }

    # NOTE: you can probably use the next bunch of lines verbatim
    # for all entryparser plugins.  this pulls the first line off as
    # the title, the next bunch of lines that start with # as 
    # metadata lines, and then everything after that is the body
    # of the entry.
    title = lines.pop(0).strip()
    entryData['title'] = title

    # absorb meta data lines which begin with a #
    while lines and lines[0].startswith("#"):
        meta = lines.pop(0)
        meta = meta[1:].strip()     # remove the hash
        meta = meta.split(" ", 1)
        entryData[meta[0].strip()] = meta[1].strip()

    # Call the preformat function
    args = {'parser': entryData.get('parser', config.get('parser', 'plain')),
            'story': lines,
            'request': request}
    otmp = tools.run_callback('preformat', 
                              args,
                              donefunc = lambda x:x != None,
                              defaultfunc = lambda x: ''.join(x['story']))
    entryData['body'] = otmp

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
    @type args: object

    @returns: the content we want to render
    @rtype: list of EntryBase objects
    """
    request = args["request"]

    data = request.data
    config = request.config

    if data['bl_type'] == 'dir':
        filelist = tools.Walk(request, 
                              data['root_datadir'], 
                              int(config.get("depth", "0")))
    elif data['bl_type'] == 'file':
        filelist = [data['root_datadir']]
    else:
        filelist = []

    entrylist = []
    for ourfile in filelist:
        e = FileEntry(request, ourfile, data['root_datadir'])
        entrylist.append((e._mtime, e))

    # this sorts entries by mtime in reverse order.  entries that have
    # no mtime get sorted to the top.
    entrylist.sort()
    entrylist.reverse()
    
    # Match dates with files if applicable
    if data['pi_yr']:
        # This is called when a date has been requested, e.g. 
        # /some/category/2004/Sep
        # FIXME - month = (data['pi_mo'] in tools.month2num.keys() and \
        month = (data['pi_mo'] in tools.month2num and \
                      tools.month2num[data['pi_mo']] or \
                      data['pi_mo'])
        matchstr = "^" + data["pi_yr"] + month + data["pi_da"]
        valid_list = [x for x in entrylist if re.match(matchstr, 
                                                       x[1]._fulltime)]
    else:
        valid_list = entrylist

    # This is the maximum number of entries we can show on the front page
    # (zero indicates show all entries)
    maxe = config.get("num_entries", 5)
    if maxe and not data["pi_yr"]:
        valid_list = valid_list[:maxe]
        data["debugme"] = "done"

    valid_list = [x[1] for x in valid_list]

    return valid_list

def blosxom_process_path_info(args):
    """ 
    Process HTTP PATH_INFO for URI according to path specifications, fill in
    data dict accordingly.
    
    The paths specification looks like this:
        - C{/foo.html} and C{/cat/foo.html} - file foo.* in / and /cat
        - C{/cat} - category
        - C{/2002} - category
        - C{/2002} - year
        - C{/2002/Feb} (or 02) - Year and Month
        - C{/cat/2002/Feb/31} - year and month day in category.

    @param args: dict containing the incoming Request object
    @type args: object
    """
    request = args['request']
    config = request.config
    data = request.data
    pyhttp = request.http

    form = request.getForm()

    # figure out which flavour to use.  the flavour is determined
    # by looking at the "flav" post-data variable, the "flav"
    # query string variable, the "default_flavour" setting in the
    # config.py file, or "html"
    flav = config.get("default_flavour", "html")
    if 'flav' in form:
        flav = form["flav"].value

    data["flavour"] = flav

    data['pi_yr'] = ''
    data['pi_mo'] = ''
    data['pi_da'] = ''
    
    path_info = pyhttp.get("PATH_INFO", "")

    data['root_datadir'] = config['datadir']

    data["pi_bl"] = path_info

    # first we check to see if this is a request for an index and we can pluck
    # the extension (which is certainly a flavour) right off.
    newpath, ext = os.path.splitext(path_info)
    if newpath.endswith("/index") and ext:
        # there is a flavour-like thing, so that's our new flavour
        # and we adjust the path_info to the new filename
        data["flavour"] = ext[1:]
        path_info = newpath

    while path_info and path_info.startswith("/"):
        path_info = path_info[1:]

    absolute_path = os.path.join(config["datadir"], path_info)

    path_info = path_info.split("/")

    if os.path.isdir(absolute_path):

        # this is an absolute path

        data['root_datadir'] = absolute_path
        data['bl_type'] = 'dir'

    elif absolute_path.endswith("/index") and \
            os.path.isdir(absolute_path[:-6]):

        # this is an absolute path with /index at the end of it

        data['root_datadir'] = absolute_path[:-6]
        data['bl_type'] = 'dir'

    else:
        # this is either a file or a date

        ext = tools.what_ext(data["extensions"].keys(), absolute_path)
        if not ext:
            # it's possible we didn't find the file because it's got a flavour
            # thing at the end--so try removing it and checking again.
            newpath, flav = os.path.splitext(absolute_path)
            if flav:
                ext = tools.what_ext(data["extensions"].keys(), newpath)
                if ext:
                    # there is a flavour-like thing, so that's our new flavour
                    # and we adjust the absolute_path and path_info to the new 
                    # filename
                    data["flavour"] = flav[1:]
                    absolute_path = newpath
                    path_info, flav = os.path.splitext("/".join(path_info))
                    path_info = path_info.split("/")

        if ext:
            # this is a file
            data["bl_type"] = "file"
            data["root_datadir"] = absolute_path + "." + ext

        else:
            data["bl_type"] = "dir"

            # it's possible to have category/category/year/month/day
            # (or something like that) so we pluck off the categories
            # here.
            pi_bl = ""
            while len(path_info) > 0 and \
                    not (len(path_info[0]) == 4 and path_info[0].isdigit()):
                pi_bl = os.path.join(pi_bl, path_info.pop(0))

            # handle the case where we do in fact have a category
            # preceeding the date.
            if pi_bl:
                pi_bl = pi_bl.replace("\\", "/")
                data["pi_bl"] = pi_bl
                data["root_datadir"] = os.path.join(config["datadir"], pi_bl)

            if len(path_info) > 0:
                item = path_info.pop(0)
                # handle a year token
                if len(item) == 4 and item.isdigit():
                    data['pi_yr'] = item
                    item = ""

                    if (len(path_info) > 0):
                        item = path_info.pop(0)
                        # handle a month token
                        if item in tools.MONTHS:
                            data['pi_mo'] = item
                            item = ""

                            if (len(path_info) > 0):
                                item = path_info.pop(0)
                                # handle a day token
                                if len(item) == 2 and item.isdigit():
                                    data["pi_da"] = item
                                    item = ""

                                    if len(path_info) > 0:
                                        item = path_info.pop(0)

                # if the last item we picked up was "index", then we
                # just ditch it because we don't need it.
                if item == "index":
                    item = ""

                # if we picked off an item we don't recognize and/or
                # there is still stuff in path_info to pluck out, then
                # it's likely this wasn't a date.
                if item or len(path_info) > 0:
                    data["bl_type"] = "dir"
                    data["root_datadir"] = absolute_path


    # figure out the blog_title_with_path data variable
    blog_title = config["blog_title"]

    if data['pi_bl'] != '':
        data['blog_title_with_path'] = '%s : %s' % (blog_title, data['pi_bl'])
    else:
        data['blog_title_with_path'] = blog_title

    # construct our final URL
    data['url'] = '%s%s' % (config['base_url'], data['pi_bl'])
    url = config['base_url']
    if data['pi_bl'].startswith("/"):
        url = url + data['pi_bl']
    else:
        url = url + "/" + data['pi_bl']
    data['url'] = url

    # set path_info to our latest path_info
    data['path_info'] = path_info


def run_pyblosxom():
    from config import py as cfg
    env = {}

    # if there's no REQUEST_METHOD, then this is being run on the
    # command line and we should execute the command_line_handler.
    if not "REQUEST_METHOD" in os.environ:
        from Pyblosxom.pyblosxom import command_line_handler

        args = sys.argv[1:]

        if len(args) == 0:
            args = ["--test"]

        sys.exit(command_line_handler("pyblosxom.cgi", args))

    # names taken from wsgi instead of inventing something new
    env['wsgi.input'] = sys.stdin
    env['wsgi.errors'] = sys.stderr

    # figure out what the protocol is for the wsgi.url_scheme property.
    # we look at the base_url first and if there's nothing set there,
    # we look at environ.
    # FIXME - if 'base_url' in cfg.keys():
    if 'base_url' in cfg:
        env['wsgi.url_scheme'] = cfg['base_url'][:cfg['base_url'].find("://")]

    else:
        if os.environ.get("HTTPS", "off") in ("on", "1"):
            env["wsgi.url_scheme"] = "https"

        else:
            env['wsgi.url_scheme'] = "http"

    try:
        # try running as a WSGI-CGI
        from wsgiref.handlers import CGIHandler
        from Pyblosxom.pyblosxom import PyBlosxomWSGIApp
        CGIHandler().run(PyBlosxomWSGIApp())

    except ImportError:
        # run as a regular CGI

        if os.environ.get("HTTPS") in ("yes", "on", "1"):
            env['wsgi.url_scheme'] = "https"

        for mem in ["HTTP_HOST", "HTTP_USER_AGENT", "HTTP_REFERER",
                    "PATH_INFO", "QUERY_STRING", "REMOTE_ADDR",
                    "REQUEST_METHOD", "REQUEST_URI", "SCRIPT_NAME",
                    "HTTP_IF_NONE_MATCH", "HTTP_IF_MODIFIED_SINCE",
                    "HTTP_COOKIE", "CONTENT_LENGTH", "CONTENT_TYPE",
                    "HTTP_ACCEPT", "HTTP_ACCEPT_ENCODING"]:
            env[mem] = os.environ.get(mem, "")

        p = PyBlosxom(cfg, env)

        p.run()
        response = p.getResponse()
        response.sendHeaders(sys.stdout)
        response.sendBody(sys.stdout)



#
# command line stuff
#

HELP = """Syntax: %(script)s [path-opts] [args]

PATH OPTIONS:

  -c, --config

     This specifies the location of the config.py file for the blog 
     you want to work with.  If the config.py file is in the current 
     directory, then you don't need to specify this.

     Note: %(script)s will use the "codebase" parameter in your config.py
     file to locate the version of PyBlosxom you're using if there
     is one.  If there isn't one, then %(script)s expects PyBlosxom to
     be installed as a Python package on your system.

ARGUMENTS:

  -v, --version

     Prints the PyBlosxom version and some other information.

  -h, --help

     Prints this help text

  -C, --create <dir>

     Creates a PyBlosxom "installation" by building the directory hierarchy
     and copying necessary files into it.  This is an easy way to create
     a new blog.

  -h, --headers

     When rendering a url, this will also render the HTTP headers.

  -r, --render <url>

     Renders a url of your blog.

        %(script)s -r http://www.joesblog.com/cgi-bin/pyblosxom.cgi/index.html

     will pull off the base_url from the front leaving "/index.html" and
     will render "/index.html" to stdout.

        %(script)s -c ~/cgi-bin/config.py -r /index.html

     will use the config.py file located in ~/cgi-bin/ and render
     "/index.html" from the PyBlosxom root.

  -s, --static [incremental]

     Statically renders your blog.  Use "incremental" to do an incremental 
     rendering.

  -t, --test

     Tests your installation.
     

EXAMPLES:


Additional flags and options may be available through plugins that
you have installed.  Refer to plugin documentation (usually found
at the top of the plugin file) for more information.
"""
     

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

    @param request: the Request object
    @type request: object
    """
    config = request.config

    # BASE STUFF
    print "Welcome to PyBlosxom's installation verification system."
    print "------"
    print "]] printing diagnostics [["
    print "pyblosxom:   %s" % VERSION_DATE
    print "sys.version: %s" % sys.version.replace("\n", " ")
    print "os.name:     %s" % os.name
    print "codebase:    %s" % config.get("codebase", "--default--")
    print "------"

    # CONFIG FILE
    print "]] checking config file [["
    print "config has %s properties set." % len(config)
    print ""

    # these are required by the blog
    required_config = ["datadir"]

    # these are nice to have optional properties
    nice_to_have_config = ["blog_title", "blog_author", "blog_description",
                           "blog_language", "blog_encoding", "blog_icbm",
                           "base_url", "depth", "num_entries", "renderer", 
                           "plugin_dirs", "load_plugins", "blog_email", 
                           "blog_rights", "default_flavour", "flavourdir", 
                           "log_file", "log_level", "logdir", ]

    config_keys = config.keys()

    # remove keys that are auto-generated
    config_keys.remove("pyblosxom_version")
    config_keys.remove("pyblosxom_name")

    missing_required_props = []
    missing_optionsal_props = []

    missing_required_props = [m
                              for m in required_config
                              if m not in config_keys]

    missing_optional_props = [m
                              for m in nice_to_have_config
                              if m not in config_keys]

    all_keys = nice_to_have_config + required_config
    
    config_keys = [m
                   for m in config_keys
                   if m not in all_keys]

    def wrappify(ks):
        ks.sort()
        if len(ks) == 1:
            return "   %s" % ks[0]
        elif len(ks) == 2:
            return "   %s and %s" % (ks[0], ks[1])

        ks = ", ".join(ks[:-1]) + " and " + ks[-1]
        import textwrap
        return "   " + "\n   ".join( textwrap.wrap(ks, 72) )
    
    if missing_required_props:
        print ""
        print "Missing properties must be set in order for your blog to"
        print "work."
        print ""
        print wrappify(missing_required_props)
        print ""
        print "This must be done before we can go further.  Exiting."
        return

    if missing_optional_props:
        print ""
        print "You're missing optional properties.  These are not required, "
        print "but some of them may interest you.  Refer to the documentation "
        print "for more information."
        print ""
        print wrappify(missing_optional_props)

    if config_keys:
        print ""
        print "These are properties PyBlosxom doesn't know about.  They "
        print "could be used by plugins or could be ones you've added."
        print "Remove them if you know they're not used."
        print ""
        print wrappify(config_keys)
        print ""
        
    print "PASS: config file is fine."

    print "------"
    print "]] checking datadir [["

    # DATADIR
    if not os.path.isdir(config["datadir"]):
        print "datadir '%s' does not exist." % config["datadir"]          
        print "You need to create your datadir and give it appropriate"
        print "permissions."
        print ""
        print "This must be done before we can go further.  Exiting."
        return

    print "PASS: datadir is there."
    print "      Note: this does NOT check whether your webserver has "
    print "      permissions to view files therein!"

    print "------"
    print "Now we're going to verify your plugin configuration."

    if "plugin_dirs" in config:
        plugin_utils.initialize_plugins(config["plugin_dirs"],
                                        config.get("load_plugins", None))

        no_verification_support = []

        for mem in plugin_utils.plugins:
            if hasattr(mem, "verify_installation"):
                print "=== plugin: '%s'" % mem.__name__
                print "    file: %s" % mem.__file__
                print "    version: %s" % (str(getattr(mem, "__version__")))

                try:
                    if mem.verify_installation(request) == 1:
                        print "    PASS"
                    else:
                        print "    FAIL!!!"
                except AssertionError, error_message:
                    print " FAIL!!! ", error_message

            else:
                mn = mem.__name__
                mf = mem.__file__
                no_verification_support.append( "'%s' (%s)" % (mn, mf))

        if len(no_verification_support) > 0:
            print ""
            print "The following plugins do not support installation " + \
                  "verification:"
            for mem in no_verification_support:
                print "   %s" % mem
    else:
        print "You have chosen not to load any plugins."


def create_blog(d):
    """
    Creates a blog in the specified directory.  Mostly this involves
    copying things over, but there are a few cases where we expand
    template variables.
    """
    if d == ".":
        d = "./blog"

    d = os.path.abspath(d)
    
    if os.path.isfile(d) or os.path.isdir(d):
        print "Cannot create '%s'--something is in the way." % d
        return 0

    def mkdir(d):
        print "Creating '%s'..." % d
        os.makedirs(d)

    mkdir(d)
    mkdir(os.path.join(d, "entries"))
    mkdir(os.path.join(d, "plugins"))
    # mkdir(os.path.join(d, "flavours"))

    def copyfile(frompath, topath, fn, fix=0):
        print "Creating '%s'..." % os.path.join(topath, fn)
        fp = open(os.path.join(frompath, fn), "r")
        filedata = fp.readlines()
        fp.close()

        if fix:
            datamap = { "basedir": topath }
            filedata = [line % datamap for line in filedata]

        fp = open(os.path.join(topath, fn), "w")
        fp.write("".join(filedata))
        fp.close()

    def copydir(arg, dirname, names):
        frompath = dirname
        topath = os.path.join(os.path.join(d, "flavours"),
                              dirname[len(path)+1:])
        mkdir(topath)
        for name in names:
            fn = os.path.join(frompath, name)
            
            if os.path.isfile(fn):
                copyfile(frompath, topath, name, 0)

    path = os.path.join(os.path.dirname(__file__), "flavours")

    os.path.walk(path, copydir, [])

    path = os.path.join(os.path.dirname(__file__), "data")

    copyfile(path, d, "config.py", 1)
    copyfile(path, d, "blog.ini", 1)
    copyfile(path, d, "pyblosxom.cgi", 0)

    datadir = os.path.join(d, "entries")
    firstpost = os.path.join(datadir, "firstpost.txt")
    print "Creating '%s'..." % firstpost
    fp = open(firstpost, "w")
    fp.write("""First post!
<p>
  This is your first post!  If you can see this with a web-browser,
  then it's likely that everything's working nicely!
</p>
""")
    fp.close()


def command_line_handler(scriptname, argv):
    """
    Handles calling PyBlosxom from the command line.  This can be
    called from two different things: pyblosxom.cgi and pyblcmd.

    @param scriptname: the name of the script (ex. "pyblcmd")
    @type  scriptname: string

    @param argv: the arguments passed in
    @type  argv: list of strings

    @returns: the exit code
    """
    def printq(s):
        print s

    # parse initial command line variables that don't require config
    optlist = tools.parse_args(argv)
    for mem in optlist:
        if mem[0] in ["-c", "--config"]:
            m = mem[1]
            if m.endswith("config.py"):
                m = m[0:-9]
            printq("Appending %s to sys.path for config.py location." % m)
            sys.path.append(m)

        elif mem[0] in ["-C", "--create"]:
            return create_blog(mem[1])

        elif mem[0] in ["-q", "--quiet"]:
            # this quiets the printing by doing nothing with the input
            printq = lambda s : s

        elif mem[0] in ["-v", "--version"]:
            return 0

        elif mem[0] in ["-h", "--help"]: 
            print HELP % { "script": scriptname }
            return 0

 
    # the configuration properties are in a dict named "py" in
    # the config module
    printq("Trying to import the config module....")
    try:
        from config import py as cfg
    except:
        print "Error: Cannot find your config.py file.  Please execute %s in\n" \
              % scriptname
        print "the directory with your config.py file in it."
        return 0

    # If the user defined a "codebase" property in their config file,
    # then we insert that into our sys.path because that's where the
    # PyBlosxom installation is.
    # NOTE: this _has_ to come before any PyBlosxom calls.
    if "codebase" in cfg:
        sys.path.append(cfg["codebase"])

    printq("PyBlosxom version: %s" % VERSION_DATE)

    if len(argv) == 0:
        print HELP % { "script": scriptname }
        return 0

    p = PyBlosxom(cfg, {})
    headers = 0

    for mem in optlist:
        if mem[0] in ["--static", "-s"]:
            if mem[1].startswith("incr"):
                incremental = 1
            else:
                incremental = 0

            p.runStaticRenderer(incremental)

        elif mem[0] in ["--headers", "-h"]:
            headers = 1

        elif mem[0] in ["--render", "-r"]:
            url = mem[1]
            if url.startswith(cfg.get("base_url", "")):
                url = url[len(cfg.get("base_url", "")):]

            printq("Rendering '%s'" % url)

            p.runRenderOne(url, headers)

        elif mem[0] in ["--test", "-t"]:
            p.testInstallation()

    return 0

# vim: shiftwidth=4 tabstop=4 expandtab
