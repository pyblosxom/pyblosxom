# vim: shiftwidth=4 tabstop=4 expandtab
import os, glob, sys

plugins = []

# this holds a list of callbacks (any function that begins with cp_) and the
# list of function instances that support that callback.
callbacks = {}

# XMLRPC methods
methods = {}

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
    Imports and initializes plugins from the directories in the list
    specified by "plugins_dir".  If no such list exists, then we don't
    load any plugins.

    If the user specifies a "load_plugins" list of plugins to load, then
    we explicitly load those plugins in the order they're listed.  If the
    load_plugins key does not exist, then we load all the plugins in the
    plugins directory using an alphanumeric sorting order.
    """
    if callbacks != {}:
        return

    # handle plugin_dirs here
    plugin_dirs = configdict.get("plugin_dirs", [])
    for mem in plugin_dirs:
        # FIXME - do we want to check to see if the dir exists first
        # or just not worry about it?
        sys.path.append(mem)

    plugin_list = configdict.get("load_plugins", None)

    plugin_list = get_plugin_list(plugin_list, plugin_dirs)

    for mem in plugin_list:
        _module = __import__(mem)
        for comp in mem.split(".")[1:]:
            _module = getattr(_module, comp)

        catalogue_plugin(_module)

        plugins.append(_module)

def initialize_xmlrpc_plugins(configdict):
    """
    Imports and initializes plugins from a specified directory so they can
    register with the xmlrpc method callbacks.

    Plugins must have the C{register_xmlrpc_methods} in the plugin module. It
    must return a dict containing the XMLRPC method name as the key, and a
    function reference as its value. For example::

        def helloWorld(request, name):
            return "Hello %s" % name

        def test(request):
            return "Test Passed"

        def register_xmlrpc_methods():
            return {'system.testing': test,
                    'system.helloWorld': helloWorld}
    """
    if callbacks != {}:
        return

    # handle plugin_dirs here
    plugin_dirs = configdict.get("xmlrpc_plugin_dirs", [])
    for mem in plugin_dirs:
        # FIXME - do we want to check to see if the dir exists first
        # or just not worry about it?
        sys.path.append(mem)

    plugin_list = configdict.get("load_xmlrpc_plugins", None)

    plugin_list = get_plugin_list(plugin_list, plugin_dirs)

    for mem in plugin_list:
        _module = __import__(mem)
        for comp in mem.split(".")[1:]:
            _module = getattr(_module, comp)

        # if the module has a register_xmlrpc_methods function, we call it with
        # our py dict so it can bind itself to variable names of its own accord
        if _module.__dict__.has_key("register_xmlrpc_methods"):
            api = _module.register_xmlrpc_methods()

        methods.update(api)

def get_plugin_list(plugin_list, plugin_dirs):    
    """
    Grabs a list of plugins in a list of plugin dirs, and returns the who
    possible importable list of plugins. If load_plugins is None, then we grab
    all the plugins in the directory and sort them alphanumerically

    @param plugin_list: List of plugins to load
    @type plugin_list: list or None
    @param plugin_dirs: A list of directories where plugins can be loaded from
    @type plugin_dirs: list
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
