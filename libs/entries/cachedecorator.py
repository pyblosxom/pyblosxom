"""
This module acts as a decorator for EntryBase derivatives giving them
a caching mechanism.
"""
import base
from libs import tools

class CacheDecorator(base.EntryBase):
    """
    This class is a decorator for Entry objects to give them a 
    caching mechanism.

    To use this, wrap your Entry object in the CacheDecorator::

        from libs.entries.cachedecorator import CacheDecorator
        from libs.entries.fileentry import FileEntry
        myentry = CacheDecorator(FileEntry(config, filename, root))

    """
    def __init__(self, entryob):
        base.EntryBase.__init__(self)
        self._child = entryob
        self._triedcache = 0

    def retrieveChildFromCache(self):
        """
        Retrieves the child from the cache if we have one.  We return
        the cached item.
        """
        mycache = tools.get_cache()

        id = self._child.getId()

        if mycache.has_key(id):
            # we have the item in cache, so we retrieve it from
            # cache and populate our child's data with it
            entrydict = mycache[id]
            self._child.setCacheableData(entrydict)
            self._child["cached"] = "(yes) " + repr(entrydict.keys())

        else:
            # first we build the dict we're going to cache
            entrydict = self._child.getCacheableData()

            # if we have something to cache, we toss it in
            if entrydict:
                mycache[id] = entrydict
                self._child["cached"] = "(no) " + repr(entrydict.keys())
            else:
                self._child["cached"] = "(no) (no data)"

        self._triedcache = 1

    def __repr__(self):
        return "CD: %d" % self._triedcache

    def getId(self):
        return self._child.getId()

    def getMetadata(self, key, default):
        """
        First we check to see if we've uncached our child yet.  If we
        haven't, then we uncache our child first.
        """
        if self._triedcache == 0:
            self.retrieveChildFromCache()

        return self._child.getMetadata(key, default)

    def getData(self):
        """
        First we check the caching mechanism to see if our entry is cached.
        If it's not, we ask our encapsulated child to get the data and 
        give it to us.
        """
        if self._triedcache == 0:
            self.retrieveChildFromCache()

        return self._child.getData()

    def setData(self, data):
        self._child.setData(data)

    def setMetadata(self, key, value):
        self._child.setMetadata(key, value)

    def getMetadataKeys(self):
        return self._child.getMetadataKeys()
