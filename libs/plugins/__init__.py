# vim: shiftwidth=4 tabstop=4 expandtab
import os, glob

plugins = []

def initialize_plugins(configdict):
    """
    Imports and initializes plugins from this directory so they can register
    with the api callbacks.  The import list is based on the "load_plugins"
    entry in the config dict.
    """
    plugin_list = configdict.get("load_plugins", ())

    for mem in plugin_list:

        name = "libs.plugins." + mem
        _module = __import__(name)
        for comp in name.split(".")[1:]:
            _module = getattr(_module, comp)

        if _module.__dict__.has_key("initialize"):
            _module.initialize()

        plugins.append(_module)
