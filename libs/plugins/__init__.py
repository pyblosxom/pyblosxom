# vim: shiftwidth=4 tabstop=4 expandtab
import os, glob

plugins = []

# this holds a list of callbacks (any function that begins with cp_) and the
# list of function instances that support that callback.
callbacks = {}

def catalogue_plugin(plugin_module):
    """
    We go through the plugin's contents and catalogue all the
    functions that start with cb_.  These are callbacks.

    @param plugin_module: the module to catalogue
    @type  plugin_module: module
    """
    listing = dir(plugin_module)

    listing = [m for m in listing if m.startswith("cb_")]

    for mem in listing:
        func = getattr(plugin_module, mem)
        memadj = mem[3:]
        if callable(func):
            callbacks.setdefault(memadj, []).append(func)
            
def get_callback_chain(chain):
    """
    Returns a list of functions registered with the callback.

    @returns: list of functions registered with the callback
    @rtype: list of functions
    """
    return callbacks.get(chain, [])

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
        # get basename - py extension
        plugin_list = [p[p.rfind(os.sep)+1:p.rfind(".")] for p in plugin_list]
        # remove plugins that start with a _
        plugin_list = [p for p in plugin_list if not p.startswith('_')]

        plugin_list.sort()


    for mem in plugin_list:
        name = "libs.plugins." + mem
        _module = __import__(name)
        for comp in name.split(".")[1:]:
            _module = getattr(_module, comp)

        if _module.__dict__.has_key("initialize"):
            _module.initialize()

        catalogue_plugin(_module)

        plugins.append(_module)
