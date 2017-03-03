#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################


"""This is the main module for Pyblosxom functionality.  Pyblosxom's
setup and default handlers are defined here.
"""



# Python imports
import cgi
import locale
import os
import sys
import time
from Pyblosxom.blosxom import blosxom_entry_parser, blosxom_handler

try:
    from io import BytesIO
except ImportError:
    from io import BytesIO

# Pyblosxom imports
from Pyblosxom import __version__
from Pyblosxom import crashhandling
from Pyblosxom import tools
from Pyblosxom import plugin_utils


VERSION = __version__


class Pyblosxom:
    """Main class for Pyblosxom functionality.  It handles
    initialization, defines default behavior, and also pushes the
    request through all the steps until the output is rendered and
    we're complete.
    """

    def __init__(self, config, environ, data=None):
        """Sets configuration and environment and creates the Request
        object.

        :param config: dict containing the configuration variables.
        :param environ: dict containing the environment variables.
        :param data: dict containing data variables.
        """
        # FIXME: These shouldn't be here.
        config['pyblosxom_name'] = "pyblosxom"
        config['pyblosxom_version'] = __version__

        self._config = config
        self._request = Request(config, environ, data)

    def initialize(self):
        """The initialize step further initializes the Request by
        setting additional information in the ``data`` dict,
        registering plugins, and entryparsers.
        """
        data = self._request.get_data()
        py_http = self._request.get_http()
        config = self._request.get_configuration()

        # initialize the locale, if wanted (will silently fail if locale
        # is not available)
        if config.get('locale', None):
            try:
                locale.setlocale(locale.LC_ALL, config['locale'])
            except locale.Error:
                # invalid locale
                pass

        # initialize the tools module
        tools.initialize(config)

        data["pyblosxom_version"] = __version__
        data['pi_bl'] = ''

        # if the user specifies base_url in config, we use that.
        # otherwise we compose it from SCRIPT_NAME in the environment
        # or we leave it blank.
        if not "base_url" in config:
            if 'SCRIPT_NAME' in py_http:
                # allow http and https
                config['base_url'] = '%s://%s%s' % \
                                     (py_http['wsgi.url_scheme'],
                                      py_http['HTTP_HOST'],
                                      py_http['SCRIPT_NAME'])
            else:
                config["base_url"] = ""

        # take off the trailing slash for base_url
        if config['base_url'].endswith("/"):
            config['base_url'] = config['base_url'][:-1]

        data_dir = config["datadir"]
        if data_dir.endswith("/") or data_dir.endswith("\\"):
            data_dir = data_dir[:-1]
            config['datadir'] = data_dir

        # import and initialize plugins
        plugin_utils.initialize_plugins(config.get("plugin_dirs", []),
                                        config.get("load_plugins", None))

        # entryparser callback is run here first to allow other
        # plugins register what file extensions can be used
        data['extensions'] = tools.run_callback("entryparser",
                                                {'txt': blosxom_entry_parser},
                                                mappingfunc=lambda x, y: y,
                                                defaultfunc=lambda x: x)

    def cleanup(self):
        """This cleans up Pyblosxom after a run.

        This should be called when Pyblosxom has done everything it
        needs to do before exiting.
        """
        # log some useful stuff for debugging
        # this will only be logged if the log_level is "debug"
        log = tools.getLogger()
        response = self.get_response()
        log.debug("status = %s" % response.status)
        log.debug("headers = %s" % response.headers)

    def get_request(self):
        """Returns the Request object for this Pyblosxom instance.
        """
        return self._request

    getRequest = tools.deprecated_function(get_request)

    def get_response(self):
        """Returns the Response object associated with this Request.
        """
        return self._request.getResponse()

    getResponse = tools.deprecated_function(get_response)

    def run(self, static=False):
        """This is the main loop for Pyblosxom.  This method will run
        the handle callback to allow registered handlers to handle the
        request.  If nothing handles the request, then we use the
        ``default_blosxom_handler``.

        :param static: True if Pyblosxom should execute in "static rendering
                       mode" and False otherwise.
        """
        self.initialize()

        # buffer the input stream in a BytesIO instance if dynamic
        # rendering is used.  This is done to have a known/consistent
        # way of accessing incoming data.
        if not static:
            self.get_request().buffer_input_stream()

        # run the start callback
        tools.run_callback("start", {'request': self._request})

        # allow anyone else to handle the request at this point
        handled = tools.run_callback("handle",
                                     {'request': self._request},
                                     mappingfunc=lambda x, y: x,
                                     donefunc=lambda x: x)

        if not handled == 1:
            blosxom_handler(self._request)

        # do end callback
        tools.run_callback("end", {'request': self._request})

        # we're done, clean up.
        # only call this if we're not in static rendering mode.
        if not static:
            self.cleanup()

    def run_callback(self, callback="help"):
        """This method executes the start callback (initializing
        plugins), executes the requested callback, and then executes
        the end callback.

        This is useful for scripts outside of Pyblosxom that need to
        do things inside of the Pyblosxom framework.

        If you want to run a callback from a plugin, use
        ``tools.run_callback`` instead.

        :param callback: the name of the callback to execute.

        :returns: the results of the callback.
        """
        self.initialize()

        # run the start callback
        tools.run_callback("start", {'request': self._request})

        # invoke all callbacks for the 'callback'
        handled = tools.run_callback(callback,
                                     {'request': self._request},
                                     mappingfunc=lambda x, y: x,
                                     donefunc=lambda x: x)

        # do end callback
        tools.run_callback("end", {'request': self._request})

        return handled

    runCallback = tools.deprecated_function(run_callback)

    def run_render_one(self, url, headers):
        """Renders a single page from the blog.

        :param url: the url to render--this has to be relative to the
                    base url for this blog.

        :param headers: True if you want headers to be rendered and
                        False if not.
        """
        self.initialize()

        config = self._request.get_configuration()

        if url.find("?") != -1:
            url = url[:url.find("?")]
            query = url[url.find("?") + 1:]
        else:
            query = ""

        url = url.replace(os.sep, "/")
        response = tools.render_url(config, url, query)
        if headers:
            response.send_headers(sys.stdout)
        response.send_body(sys.stdout)

        print(response.read())

        # we're done, clean up
        self.cleanup()

    def run_static_renderer(self, incremental=False):
        """This will go through all possible things in the blog and
        statically render everything to the ``static_dir`` specified
        in the config file.

        This figures out all the possible ``path_info`` settings and
        calls ``self.run()`` a bazillion times saving each file.

        :param incremental: Whether (True) or not (False) to
                            incrementally render the pages.  If we're
                            incrementally rendering pages, then we
                            render only the ones that have changed.
        """
        self.initialize()

        config = self._request.get_configuration()
        data = self._request.get_data()
        print("Performing static rendering.")
        if incremental:
            print("Incremental is set.")

        static_dir = config.get("static_dir", "")
        data_dir = config["datadir"]

        if not static_dir:
            print("Error: You must set static_dir in your config file.")
            return 0

        flavours = config.get("static_flavours", ["html"])
        index_flavours = config.get("static_index_flavours", ["html"])

        render_me = []

        month_names = config.get("static_monthnames", True)
        month_numbers = config.get("static_monthnumbers", False)
        year_indexes = config.get("static_yearindexes", True)

        dates = {}
        categories = {}

        # first we handle entries and categories
        listing = tools.walk(self._request, data_dir)

        for mem in listing:
            # skip the ones that have bad extensions
            ext = mem[mem.rfind(".") + 1:]
            if not ext in list(data["extensions"].keys()):
                continue

            # grab the mtime of the entry file
            mtime = time.mktime(tools.filestat(self._request, mem))

            # remove the datadir from the front and the bit at the end
            mem = mem[len(data_dir):mem.rfind(".")]

            # this is the static filename
            fn = os.path.normpath(static_dir + mem)

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
                for i in range(len(temp) + 1):
                    p = os.sep.join(temp[0:i])
                    categories[p] = 0

                # grab the date
                mtime = time.localtime(mtime)
                year = time.strftime("%Y", mtime)
                month = time.strftime("%m", mtime)
                day = time.strftime("%d", mtime)

                if year_indexes:
                    dates[year] = 1

                if month_numbers:
                    dates[year + "/" + month] = 1
                    dates[year + "/" + month + "/" + day] = 1

                if month_names:
                    monthname = tools.num2month[month]
                    dates[year + "/" + monthname] = 1
                    dates[year + "/" + monthname + "/" + day] = 1

                # toss in the render queue
                for f in flavours:
                    render_me.append((mem + "." + f, ""))

        print("rendering %d entries." % len(render_me))

        # handle categories
        categories = list(categories.keys())
        categories.sort()

        # if they have stuff in their root category, it'll add a "/"
        # to the category list and we want to remove that because it's
        # a duplicate of "".
        if "/" in categories:
            categories.remove("/")

        print("rendering %d category indexes." % len(categories))

        for mem in categories:
            mem = os.path.normpath(mem + "/index.")
            for f in index_flavours:
                render_me.append((mem + f, ""))

        # now we handle dates
        dates = list(dates.keys())
        dates.sort()

        dates = ["/" + d for d in dates]

        print("rendering %d date indexes." % len(dates))

        for mem in dates:
            mem = os.path.normpath(mem + "/index.")
            for f in index_flavours:
                render_me.append((mem + f, ""))

        # now we handle arbitrary urls
        additional_stuff = config.get("static_urls", [])
        print("rendering %d arbitrary urls." % len(additional_stuff))

        for mem in additional_stuff:
            if mem.find("?") != -1:
                url = mem[:mem.find("?")]
                query = mem[mem.find("?") + 1:]
            else:
                url = mem
                query = ""

            render_me.append((url, query))

        # now we pass the complete render list to all the plugins via
        # cb_staticrender_filelist and they can add to the filelist
        # any (url, query) tuples they want rendered.
        print("(before) building %s files." % len(render_me))
        tools.run_callback("staticrender_filelist",
                           {'request': self._request,
                            'filelist': render_me,
                            'flavours': flavours,
                            'incremental': incremental})

        render_me = sorted(set(render_me))

        print("building %s files." % len(render_me))

        for url, q in render_me:
            url = url.replace(os.sep, "/")
            print("rendering '%s' ..." % url)

            tools.render_url_statically(dict(config), url, q)

        # we're done, clean up
        self.cleanup()


