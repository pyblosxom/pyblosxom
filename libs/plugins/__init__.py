# vim: shiftwidth=4 tabstop=4 expandtab
import os, glob

plugins = []

def initialize_plugins(configdict):
    """
    Imports and initializes plugins from this directory so they can register
    with the api callbacks.

    If the user specifies a "load_plugins" list of plugins to load, then
    we explicitly load those plugins in the order they're listed.  If the
    load_plugins key does not exist, then we load all the plugins in the
    plugins directory using an alphanumeric sorting order.
    """
    plugin_list = configdict.get("load_plugins", None)

    # if there's no load_plugins key, then we grab all the plugins
    # in the directory and sort them alphanumerically
    if plugin_list == None:
        index = __file__.rfind(os.sep)
        if index == -1:
            path = "." + os.sep
        else:
            path = __file__[:index]

        plugin_list = glob.glob(os.path.join(path, "*.py"))
        
        plugin_list = map(lambda p: p[p.rfind(os.sep)+1:p.rfind(".")], plugin_list)

        # remove plugins that start with a _
        plugin_list = filter(lambda p: not p.startswith('_'), plugin_list)

        plugin_list.sort()

    for mem in plugin_list:

        name = "libs.plugins." + mem
        _module = __import__(name)
        for comp in name.split(".")[1:]:
            _module = getattr(_module, comp)

        if _module.__dict__.has_key("initialize"):
            _module.initialize()

        plugins.append(_module)
