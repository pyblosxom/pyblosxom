from libs.renderers.base import RendererBase
from libs import tools

class Renderer(RendererBase):
    def render(self, header = 1):
        pyhttp = self._request.getHttp()
        config = self._request.getConfiguration()
        data = self._request.getData()

        print "Content-Type: text/plain"
        print
        print "Welcome to debug mode!"
        print "You wanted the %(flavour)s flavour if I support flavours" % data

        print "------------------------------------------------------"
        print "The OS environment contains:"
        print "------------------------------------------------------"
        import os
        for key in os.environ.keys():
            print "%s -> %s" % (key, os.environ[key])

        print "------------------------------------------------------"
        print "Request.getHttp() dict contains:"
        print "------------------------------------------------------"
        for key in pyhttp.keys():
            print "%s -> %s" % (key, pyhttp[key])

        print "------------------------------------------------------"
        print "Request.getConfiguration() dict contains:"
        print "------------------------------------------------------"
        for key in config.keys():
            print "%s -> %s" % (key, config[key])

        print "------------------------------------------------------"
        print "Request.getData() dict contains:"
        print "------------------------------------------------------"
        for key in data.keys():
            print "%s -> %s" % (key, data[key])

        print "------------------------------------------------------"
        print "Entries to process:"
        print "------------------------------------------------------"
        for content in self._content:
            print "%s" % content['filename']

        print "------------------------------------------------------"
        print "Cached Titles:"
        print "------------------------------------------------------"
        cache = tools.get_registry()['cache']
        for content in self._content:
            cache.load(content['filename'])
            if cache.isCached():
                print "%s" % cache.getEntry()['title']
            cache.close()

        print "------------------------------------------------------"
        print "Cached Entry Bodies:"
        print "------------------------------------------------------"
        for content in self._content:
            cache.load(content['filename'])
            if cache.isCached():
                print "%s" % cache.getEntry()['title']
                print "=================================================="
                print "%s" % cache.getEntry()['body']
            cache.close()
            print "------------------------------------------------------"
