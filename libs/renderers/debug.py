from libs.renderers.base import RendererBase
from libs import tools

class Renderer(RendererBase):
    def render(self, header = 1):
        print "Content-Type: text/plain\n"
        print "Welcome to debug mode!"
        print "You wanted the %(flavour)s flavour if I support flavours" % self._py

        print "------------------------------------------------------"
        print "The OS environment contains:"
        print "------------------------------------------------------"
        import os
        for key in os.environ.keys():
            print "%s -> %s" % (key, os.environ[key])
        print "------------------------------------------------------"
        print "Py dict contains:"
        print "------------------------------------------------------"
        for key in self._py.keys():
            print "%s -> %s" % (key, self._py[key])
        print "------------------------------------------------------"
        print "Entries to process:"
        print "------------------------------------------------------"
        for content in self._content:
            print "%s" % content['filename']
        print "------------------------------------------------------"
        print "Cached Titles:"
        print "------------------------------------------------------"
        cache_driver = tools.importName('libs.cache', self._py.get('cacheDriver', 'base'))
        cache = cache_driver.BlosxomCache(self._py.get('cacheConfig', ''))
        for content in self._content:
            cache.load(content['filename'])
            if cache.isCached():
                print "%s" % cache.getEntry()['title']
            cache.close()
        print "------------------------------------------------------"
        print "Cached Entry Bodies:"
        print "------------------------------------------------------"
        cache_driver = tools.importName('libs.cache', self._py.get('cacheDriver', 'base'))
        cache = cache_driver.BlosxomCache(self._py.get('cacheConfig', ''))
        for content in self._content:
            cache.load(content['filename'])
            if cache.isCached():
                print "%s" % cache.getEntry()['title']
		print "=================================================="
                print "%s" % cache.getEntry()['body']
            cache.close()
	    print "------------------------------------------------------"
