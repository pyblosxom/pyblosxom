#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
This is the debug renderer.  This is very useful for debugging plugins
and templates.
"""

from Pyblosxom.renderers.base import RendererBase
from Pyblosxom import tools, plugin_utils


def escv(s):
    """
    Takes in a value.  If it's not a string, we repr it and turn it into
    a string.  Then we escape it so it can be printed in HTML safely.

    :param s: any value

    :returns: a safe-to-print-in-html string representation of the value
    """
    if not s:
        return ""

    if not isinstance(s, str):
        s = repr(s)

    return tools.escape_text(s)


def print_map(printfunc, keymap):
    """
    Takes a map of keys to values and applies the function f to a pretty
    printed version of each key/value pair.

    :param printfunc: function for printing

    :param keymap: a mapping of key/value pairs
    """
    keys = list(keymap.keys())
    keys.sort()
    for key in keys:
        printfunc("<font color=\"#0000ff\">%s</font> -&gt; %s\n" % \
                  (escv(key), escv(keymap[key])))


class Renderer(RendererBase):
    """
    This is the debug renderer.  This is very useful for debugging
    plugins and templates.
    """
    def render(self, header=True):
        """
        Renders a Pyblosxom request after we've gone through all the
        motions of converting data and getting entries to render.

        :param header: either prints (True) or does not print (True)
                       the http headers.
        """
        pyhttp = self._request.get_http()
        config = self._request.get_configuration()
        data = self._request.get_data()
        printout = self.write

        hbar = "------------------------------------------------------\n"


        if header:
            self.add_header('Content-type', 'text/html')
            self.show_headers()

        printout("<html>")
        printout("<body>")
        printout("<pre>")
        printout("Welcome to debug mode!\n")
        printout("You requested the %(flavour)s flavour.\n" % data)

        printout(hbar)
        printout("HTTP return headers:\n")
        printout(hbar)
        for k, v in self._header:
            printout("<font color=\"#0000ff\">%s</font> -&gt; %s\n" % \
                     (escv(k), escv(v)))

        printout(hbar)
        printout("The OS environment contains:\n")
        printout(hbar)
        import os
        print_map(printout, os.environ)

        printout(hbar)
        printout("Plugins:\n")
        printout(hbar)
        printout("Plugins that loaded:\n")
        if plugin_utils.plugins:
            for plugin in plugin_utils.plugins:
                printout(" * " + escv(plugin) + "\n")
        else:
            printout("None\n")

        printout("\n")

        printout("Plugins that didn't load:\n")
        if plugin_utils.bad_plugins:
            for plugin, exc in plugin_utils.bad_plugins:
                exc = "    " + "\n    ".join(exc.splitlines()) + "\n"
                printout(" * " + escv(plugin) + "\n")
                printout(escv(exc))
        else:
            printout("None\n")

        printout(hbar)
        printout("Request.get_http() dict contains:\n")
        printout(hbar)
        print_map(printout, pyhttp)

        printout(hbar)
        printout("Request.get_configuration() dict contains:\n")
        printout(hbar)
        print_map(printout, config)

        printout(hbar)
        printout("Request.get_data() dict contains:\n")
        printout(hbar)
        print_map(printout, data)

        printout(hbar)
        printout("Entries to process:\n")
        printout(hbar)
        for content in self._content:
            if not isinstance(content, str):
                printout("%s\n" %
                         escv(content.get('filename', 'No such file\n')))

        printout(hbar)
        printout("Entries processed:\n")
        printout(hbar)
        for content in self._content:
            if not isinstance(content, str):
                printout(hbar)
                emsg = escv(content.get('filename', 'No such file\n'))
                printout("Items for %s:\n" % emsg)
                printout(hbar)
                print_map(printout, content)

        printout(hbar)
        if "cacheDriver" not in config:
            printout("No cache driver configured.")
        else:
            printout("Cached Titles:\n")
            printout(hbar)
            cache = tools.get_cache(self._request)
            for content in self._content:
                if not isinstance(content, str):
                    filename = content['filename']

                    if filename in cache:
                        printout("%s\n" % escv(cache[filename]['title']))
                    cache.close()

            printout(hbar)
            printout("Cached Entry Bodies:\n")
            printout(hbar)
            for content in self._content:
                if not isinstance(content, str):
                    filename = content['filename']
                    if filename in cache:
                        printout("%s\n" % escv(cache[filename]['title']))
                        printout(hbar.replace("-", "="))
                        printout("%s\n" % escv(cache[filename]['body']))
                    else:
                        printout("Contents of %s is not cached\n" % \
                                 escv(filename))
                    cache.close()
                    printout(hbar)

        printout("</body>")
        printout("</html>")
