"""
A base class and utilities for external unit testing of PyBlosxom
plugins.

Includes up a number of mocks, environment variables, and PyBlosxom
data structures for useful testing plugins.
"""

__author__ = 'Ryan Barrett <pyblosxom@ryanb.org>'
__url__ = 'http://pyblosxom.sourceforge.net/wiki/index.php/Framework_for_testing_plugins'

from Pyblosxom import pyblosxom, tools, entries
from Pyblosxom.renderers.blosxom import Renderer
import cgi, cStringIO, os, tempfile, time, urllib

import unittest

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

    Many common PyBlosxom data structures are populated as attributes
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
        self.datadir = tempfile.mkdtemp(prefix='pyblosxom_test_datadir',
                                        dir='/tmp')

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
        """Injects a frozen time module into PyBlosxom.

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

        encoded = ['%s=%s' % (arg, urllib.quote(val))
                   for arg, val in args.items()]
        self.form_data += ('&' + '&'.join(encoded))
        input_ = cStringIO.StringIO(self.form_data)
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
        if os.path.isdir(self.datadir):
            for root, subdirs, files in os.walk(dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in subdirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(dir)
