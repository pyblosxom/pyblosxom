"""
This is the debug renderer.  This is very useful for debugging plugins
and templates.
"""
from Pyblosxom.renderers.base import RendererBase
from Pyblosxom import tools

def E(s):
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

def print_map(f, m):
    """
    Takes a map of keys to values and applies the function f to a pretty
    printed version of each key/value pair.

    @param f: function for printing
    @type  f: function

    @param m: a mapping of key/value pairs
    @type  m: map
    """
    keys = m.keys()
    keys.sort()
    for key in keys:
        f("<font color=\"#0000ff\">%s</font> -&gt; %s\n" % (E(key), E(m[key])))

class Renderer(RendererBase):
    """
    This is the debug renderer.  This is very useful for debugging plugins
    and templates.
    """
    def render(self, header = 1):
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
