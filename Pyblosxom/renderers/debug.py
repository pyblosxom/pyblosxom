from Pyblosxom.renderers.base import RendererBase
from Pyblosxom import tools
import types

class Renderer(RendererBase):
    def render(self, header = 1):
        pyhttp = self._request.getHttp()
        config = self._request.getConfiguration()
        data = self._request.getData()
        printout = self.write

        self.addHeader('Content-type', 'text/plain')
        self.showHeaders()
        printout("Welcome to debug mode!\n")
        printout("You wanted the %(flavour)s flavour if I support flavours\n" % data)

        printout("------------------------------------------------------\n")
        printout("The HTTP Return codes are:\n")
        printout("------------------------------------------------------\n")
        for key in self._header.keys():
            printout("%s -> %s\n" % (key, self._header[key]))

        printout("------------------------------------------------------\n")
        printout("The OS environment contains:\n")
        printout("------------------------------------------------------\n")
        import os
        for key in os.environ.keys():
            printout("%s -> %s\n" % (key, os.environ[key]))

        printout("------------------------------------------------------\n")
        printout("Request.getHttp() dict contains:\n")
        printout("------------------------------------------------------\n")
        for key in pyhttp.keys():
            printout("%s -> %s\n" % (key, pyhttp[key]))

        printout("------------------------------------------------------\n")
        printout("Request.getConfiguration() dict contains:\n")
        printout("------------------------------------------------------\n")
        for key in config.keys():
            printout("%s -> %s\n" % (key, config[key]))

        printout("------------------------------------------------------\n")
        printout("Request.getData() dict contains:\n")
        printout("------------------------------------------------------\n")
        for key in data.keys():
            printout("%s -> %s\n" % (key, data[key]))

        printout("------------------------------------------------------\n")
        printout("Entries to process:\n")
        printout("------------------------------------------------------\n")
        for content in self._content:
            if type(content) != types.StringType:
                printout("%s\n" % content.get('filename', 'No such file\n'))

        printout("------------------------------------------------------\n")
        printout("Entries processed:\n")
        printout("------------------------------------------------------\n")
        for content in self._content:
            if type(content) != types.StringType:
                printout("------------------------------------------------------\n")
                printout("Items for %s:\n" % content.get('filename', 'No such file\n'))
                printout("------------------------------------------------------\n")
                for item in content.keys():
                    printout("%s -> %s\n" % (item, content[item]))

                #printout("%s\n" % content.get('filename', 'No such file\n'))

        printout("------------------------------------------------------\n")
        printout("Cached Titles:\n")
        printout("------------------------------------------------------\n")
        cache = tools.get_cache(self._request)
        for content in self._content:
            if type(content) != types.StringType:
                filename = content['filename']
            
                if cache.has_key(filename):
                    printout("%s\n" % cache[filename]['title'])
                cache.close()

        printout("------------------------------------------------------\n")
        printout("Cached Entry Bodies:\n")
        printout("------------------------------------------------------\n")
        for content in self._content:
            if type(content) != types.StringType:
                filename = content['filename']
                if cache.has_key(filename):
                    printout("%s\n" % cache[filename]['title'])
                    printout("==================================================\n")
                    printout("%s\n" % cache[filename]['body'])
                else:
                    printout("Contents of %s is not cached\n" % filename)
                cache.close()
                printout("------------------------------------------------------\n")
