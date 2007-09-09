import _path_pyblosxom

from Pyblosxom import tools
from Pyblosxom import plugin_utils

def rc(chain, args):
    ret = tools.run_callback(chain, args)
    print repr(ret)
    return ret

class Testcallbacks:
    def _setup(self, chain, funcs):
        plugin_utils.callbacks = { chain: funcs }

    def _teardown(self):
        plugin_utils.callbacks = {}

    def test_defaults(self):
        args = { "item1": 1, "item2": 2 }

        def f1(args):
            return args["item1"]
        def f2(args):
            return args["item2"]

        self._setup("test", [f1, f2])

        # pass args to f1, 
        # f1 returns 1, 
        # mappingfunc maps (args, 1) to args,
        # pass args to f2,
        # f2 returns 2
        # run_callback returns the last output item, which is 2.
        assert rc("test", args) == 2

        self._teardown()
