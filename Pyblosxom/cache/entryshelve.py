#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
This cache driver creates shelved data as cache in a dbm file.

To use this driver, add the following configuration options in your config.py

py['cacheDriver'] = 'entryshelve'
py['cacheConfig'] = '/path/to/a/cache/dbm/file'

If successful, you will see the cache file. Be sure that you have write access
to the cache file.
"""

from Pyblosxom.cache.base import BlosxomCacheBase
import shelve
import os


class BlosxomCache(BlosxomCacheBase):
    """
    This stores entries in shelves in a .dbm file.
    """
    def __init__(self, req, config):
        """
        Initializes BlosxomCacheBase.__init__ and also opens the
        shelf file.
        """
        BlosxomCacheBase.__init__(self, req, config)
        self._db = shelve.open(self._config)

    def load(self, entryid):
        """
        Loads a specific entryid.
        """
        BlosxomCacheBase.load(self, entryid)

    def getEntry(self):
        """
        Get an entry from the shelf.
        """
        data = self._db.get(self._entryid, {})
        return data.get('entrydata', {})

    def isCached(self):
        """
        Returns true if the entry is cached and the cached version is
        not stale.  Returns false otherwise.
        """
        data = self._db.get(self._entryid, {'mtime':0})
        if os.path.isfile(self._entryid):
            return data['mtime'] == os.stat(self._entryid)[8]
        else:
            return None

    def saveEntry(self, entrydata):
        """
        Save data in the pickled file.
        """
        payload = {}
        payload['mtime'] = os.stat(self._entryid)[8]
        payload['entrydata'] = entrydata

        self._db[self._entryid] = payload

    def rmEntry(self):
        """
        Removes an entry from the shelf.
        """
        if self._entryid in self._db:
            del self._db[self._entryid]

    def keys(self):
        """
        Returns a list of entries that are cached in the shelf.

        @returns: list of entry paths
        @rtype: list of strings
        """
        ret = []
        for key in list(self._db.keys()):
            self.load(key)
            if self.isCached():
                ret.append(key)
            else:
                # Remove this key, why is it there in the first place?
                del self._db[self._entryid]
        return ret

    def close(self):
        """
        Closes the db file.
        """
        self._db.close()
        self._db = None
