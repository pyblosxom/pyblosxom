# vim: tabstop=4 shiftwidth=4 expandtab
"""
This cache driver creates pickled data as cache in a directory.

To use this driver, add the following configuration options in your config.py

py['cacheDriver'] = 'entrypickle'
py['cacheConfig'] = '/path/to/a/cache/directory'

If successful, you will see the cache directory filled up with files that ends
with .entryplugin extention in the drectory.
"""
from libs import tools
from libs.cache.base import blosxomCacheBase
import cPickle as pickle
import os
from os import makedirs
from os.path import normpath,dirname,exists,abspath

class blosxomCache(blosxomCacheBase):
    def load(self, config, entryID):
        blosxomCacheBase.load(self, config, entryID)
        self._cacheFile = os.path.join(config, entryID.replace('/', '_')) + '.entryplugin'


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
            os.stat(self._cacheFile)[8] >= os.stat(self._entryID)[8]


    def saveEntry(self, entryData):
        """
        Save data in the pickled file
        """
        try:
            self.__makepath(self._cacheFile)
            fp = file(self._cacheFile, "w+b")
            pickle.dump(entryData, fp, 1)
        except IOError:
            pass


    def rmEntry(self):
        if os.path.isfile(self._cacheFile):
            os.remove(self._cacheFile)


    def __makepath(self, path):
        dpath = normpath(dirname(path))
        if not exists(dpath): makedirs(dpath)
        return normpath(abspath(path))
