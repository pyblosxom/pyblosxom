# vim: tabstop=4 shiftwidth=4 expandtab
"""
A basic driver, used by default in pyblosxom, does not do anything at all
"""
class BlosxomCacheBase:
    """
    Base Class for Caching stories in pyblosxom.

    A cache is a disposable piece of data that gets updated when an entry is in a
    fresh state.

    Drivers are to subclass this object, overriding methods defined in this class.
    If there is an error in creating cache data, be as quite as possible, document
    how a user could check whether his cache works.

    Driver should expect empty caches and should attempt to create them from
    scratch.

    @cvar _config: String containing config on where to store the cache. The Value
        of config is derived from C{py['cacheConfig']} in L{config}.
    @type _config: string
    """
    def __init__(self, config):
        """
        Constructor - setup and load up the cache

        @param config: String containing config on where to store the cache
        @type config: string
        """
        self._config = config


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
        utilities
        """
        pass


    def close(self):
        """
        Close your cache if necessary.
        """
        pass


    def __getitem__(self, key):
        """
        Convenience function to make this class look like a dict
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
        self.load(key)
        self.rmEntry()


    def has_key(self, key):
        self.load(key)
        return self.isCached()


    def keys(self):
        """
        List out a list of keys for the cache, to be overridden by a subclass
        if a full dict interface is required.
        """
        return []


    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


class BlosxomCache(BlosxomCacheBase):
    """
    A Null cache
    """
    pass
