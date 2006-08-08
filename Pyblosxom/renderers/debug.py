#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003, 2004, 2005, 2006 Wari Wahab
# 
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#
# $Id$
#######################################################################
"""
This is the debug renderer.  This is very useful for debugging plugins
and templates.
"""

__revision__ = "$Id$"

from Pyblosxom.renderers.base import RendererBase
from Pyblosxom import tools

def escv(s):
    """
    Takes in a value.  If it's not a string, we repr it and turn it into
    a string.  Then we escape it so it can be printed in HTML safely.

    @param s: any value
    @type  s: varies

    @returns: a safe-to-print-in-html string representation of the value
    @rtype: string
    """
    if not s:
        return ""

    if not isinstance(s, str):
        s = repr(s)

    return s.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")

def print_map(printfunc, keymap):
    """
    Takes a map of keys to values and applies the function f to a pretty
    printed version of each key/value pair.

    @param printfunc: function for printing
    @type  printfunc: function

    @param keymap: a mapping of key/value pairs
    @type  keymap: map
    """
    keys = keymap.keys()
    keys.sort()
    for key in keys:
        printfunc("<font color=\"#0000ff\">%s</font> -&gt; %s\n" % \
                  (escv(key), escv(keymap[key])))

class Renderer(RendererBase):
    """
    This is the debug renderer.  This is very useful for debugging plugins
    and templates.
    """
    def render(self, header=1):
        """
        Renders a PyBlosxom request after we've gone through all the 
        motions of converting data and getting entries to render.

        @param header: either prints (1) or does not print (0) the http
                       headers.
        @type  header: boolean
        """
        pyhttp = self._request.getHttp()
        config = self._request.getConfiguration()
        data = self._request.getData()
        printout = self.write

        hbar = "------------------------------------------------------\n"


        if header:
            self.addHeader('Content-type', 'text/html')
            self.showHeaders()

        printout("<html>")
        printout("<body>")
        printout("<pre>")
        printout("Welcome to debug mode!\n")
        printout("You requested the %(flavour)s flavour.\n" % data)

        printout(hbar)
        printout("The HTTP Return codes are:\n")
        printout(hbar)
        print_map(printout, self._header)

        printout(hbar)
        printout("The OS environment contains:\n")
        printout(hbar)
        import os
        print_map(printout, os.environ)

        printout(hbar)
        printout("Request.getHttp() dict contains:\n")
        printout(hbar)
        print_map(printout, pyhttp)

        printout(hbar)
        printout("Request.getConfiguration() dict contains:\n")
        printout(hbar)
        print_map(printout, config)

        printout(hbar)
        printout("Request.getData() dict contains:\n")
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
        if not config.has_key("cacheDriver"):
            printout("No cache driver configured.")
        else:
            printout("Cached Titles:\n")
            printout(hbar)
            cache = tools.get_cache(self._request)
            for content in self._content:
                if not isinstance(content, str):
                    filename = content['filename']
            
                    if cache.has_key(filename):
                        printout("%s\n" % escv(cache[filename]['title']))
                    cache.close()

            printout(hbar)
            printout("Cached Entry Bodies:\n")
            printout(hbar)
            for content in self._content:
                if not isinstance(content, str):
                    filename = content['filename']
                    if cache.has_key(filename):
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