Pyblosxom = Pyblosxom


class PyblosxomWSGIApp:
    """This class is the WSGI application for Pyblosxom.
    """

    def __init__(self, environ=None, start_response=None, configini=None):
        """
        Make WSGI app for Pyblosxom.

        :param environ: FIXME

        :param start_response: FIXME

        :param configini: Dict encapsulating information from a
                          ``config.ini`` file or any other property
                          file that will override the ``config.py``
                          file.
        """
        self.environ = environ
        self.start_response = start_response

        if configini is None:
            configini = {}

        _config = tools.convert_configini_values(configini)

        import config

        self.config = dict(config.py)

        self.config.update(_config)
        if "codebase" in _config:
            sys.path.insert(0, _config["codebase"])

    def run_pyblosxom(self, env, start_response):
        """
        Executes a single run of Pyblosxom wrapped in the crash handler.
        """
        try:
            # ensure that PATH_INFO exists. a few plugins break if this is
            # missing.
            if "PATH_INFO" not in env:
                env["PATH_INFO"] = ""

            p = Pyblosxom(dict(self.config), env)
            p.run()

            response = p.get_response()

        except Exception:
            ch = crashhandling.CrashHandler(True, env)
            response = ch.handle_by_response(*sys.exc_info())

        start_response(response.status, list(response.headers.items()))
        response.seek(0)

        return response.read()

    def __call__(self, env, start_response):
        return [self.run_pyblosxom(env, start_response)]

    def __iter__(self):
        yield self.run_pyblosxom(self.environ, self.start_response)


