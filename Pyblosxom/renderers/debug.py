"""
This is the debug renderer.  This is very useful for debugging plugins
and templates.
"""
from Pyblosxom.renderers.base import RendererBase
from Pyblosxom import tools
import types

def E(s):
    if not s:
        return ""

    if not isinstance(s, str):
        s = repr(s)

    return s.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")

def print_map(f, m):
    keys = m.keys()
    keys.sort()
    for key in keys:
        f("<font color=\"#0000ff\">%s</font> -&gt; %s\n" % (E(key), E(m[key])))

class Renderer(RendererBase):
    def render(self, header = 1):
        pyhttp = self._request.getHttp()
        config = self._request.getConfiguration()
        data = self._request.getData()
        printout = self.write

        self.addHeader('Content-type', 'text/html')
        self.showHeaders()
        printout("<html>")
        printout("<body>")
        printout("<pre>")
        printout("Welcome to debug mode!\n")
        printout("You wanted the %(flavour)s flavour if I support flavours\n" % data)

        printout("------------------------------------------------------\n")
        printout("The HTTP Return codes are:\n")
        printout("------------------------------------------------------\n")
        print_map(printout, self._header)

        printout("------------------------------------------------------\n")
        printout("The OS environment contains:\n")
        printout("------------------------------------------------------\n")
        import os
        print_map(printout, os.environ)

        printout("------------------------------------------------------\n")
        printout("Request.getHttp() dict contains:\n")
        printout("------------------------------------------------------\n")
        print_map(printout, pyhttp)

        printout("------------------------------------------------------\n")
        printout("Request.getConfiguration() dict contains:\n")
        printout("------------------------------------------------------\n")
        print_map(printout, config)

        printout("------------------------------------------------------\n")
        printout("Request.getData() dict contains:\n")
        printout("------------------------------------------------------\n")
        print_map(printout, data)

        printout("------------------------------------------------------\n")
        printout("Entries to process:\n")
        printout("------------------------------------------------------\n")
        for content in self._content:
            if not isinstance(content, str):
                printout("%s\n" % E(content.get('filename', 'No such file\n')))

        printout("------------------------------------------------------\n")
        printout("Entries processed:\n")
        printout("------------------------------------------------------\n")
        for content in self._content:
            if not isinstance(content, str):
                printout("------------------------------------------------------\n")
                printout("Items for %s:\n" % E(content.get('filename', 'No such file\n')))
                printout("------------------------------------------------------\n")
                print_map(printout, content)

        printout("------------------------------------------------------\n")
        printout("Cached Titles:\n")
        printout("------------------------------------------------------\n")
        cache = tools.get_cache(self._request)
        for content in self._content:
            if not isinstance(content, str):
                filename = content['filename']
            
                if cache.has_key(filename):
                    printout("%s\n" % E(cache[filename]['title']))
                cache.close()

        printout("------------------------------------------------------\n")
        printout("Cached Entry Bodies:\n")
        printout("------------------------------------------------------\n")
        for content in self._content:
            if not isinstance(content, str):
                filename = content['filename']
                if cache.has_key(filename):
                    printout("%s\n" % E(cache[filename]['title']))
                    printout("==================================================\n")
                    printout("%s\n" % E(cache[filename]['body']))
                else:
                    printout("Contents of %s is not cached\n" % E(filename))
                cache.close()
                printout("------------------------------------------------------\n")
        printout("</body>")
        printout("</html>")
