import _path_pyblosxom

from nose.tools import eq_

from helpers import req_

from Pyblosxom import tools
from Pyblosxom import plugin_utils
from Pyblosxom.entries.base import EntryBase

class Testcallbacks:
    def _setup(self, plugins):
        plugin_utils.callbacks = plugins

    def _teardown(self):
        plugin_utils.callbacks = {}

    def test_defaults(self):
        # pass args to f1,
        # f1 returns 1,
        # mappingfunc maps (args, 1) to args,
        # pass args to f2,
        # f2 returns 2
        # run_callback returns the last output item, which is 2.
        try:
            self._setup({"test": [lambda args: args["item1"],
                                  lambda args: args["item2"]]})
            yield eq_, tools.run_callback("test", {"item1": 1, "item2": 2}), 2
        finally:
            self._teardown()

    def test_default_returnitem(self):
        f1 = tools.default_returnitem("foo")
        yield eq_, f1({"foo": "bar"}), "bar"
        yield eq_, f1({"foo": "bar", "foo2": "baz"}), "bar"

    def test_handler(self):
        # FIXME - test handler-style callback
        pass

    def test_handler(self):
        # FIXME - test chain-style callback
        pass

    def test_getFromCache(self):
        try:
            cache = {}
            cache2 = {}

            def get_from_cache(args):
                return cache.get(args["id"])

            def get_from_cache2(args):
                return cache2.get(args["id"])

            def update_cache(args):
                cache[args["id"]] = args["data"]

            def update_cache2(args):
                cache2[args["id"]] = args["data"]

            self._setup({"entrycache_get": [get_from_cache],
                         "entrycache_update": [update_cache, update_cache2]})

            r = req_()
            e = EntryBase(r)
            e._id = "testentry"
            yield eq_, e.getFromCache(), None

            foo = {"foo": "bar"}
            e.updateCache(foo)
            yield eq_, e.getFromCache(), foo
            yield eq_, cache["testentry"]["foo"], "bar"
            yield eq_, cache2["testentry"]["foo"], "bar"
        finally:
            self._teardown()