# Do this for historical reasons
PyblosxomWSGIApp = PyblosxomWSGIApp


def pyblosxom_app_factory(global_config, **local_config):
    """App factory for paste.

    :returns: WSGI application
    """
    conf = global_config.copy()
    conf.update(local_config)
    conf.update(dict(local_config=local_config, global_config=global_config))

    if "configpydir" in conf:
        sys.path.insert(0, conf["configpydir"])

    return PyblosxomWSGIApp(configini=conf)


class EnvDict(dict):
    """Wrapper around a dict to provide a backwards compatible way to
    get the ``form`` with syntax as::

        request.get_http()['form']

    instead of::

        request.get_form()
    """

    def __init__(self, request, env):
        """Wraps an environment (which is a dict) and a request.

        :param request: the Request object for this request.
        :param env: the environment dict for this request.
        """
        dict.__init__(self)
        self._request = request
        self.update(env)

    def __getitem__(self, key):
        """If the key argument is ``form``, we return
        ``_request.get_form()``.  Otherwise this returns the item for
        that key in the wrapped dict.
        """
        if key == "form":
            return self._request.get_form()

        return dict.__getitem__(self, key)


class Request(object):
    """
    This class holds the Pyblosxom request.  It holds configuration
    information, HTTP/CGI information, and data that we calculate and
    transform over the course of execution.

    There should be only one instance of this class floating around
    and it should get created by ``pyblosxom.cgi`` and passed into the
    Pyblosxom instance which will do further manipulation on the
    Request instance.
    """

    def __init__(self, config, environ, data):
        """Sets configuration and environment.

        Creates the Response object which handles all output related
        functionality.

        :param config: dict containing configuration variables.
        :param environ: dict containing environment variables.
        :param data: dict containing data variables.
        """
        # this holds configuration data that the user changes in
        # config.py
        self._configuration = config

        # this holds HTTP/CGI oriented data specific to the request
        # and the environment in which the request was created
        self._http = EnvDict(self, environ)

        # this holds run-time data which gets created and transformed
        # by pyblosxom during execution
        if data is None:
            self._data = dict()
        else:
            self._data = data

        # this holds the input stream.  initialized for dynamic
        # rendering in Pyblosxom.run.  for static rendering there is
        # no input stream.
        self._in = BytesIO()

        # copy methods to the Request object.
        self.read = self._in.read
        self.readline = self._in.readline
        self.readlines = self._in.readlines
        self.seek = self._in.seek
        self.tell = self._in.tell

        # this holds the FieldStorage instance.
        # initialized when request.get_form is called the first time
        self._form = None

        self._response = None

        # create and set the Response
        self.setResponse(Response(self))

    def __iter__(self):
        """
        Can't copy the __iter__ method over from the BytesIO instance
        cause iter looks for the method in the class instead of the
        instance.

        See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252151
        """
        return self._in

    def buffer_input_stream(self):
        """
        Buffer the input stream in a BytesIO instance.  This is done
        to have a known/consistent way of accessing incoming data.
        For example the input stream passed by mod_python does not
        offer the same functionality as ``sys.stdin``.
        """
        # TODO: tests on memory consumption when uploading huge files
        py_http = self.get_http()
        winput = py_http['wsgi.input']
        method = py_http["REQUEST_METHOD"]

        # there's no data on stdin for a GET request.  pyblosxom
        # will block indefinitely on the read for a GET request with
        # thttpd.
        if method != "GET":
            try:
                length = int(py_http.get("CONTENT_LENGTH", 0))
            except ValueError:
                length = 0

            if length > 0:
                self._in.write(winput.read(length))
                # rewind to start
                self._in.seek(0)

    def set_response(self, response):
        """Sets the Response object.
        """
        self._response = response
        # for backwards compatibility
        self.get_configuration()['stdoutput'] = response

    setResponse = tools.deprecated_function(set_response)

    def get_response(self):
        """Returns the Response for this request.
        """
        return self._response

    getResponse = tools.deprecated_function(get_response)

    def _getform(self):
        form = cgi.FieldStorage(fp=self._in,
                                environ=self._http,
                                keep_blank_values=0)
        # rewind the input buffer
        self._in.seek(0)
        return form

    def get_form(self):
        """Returns the form data submitted by the client.  The
        ``form`` instance is created only when requested to prevent
        overhead and unnecessary consumption of the input stream.

        :returns: a ``cgi.FieldStorage`` instance.
        """
        if self._form is None:
            self._form = self._getform()
        return self._form

    getForm = tools.deprecated_function(get_form)

    def get_configuration(self):
        """Returns the *actual* configuration dict.  The configuration
        dict holds values that the user sets in their ``config.py``
        file.

        Modifying the contents of the dict will affect all downstream
        processing.
        """
        return self._configuration

    getConfiguration = tools.deprecated_function(get_configuration)

    def get_http(self):
        """Returns the *actual* http dict.  Holds HTTP/CGI data
        derived from the environment of execution.

        Modifying the contents of the dict will affect all downstream
        processing.
        """
        return self._http

    getHttp = tools.deprecated_function(get_http)

    def get_data(self):
        """Returns the *actual* data dict.  Holds run-time data which
        is created and transformed by pyblosxom during execution.

        Modifying the contents of the dict will affect all downstream
        processing.
        """
        return self._data

    getData = tools.deprecated_function(get_data)

    def add_http(self, d):
        """Takes in a dict and adds/overrides values in the existing
        http dict with the new values.
        """
        self._http.update(d)

    addHttp = tools.deprecated_function(add_http)

    def add_data(self, d):
        """Takes in a dict and adds/overrides values in the existing
        data dict with the new values.
        """
        self._data.update(d)

    addData = tools.deprecated_function(add_data)

    def add_configuration(self, newdict):
        """Takes in a dict and adds/overrides values in the existing
        configuration dict with the new values.
        """
        self._configuration.update(newdict)

    addConfiguration = tools.deprecated_function(add_configuration)

    def __getattr__(self, name):
        if name in ["config", "configuration", "conf"]:
            return self._configuration

        if name == "data":
            return self._data

        if name == "http":
            return self._http

        raise AttributeError(name)

    def __repr__(self):
        return "Request"


