# vim: shiftwidth=4 tabstop=4 expandtab
"""
Holds a series of utility functions for cataloguing, retrieving, and
manipulating callback functions and chains.  Refer to the documentation
for which callbacks are available and what their behavior is.
"""
import os, glob, sys
import os.path

plugins = []

# this holds a list of callbacks (any function that begins with cp_) and the
# list of function instances that support that callback.
callbacks = {}

def catalogue_plugin(plugin_module):
    """
    Goes through the plugin's contents and catalogues all the functions
    that start with cb_.  Functions that start with cb_ are callbacks.

    @param plugin_module: the module to catalogue
    @type  plugin_module: module
    """
    global callbacks
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

    @returns: list of functions registered with the callback (or an
        empty list)
    @rtype: list of functions
    """
    global callbacks
    return callbacks.get(chain, [])

def initialize_plugins(plugin_dirs, plugin_list):
    """
    Imports and initializes plugins from the directories in the list
    specified by "plugins_dir".  If no such list exists, then we don't
    load any plugins.

    If the user specifies a "load_plugins" list of plugins to load, then
    we explicitly load those plugins in the order they're listed.  If the
    load_plugins key does not exist, then we load all the plugins in the
    plugins directory using an alphanumeric sorting order.

    @param plugin_dirs: the list of directories to add to the sys.path
        because that's where our plugins are located.
    @type  plugin_dirs: list of strings

    @param plugin_list: the list of plugins to load, or if None, we'll
        load all the plugins we find in those dirs.
    @type  plugin_list: list of strings or None
    """
    global plugins

    # handle plugin_dirs here
    for mem in plugin_dirs:
        if os.path.isdir(mem):
            sys.path.append(mem)
        else:
            raise Exception("Plugin directory '%s' does not exist.  Please check your config file." % mem)

    plugin_list = get_plugin_list(plugin_list, plugin_dirs)

    for mem in plugin_list:
        _module = __import__(mem)
        for comp in mem.split(".")[1:]:
            _module = getattr(_module, comp)
        catalogue_plugin(_module)
        plugins.append(_module)

def get_plugin_by_name(name):
    """
    This retrieves a plugin instance (it's a Python module instance)
    by name.

    @param name: the name of the plugin to retrieve (ex: "xmlrpc")
    @type  name: string

    @returns: the Python module instance for the plugin or None
    @rtype: Python module
    """
    global plugins
    if plugins:
        for mem in plugins:
            if mem.__name__ == name:
                return mem
    return None

def get_plugin_list(plugin_list, plugin_dirs):    
    """
    This handles the situation where the user has provided a series of
    plugin dirs, but has not specified which plugins they want to load
    from those dirs.  In this case, we load all possible plugins except
    the ones whose names being with _ .  

    @param plugin_list: List of plugins to load
    @type plugin_list: list or None

    @param plugin_dirs: A list of directories where plugins can be loaded from
    @type plugin_dirs: list

    @return: list of python module names of the plugins to load
    @rtype: list of strings
    """
    if plugin_list == None:
        plugin_list = []
        for mem in plugin_dirs:
            file_list = glob.glob(os.path.join(mem, "*.py"))
            # get basename - py extension
            file_list = [p[p.rfind(os.sep)+1:p.rfind(".")] for p in file_list]
            # remove plugins that start with a _
            file_list = [p for p in file_list if not p.startswith('_')]
            plugin_list += file_list

        plugin_list.sort()

    return plugin_list

