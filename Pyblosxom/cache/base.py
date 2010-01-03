#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003-2006 Wari Wahab
# Copyright (c) 2003-2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################
"""
The cache base class.  Subclasses of this class provide caching for
blog entry data in PyBlosxom.
"""

class BlosxomCacheBase:
    """
    Base Class for Caching stories in pyblosxom.

    A cache is a disposable piece of data that gets updated when an entry
    is in a fresh state.

    Drivers are to subclass this object, overriding methods defined in
    this class.  If there is an error in creating cache data, be as quite
    as possible, document how a user could check whether his cache works.

    Driver should expect empty caches and should attempt to create them from
    scratch.

    @ivar _config: String containing config on where to store the cache.
        The value of config is derived from C{py['cacheConfig']} in config.py.
    @type _config: string
    """
    def __init__(self, req, config):
        """
        Constructor - setup and load up the cache

        @param req: the request object
        @type req: Request

        @param config: String containing config on where to store the cache
        @type config: string
        """
        self._request = req
        self._config = config

        self._entryid = ""
        self._entrydata = {}

    def load(self, entryid):
        """
        Try to load up the cache with entryid (a unique key for the entry)

        @param entryid: The key identifier for your cache
        @type entryid: string
        """
        self._entryid = entryid # The filename of the entry
        self._entrydata = {}    # The data of the entry

    def getEntry(self):
        """
        Gets the data from the cache, returns a dict or an empty dict.
        """
        return self._entrydata

    def isCached(self):
        """
        Returns 0 or 1 based on whether there is cached data, returns 0 is
        cache data is stale

        @returns: 0 or 1 based on cache
        @rtype: boolean
        """
        return 0

    def saveEntry(self, entrydata):
        """
        Store entrydata in cache

        @param entrydata: The payload, usually a dict
        @type entrydata: dict
        """
        pass

    def rmEntry(self):
        """
        Remove cache entry: This is not used by pyblosxom, but used by
        utilities.
        """
        pass

    def close(self):
        """
        Override this to close your cache if necessary.
        """
        pass

    def __getitem__(self, key):
        """
        Convenience function to make this class look like a dict.
        """
        self.load(key)
        if not self.has_key(key):
            raise KeyError
        return self.getEntry()

    def __setitem__(self, key, value):
        """
        Synonymous to L{saveEntry}
        """
        self.load(key)
        self.saveEntry(value)

    def __delitem__(self, key):
        """
        Convenience function to make this look more like a dict.
        """
        self.load(key)
        self.rmEntry()

    def has_key(self, key):
        """
        Convenience function to make this look more like a dict.
        """
        self.load(key)
        return self.isCached()

    def keys(self):
        """
        List out a list of keys for the cache, to be overridden by a subclass
        if a full dict interface is required.
        """
        return []

    def get(self, key, default=None):
        """
        Convenience function to make this look more like a dict.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


class BlosxomCache(BlosxomCacheBase):
    """
    A null cache.
    """
    pass