class Response(object):
    """Response class to handle all output related tasks in one place.

    This class is basically a wrapper arround a ``BytesIO`` instance.
    It also provides methods for managing http headers.
    """

    def __init__(self, request):
        """Sets the ``Request`` object that leaded to this response.
        Creates a ``BytesIO`` that is used as a output buffer.
        """
        self._request = request
        self._out = BytesIO()
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
        """Can't copy the ``__iter__`` method over from the
        ``BytesIO`` instance because iter looks for the method in the
        class instead of the instance.

        See
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252151
        """
        return self._out

    def set_status(self, status):
        """Sets the status code for this response.  The status should
        be a valid HTTP response status.

        Examples:

        >>> resp = Response('some fake request')
        >>> resp.set_status("200 OK")
        >>> resp.set_status("404 Not Found")

        :param status: the status string.
        """
        self.status = status

    setStatus = tools.deprecated_function(set_status)

    def get_status(self):
        """Returns the status code and message of this response.
        """
        return self.status

    def add_header(self, key, value):
        """Populates the HTTP header with lines of text.  Sets the
        status code on this response object if the given argument list
        contains a 'Status' header.

        Example:

        >>> resp = Response('some fake request')
        >>> resp.add_header("Content-type", "text/plain")
        >>> resp.add_header("Content-Length", "10500")

        :raises ValueError: This happens when the parameters are
                            not correct.
        """
        key = key.strip()
        if key.find(' ') != -1 or key.find(':') != -1:
            raise ValueError('There should be no spaces in header keys')
        value = value.strip()
        if key.lower() == "status":
            self.setStatus(str(value))
        else:
            self.headers.update({key: str(value)})

    addHeader = tools.deprecated_function(add_header)

    def get_headers(self):
        """Returns the headers.
        """
        return self.headers

    getHeaders = tools.deprecated_function(get_headers)

    def send_headers(self, out):
        """Send HTTP Headers to the given output stream.

        .. Note::

            This prints the headers and then the ``\\n\\n`` that
            separates headers from the body.

        :param out: The file-like object to print headers to.
        """
        out.write("Status: %s\n" % self.status)
        out.write('\n'.join(['%s: %s' % (hkey, self.headers[hkey])
                             for hkey in list(self.headers.keys())]))
        out.write('\n\n')
        self._headers_sent = True

    sendHeaders = tools.deprecated_function(send_headers)

    def send_body(self, out):
        """Send the response body to the given output stream.

        :param out: the file-like object to print the body to.
        """
        self.seek(0)
        try:
            out.write(self.read())
        except IOError:
            # this is usually a Broken Pipe because the client dropped the
            # connection.  so we skip it.
            pass

    sendBody = tools.deprecated_function(send_body)


def run_pyblosxom():
    """Executes Pyblosxom either as a commandline script or CGI
    script.
    """
    from config import py as cfg

    env = {}

    # if there's no REQUEST_METHOD, then this is being run on the
    # command line and we should execute the command_line_handler.
    if not "REQUEST_METHOD" in os.environ:
        from .Pyblosxom.commandline import command_line_handler

        if len(sys.argv) <= 1:
            sys.argv.append("test")

        sys.exit(command_line_handler("pyblosxom.cgi", sys.argv))

    # names taken from wsgi instead of inventing something new
    env['wsgi.input'] = sys.stdin
    env['wsgi.errors'] = sys.stderr

    # figure out what the protocol is for the wsgi.url_scheme
    # property.  we look at the base_url first and if there's nothing
    # set there, we look at environ.
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

        CGIHandler().run(PyblosxomWSGIApp())

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

        p = Pyblosxom(dict(cfg), env)

        p.run()
        response = p.get_response()
        response.send_headers(sys.stdout)
        response.send_body(sys.stdout)
