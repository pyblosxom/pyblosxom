# vim: tabstop=4 shiftwidth=4 expandtab
"""
This cache driver creates shelved data as cache in a dbm file.

To use this driver, add the following configuration options in your config.py

py['cacheDriver'] = 'entryshelve'
py['cacheConfig'] = '/path/to/a/cache/dbm/file'

If successful, you will see the cache file. Be sure that you have write access
to the cache file.
"""
from Pyblosxom import tools
from Pyblosxom.cache.base import BlosxomCacheBase
import shelve
import os

class BlosxomCache(BlosxomCacheBase):
    def __init__(self, req, config):
        BlosxomCacheBase.__init__(self, req, config)
        self._db = shelve.open(self._config)

    def load(self, entryid):
        BlosxomCacheBase.load(self, entryid)

    def getEntry(self):
        """
        Get data from shelve
        """
        data = self._db.get(self._entryid, {})
        return data.get('entrydata', {})
        

    def isCached(self):
        data = self._db.get(self._entryid, {'mtime':0})
        if os.path.isfile(self._entryid):
            return data['mtime'] == os.stat(self._entryid)[8]
        else:
            return None


    def saveEntry(self, entrydata):
        """
        Save data in the pickled file
        """
        payload = {}
        payload['mtime'] = os.stat(self._entryid)[8]
        payload['entrydata'] = entrydata
        
        self._db[self._entryid] = payload


    def rmEntry(self):
        if self._db.has_key(self._entryid):
            del self._db[self._entryid]

    def keys(self):
        ret = []
        for key in self._db.keys():
            self.load(key)
            if self.isCached():
                ret.append(key)
            else:
                # Remove this key, why is it there in the first place?
                del self._db[self._entryid]
        return ret
    

    def close(self):
        self._db.close()
        self._db = None
