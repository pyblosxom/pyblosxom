# vim: tabstop=4 shiftwidth=4 expandtab
"""
This cache driver creates pickled data as cache in a directory.

To use this driver, add the following configuration options in your config.py

py['cacheDriver'] = 'entrypickle'
py['cacheConfig'] = '/path/to/a/cache/directory'

If successful, you will see the cache directory filled up with files that ends
with .entryplugin extention in the drectory.
"""
from Pyblosxom import tools
from Pyblosxom.cache.base import BlosxomCacheBase
import cPickle as pickle
import os
from os import makedirs
from os.path import normpath,dirname,exists,abspath

class BlosxomCache(BlosxomCacheBase):
    def load(self, entryid):
        BlosxomCacheBase.load(self, entryid)
        self._cacheFile = os.path.join(self._config, entryid.replace('/', '_')) + \
                '.entrypickle'


    def getEntry(self):
        """
        Get data from pickle
        """
        try:
            fp = file(self._cacheFile, 'rb')
            return pickle.load(fp)
        except IOError:
            return None


    def isCached(self):
        """
        Check if file is updated
        """
        return os.path.isfile(self._cacheFile) and \
            os.stat(self._cacheFile)[8] >= os.stat(self._entryid)[8]


    def saveEntry(self, entrydata):
        """
        Save data in the pickled file
        """
        try:
            self.__makepath(self._cacheFile)
            fp = file(self._cacheFile, "w+b")
            entrydata.update({'realfilename': self._entryid})
            pickle.dump(entrydata, fp, 1)
        except IOError:
            pass


    def rmEntry(self):
        if os.path.isfile(self._cacheFile):
            os.remove(self._cacheFile)


    def keys(self):
        import re
        keys = []
        cached = []
        if os.path.isdir(self._config):
            cached = tools.Walk(self._config, 1, re.compile(r'.*\.entrypickle$'))
        for cache in cached:
            cache_data = pickle.load(file(cache))
            key = cache_data.get('realfilename', '')
            if not key and os.path.isfile(cache):
                os.remove(cache)
            self.load(key)
            if not self.isCached():
                self.rmEntry()
            else:
                keys.append(key)
        return keys


    def __makepath(self, path):
        dpath = normpath(dirname(path))
        if not exists(dpath): makedirs(dpath)
        return normpath(abspath(path))
