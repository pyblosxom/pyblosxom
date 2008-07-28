import _path_pyblosxom

from nose.tools import eq_

from helpers import req_

from Pyblosxom import tools
from Pyblosxom import plugin_utils
from Pyblosxom.entries.base import EntryBase

def rc(chain, args):
    ret = tools.run_callback(chain, args)
    print repr(ret)
    return ret

class Testcallbacks:
    def _setup(self, plugins):
        plugin_utils.callbacks = plugins

    def _teardown(self):
        plugin_utils.callbacks = {}

    def test_defaults(self):
        try:
            args = { "item1": 1, "item2": 2 }

            def f1(args):
                return args["item1"]
            def f2(args):
                return args["item2"]

            self._setup({"test": [f1, f2]})

            # pass args to f1, 
            # f1 returns 1, 
            # mappingfunc maps (args, 1) to args,
            # pass args to f2,
            # f2 returns 2
            # run_callback returns the last output item, which is 2.
            assert rc("test", args) == 2

        except:
            self._teardown()

    def test_getFromCache(self):
        try:
            cache = {}

            def get_from_cache(args):
                return cache.get(args["id"])

            def update_cache(args):
                cache[args["id"]] = args["data"]

            self._setup({"entrycache_get": [get_from_cache],
                         "entrycache_update": [update_cache]})

            r = req_()
            e = EntryBase(r)
            yield eq_, e.getFromCache(), None
            foo = {"foo": "bar"}
            e.updateCache(foo)
            yield eq_, e.getFromCache(), foo
        except:
            self._teardown()
