# vim: tabstop=4 shiftwidth=4 expandtab
"""
This cache driver creates shelved data as cache in a dbm file.

To use this driver, add the following configuration options in your config.py

py['cacheDriver'] = 'entryshelve'
py['cacheConfig'] = '/path/to/a/cache/dbm/file'

If successful, you will see the cache file. Be sure that you have write access
to the cache file.
"""
from libs import tools
from libs.cache.base import blosxomCacheBase
import shelve
import os

class blosxomCache(blosxomCacheBase):
    def __init__(self, config):
        blosxomCacheBase.__init__(self, config)
        self._db = None

    def load(self, entryID):
        blosxomCacheBase.load(self, entryID)
        if self._db is None:
            self._db = shelve.open(self._config)

    def getEntry(self):
        """
        Get data from shelve
        """
        data = self._db.get(self._entryID, {})
        return data.get('entryData', {})
        

    def isCached(self):
        data = self._db.get(self._entryID, {'mtime':0})
        return data['mtime'] == os.stat(self._entryID)[8]


    def saveEntry(self, entryData):
        """
        Save data in the pickled file
        """
        payload = {}
        payload['mtime'] = os.stat(self._entryID)[8]
        payload['entryData'] = entryData
        
        self._db[self._entryID] = payload


    def rmEntry(self):
        if self._db.has_key(self._entryID):
            del self._db[self._entryID]

    def close(self):
        self._db.close()
        self._db = None
