#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003-2006 Wari Wahab
# Copyright (c) 2003-2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#######################################################################
"""
Holds a series of utility functions for cataloguing, retrieving, and
manipulating callback functions and chains.  Refer to the documentation
for which callbacks are available and their behavior.
"""

import os
import glob
import sys
import os.path
import traceback

# this holds the list of plugins that have been loaded.  if you're running
# PyBlosxom as a long-running process, this only gets cleared when the
# process is restarted.
plugins = []

# this holds a list of callbacks (any function that begins with cp_) and the
# list of function instances that support that callback.
# if you're running PyBlosxom as a long-running process, this only
# gets cleared when the process is restarted.
callbacks = {}

# this holds a list of (plugin name, exception) tuples for plugins that
# didn't import.
bad_plugins = []

def catalogue_plugin(plugin_module):
    """
    Goes through the plugin's contents and catalogues all the functions
    that start with cb_.  Functions that start with cb_ are callbacks.

    :param plugin_module: the module to catalogue
    """
    listing = dir(plugin_module)

    listing = [item for item in listing if item.startswith("cb_")]

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

    NOTE: If PyBlosxom is part of a long-running process, you must
    restart PyBlosxom in order to pick up any changes to your plugins.

    :param plugin_dirs: the list of directories to add to the sys.path
                        because that's where our plugins are located.

    :param plugin_list: the list of plugins to load, or if None, we'll
                        load all the plugins we find in those dirs.
    """
    if plugins or bad_plugins:
        return

    # we clear out the callbacks dict so we can rebuild them
    callbacks.clear()

    # handle plugin_dirs here
    for mem in plugin_dirs:
        if os.path.isdir(mem):
            sys.path.append(mem)
        else:
            raise Exception("Plugin directory '%s' does not exist.  " \
                            "Please check your config file." % mem)

    plugin_list = get_plugin_list(plugin_list, plugin_dirs)

    for mem in plugin_list:
        try:
            _module = __import__(mem)
        except Exception, e:
            bad_plugins.append((mem, e, "".join(traceback.format_exc())))
            continue

        for comp in mem.split(".")[1:]:
            _module = getattr(_module, comp)
        catalogue_plugin(_module)
        plugins.append(_module)

def get_plugin_by_name(name):
    """
    This retrieves a plugin instance (it's a Python module instance)
    by name.

    :param name: the name of the plugin to retrieve (ex: "xmlrpc")

    :returns: the Python module instance for the plugin or None
    """
    if plugins:
        for mem in plugins:
            if mem.__name__ == name:
                return mem
    return None

def get_module_name(filename):
    """
    Takes a filename and returns the module name from the filename.

    Example: passing in "/blah/blah/blah/module.ext" returns "module"

    :param filename: the filename in question (with a full path)

    :returns: the filename without path or extension
    """
    return os.path.splitext(os.path.split(filename)[1])[0]

def get_plugin_list(plugin_list, plugin_dirs):
    """
    This handles the situation where the user has provided a series of
    plugin dirs, but has not specified which plugins they want to load
    from those dirs.  In this case, we load all possible plugins except
    the ones whose names being with _ .

    :param plugin_list: List of plugins to load

    :param plugin_dirs: A list of directories where plugins can be loaded from

    :return: list of python module names of the plugins to load
    """
    if plugin_list == None:
        plugin_list = []
        for mem in plugin_dirs:
            file_list = glob.glob(os.path.join(mem, "*.py"))

            file_list = [get_module_name(filename) for filename in file_list]

            # remove plugins that start with a _
            file_list = [plugin for plugin in file_list \
                         if not plugin.startswith('_')]
            plugin_list += file_list

        plugin_list.sort()

    return plugin_list
