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
    """
    def __init__(self, config):
        self._config = config   # Dict containing config on where to store
                                # cache Value of config is derived from
                                # py['cacheConfig']. Document your driver on
                                # what should be set here
    
    
    def load(self, entryid):
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
        """
        return 0

    
    def saveEntry(self, entrydata):
        """
        Store entrydata in cache
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


class BlosxomCache(BlosxomCacheBase):
    """
    A Null cache
    """
    pass
