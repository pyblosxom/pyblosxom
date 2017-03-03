#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Testing utilities.

Includes up a number of mocks, environment variables, and Pyblosxom
data structures for useful testing plugins.
"""

from Pyblosxom import pyblosxom, tools, entries
from Pyblosxom.renderers.blosxom import Renderer
import cgi
import io
import os
import os.path
import tempfile
import time
import urllib.request, urllib.parse, urllib.error
import shutil
import unittest


def req_():
    return pyblosxom.Request({}, {}, {})


class UnitTestBase(unittest.TestCase):
    def setUp(self):
        self._tempdir = None

    def tearDown(self):
        if self._tempdir:
            try:
                shutil.rmtree(self._tempdir)
            except OSError:
                pass

    def eq_(self, a, b, text=None):
        self.assertEqual(a, b, text)

    def get_temp_dir(self):
        if self._tempdir == None:
            self._tempdir = tempfile.mkdtemp()
        return self._tempdir

    def setup_files(self, files):
        # sort so that we're building the directories in order
        files.sort()

        tempdir = self.get_temp_dir()
        os.makedirs(os.path.join(tempdir, "entries"))

        for fn in files:
            d, f = os.path.split(fn)

            try:
                os.makedirs(d)
            except OSError as e:
                pass

            if f:
                f = open(fn, "w")
                f.write("test file: %s\n" % fn)
                f.close()
            
    def build_file_set(self, filelist):
        return [os.path.join(self.get_temp_dir(), "entries/%s" % fn)
                for fn in filelist]

    def build_request(self, cfg=None, http=None, data=None, inputstream=""):
        """
        process_path_info uses:
        - req.pyhttp["PATH_INFO"]         - string

        - req.config["default_flavour"]   - string
        - req.config["datadir"]           - string
        - req.config["blog_title"]        - string
        - req.config["base_url"]          - string

        - req.data["extensions"]          - dict of string -> func

        if using req.get_form():
        - req.pyhttp["wsgi.input"]        - StringIO instance
        - req.pyhttp["REQUEST_METHOD"]    - GET or POST
        - req.pyhttp["CONTENT_LENGTH"]    - integer
        """
        _config = {"default_flavour": "html",
                   "datadir": os.path.join(self.get_temp_dir(), "entries"),
                   "blog_title": "Joe's blog",
                   "base_url": "http://www.example.com/"}
        if cfg:
            _config.update(cfg)

        _data = {"extensions": {"txt": 0}}
        if data:
            _data.update(data)

        _http = {"wsgi.input": io.StringIO(inputstream),
                 "REQUEST_METHOD": len(inputstream) and "GET" or "POST",
                 "CONTENT_LENGTH": len(inputstream)}
        if http: _http.update(http)

        return pyblosxom.Request(_config, _http, _data)
        
    def test_setup_teardown(self):
        fileset1 = self.build_file_set(["file.txt",
                                        "cata/file.txt",
                                        "cata/subcatb/file.txt"])

        self.setup_files(fileset1)
        try:
            for mem in fileset1:
                assert os.path.isfile(mem)

        finally:
            self.tearDown()

        for mem in fileset1:
            assert not os.path.isfile(mem)

    def cmpdict(self, expected, actual):
        """expected <= actual
        """
        for mem in list(expected.keys()):
            if mem in actual:
                self.assertEqual(expected[mem], actual[mem])
            else:
                assert False, "%s not in actual" % mem


TIMESTAMP = time.mktime(time.strptime('Wed Dec 26 11:00:00 2007'))


class FrozenTime:
    """Wraps the time module to provide a single, frozen timestamp.

    Allows for dependency injection."""
    def __init__(self, timestamp):
        """Sets the time to timestamp, as seconds since the epoch."""
        self.timestamp = timestamp

    def __getattr__(self, attr):
        if attr == 'time':
            return lambda: self.timestamp
        else:
            return getattr(time, attr)


class PluginTest(unittest.TestCase):
    """Base class for plugin unit tests. Subclass this to test
    plugins.

    Many common Pyblosxom data structures are populated as attributes
    of this class, including self.environ, self.config, self.data,
    self.request, and self.args.

    By default, self.request is configured as a request for a single
    entry; its name is stored in self.entry_name. This can be
    overridden by modifying the attributes above in your test's
    setUp() method. The entry's timestamp, as seconds since the epoch,
    is stored in self.timestamp. String representations in
    self.timestamp_str and self.timestamp_w3c.

    You can change any of the data structures by modifying them
    directly in your tests or your subclass's setUp() method.

    The datadir is set to a unique temporary directory in /tmp. This
    directory is created fresh for each test, and deleted when the
    test is done.

    NOTE(ryanbarrett): Creating and deleting multiple files and
    directories for each test is inefficient. If this becomes a
    bottleneck, it might need to be reconsidered.
    """

    def setUp(self, plugin_module):
        """Subclasses should call this in their setUp() methods.

        The plugin_module arg is the plugin module being tested. This
        is used to set the plugin_dir config variable.
        """
        # freeze time
        self.timestamp = TIMESTAMP
        self.frozen_time = self.freeze_pyblosxom_time(self.timestamp)
        self.timestamp_asc = time.ctime(self.timestamp)
        gmtime = time.gmtime(self.timestamp)
        self.timestamp_date = time.strftime('%a %d %b %Y', gmtime)
        self.timestamp_w3c = time.strftime('%Y-%m-%dT%H:%M:%SZ', gmtime)

        # set up config, including datadir and plugin_dirs
        self.datadir = tempfile.mkdtemp(prefix='pyblosxom_test_datadir')

        plugin_file = os.path.dirname(plugin_module.__file__)
        self.config_base = {'datadir': self.datadir,
                            'plugin_dirs': [plugin_file],
                            'base_url': 'http://bl.og/',
                            }
        self.config = self.config_base
        tools.initialize(self.config)

        # set up environment vars and http request
        self.environ = {'PATH_INFO': '/', 'REMOTE_ADDR': ''}
        self.form_data = ''
        self.request = pyblosxom.Request(self.config, self.environ, {})
        self.http = self.request.get_http()

        # set up entries and data dict
        self.entry_name = 'test_entry'
        entry_properties = {'absolute_path': '.',
                            'fn': self.entry_name}
        self.entry = entries.base.generate_entry(
            self.request, entry_properties, {}, gmtime)
        self.entry_list = [self.entry]
        self.data = {'entry_list': self.entry_list,
                     'bl_type': 'file',
                     }
        self.request._data = self.data

        # set up renderer and templates
        self.renderer = Renderer(self.request)
        self.renderer.set_content(self.entry_list)
        templates = ('content_type', 'head', 'story', 'foot', 'date_head',
                     'date_foot')
        self.renderer.flavour = dict([(t, t) for t in templates])

        # populate args dict
        self.args = {'request': self.request,
                     'renderer': self.renderer,
                     'entry': self.entry,
                     'template': 'template starts:',
                     }

        # this stores the callbacks that have been injected. it maps
        # callback names to the injected methods to call. any
        # callbacks that haven't been injected are passed through to
        # pyblosxom's callback chain.
        #
        # use inject_callback() to inject a callback.
        self.injected_callbacks = {}
        orig_run_callback = tools.run_callback

        def intercept_callback(name, args, **kwargs):
            if name in self.injected_callbacks:
                return self.injected_callbacks[name]()
            else:
                return orig_run_callback(name, args, **kwargs)

        tools.run_callback = intercept_callback

    def tearDown(self):
        """Subclasses should call this in their tearDown() methods."""
        self.delete_datadir()

    def delete_datadir(self):
        """Deletes the datadir and its contents."""
        self.remove_dir(self.datadir)

    def freeze_pyblosxom_time(self, timestamp):
        """Injects a frozen time module into Pyblosxom.

        The timestamp argument should be seconds since the epoch. Returns the
        FrozenTime instance.
        """
        assert isinstance(timestamp, (int, float))
        frozen_time = FrozenTime(timestamp)
        pyblosxom.time = frozen_time
        tools.time = frozen_time
        return frozen_time

    def add_form_data(self, args):
        """Adds the given argument names and values to the request's form data.

        The argument names and values are URL-encoded and escaped before
        populating them in the request. This method also sets the request
        method to POST.
        """
        self.environ['REQUEST_METHOD'] = 'POST'
        self.request.add_http({'REQUEST_METHOD': 'POST'})

        encoded = ['%s=%s' % (arg, urllib.parse.quote(val))
                   for arg, val in list(args.items())]
        self.form_data += ('&' + '&'.join(encoded))
        tmpdata = self.form_data
        tmpdata = bytes(tmpdata, 'utf-8')
        input_ = io.BytesIO(tmpdata)

        self.request._form = cgi.FieldStorage(fp=input_, environ=self.environ)

    def set_form_data(self, args):
        """Clears the request's form data, then adds the given
        arguments.
        """
        self.form_data = ''
        self.add_form_data(args)

    def inject_callback(self, name, callback):
        """Injects a callback to be run by tools.run_callback().

        The callback is run *instead* of Pyblosxom's standard callback
        chain.
        """
        self.injected_callbacks[name] = callback

    def remove_dir(self, dir):
        """Recursively removes a directory and all files and
        subdirectories.

        If dir doesn't exist or is not a directory, does nothing.
        """
        shutil.rmtree(self.datadir, ignore_errors=True)

    # allows us to use shorthand
    eq_ = unittest.TestCase.assertEqual
