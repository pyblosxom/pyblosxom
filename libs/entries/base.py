# vim: tabstop=4 shiftwidth=4
"""
This module contains the base class for all the Entry classes.
"""
import time

CONTENT_KEY = "body"
DOESNOTEXIST = "THISKEYDOESNOTEXIST"

class EntryBase:
    """
    EntryBase is the base class for all the Entry classes.  Each 
    instance of an Entry class represents a single entry in the weblog, 
    whether it came from a file, or a database, or even somewhere off 
    the InterWeeb.
    """
    def __init__(self):
        self._data = None
        self._metadata = {}

    def getId(self):
        """
        This should return an id that's unique enough for caching 
        purposes.

        Override this.

        @returns: string id
        @rtype: string
        """
        return ""

    def getData(self):
        """
        Returns the data string.  This method should be overridden to
        provide from pulling the data from other places.

        @returns: the data as a string
        @rtype: string
        """
        return str(self._data)

    def setData(self, data):
        """
        Sets the data content for this entry.  If you are not
        creating the entry, then you have no right to set the data
        of the entry.  Doing so could be hazardous depending on what
        EntryBase subclass you're dealing with.

        @param data: the data
        @type  data: string
        """
        self._data = data

    def getMetadata(self, key, default=None):
        """
        Returns a given piece of metadata.

        @param key: the key being sought
        @type  key: varies

        @param default: the default to return if the key does not
            exist
        @type  default: varies

        @return: either the default (if the key did not exist) or the
            value of the key in the metadata dict
        @rtype: varies
        """
        return self._metadata.get(key, default)

    def setMetadata(self, key, value):
        """
        Sets a key/value pair in the metadata dict.
        """
        self._metadata[key] = value

    def getMetadataKeys(self):
        """
        Returns the list of keys for which we have values in our
        stored metadata.

        Note: This list gets modified later downstream.  If you
        cache your list of metadata keys, then this method should
        return a copy of that list and not the list itself
        lest it get adjusted.
        """
        return self._metadata.keys()


    # everything below this point involves convenience functions
    # that work with the above functions.

    def setTime(self, timeTuple):
        """
        This takes in a given time tuple and sets all the magic metadata
        variables we have according to the items in the time tuple.

        @param timeTuple: the timetuple to use to set the data with--this
            is the same thing as the mtime/atime portions of an os.stat.
        @type  timeTuple: tuple of ints
        """
        self['timetuple'] = timeTuple
        self['ti'] = time.strftime('%H:%M',timeTuple)
        self['mo'] = time.strftime('%b',timeTuple)
        self['mo_num'] = time.strftime('%m',timeTuple)
        self['da'] = time.strftime('%d',timeTuple)
        self['yr'] = time.strftime('%Y',timeTuple)
        self['fulltime'] = time.strftime('%Y%m%d%H%M%S',timeTuple)
        # YYYY-MM-DDThh:mm:ssTZD
        self['w3cdate'] = time.strftime('%Y-%m-%dT%H:%M:%S%Z',timeTuple)
        self['date'] = time.strftime('%a, %d %b %Y',timeTuple)

    def __getitem__(self, key, default=None):
        """
        Retrieves an item from this dict based on the key given.  If 
        the item does not exist, then we return the default.  If the 
        item is CONTENT_KEY then we return the result from 
        self.getData().

        This is just a convenience method for getData(...) and 
        getMetadata(...).

        There's no reason to override this--override getData and
        getMetadata instead.

        @returns: the value of self._metadata.get(key, default) or 
            self.getData()
        @rtype: varies
        """
        if key == CONTENT_KEY:
            return self.getData()
        return self.getMetadata(key, default)

    def __setitem__(self, key, value):
        """
        Sets the metadata[key] to the given value.

        This is a convenience method for setData(...) and setMetadata(...).

        There's no reason to override this.  Override setData and
        setMetadata.

        @param key: the given key name
        @type key: varies

        @param value: the given value
        @type value: varies
        """
        if key == CONTENT_KEY:
            self.setData(value)
        else:
            self.setMetadata(key, value)

    def update(self, newdict):
        """
        Updates the contents in this entry with the contents in the
        dict.  It does so by calling setData and setMetadata.

        @param newdict: the dict we're updating this one with
        @type newdict: dict
        """
        for mem in newdict.keys():
           if mem == CONTENT_KEY:
               self.setData(newdict[mem])
           else:
               self.setMetadata(mem, newdict[mem])

    def has_key(self, key):
        """
        Returns whether a given key is in the metadata dict.  If the key
        is the CONTENT_KEY, then we automatically return true.

        @param key: the key to check in the metadata dict for
        @type  key: varies

        @returns: whether (1) or not (0) the key exists
        @rtype: boolean
        """
        if key == CONTENT_KEY:
            return 1

        # we do this cheesy little thing in case the metadata dict
        # has to be populated in order to figure out if it has a given
        # key.
        value = self.getMetadata(key, DOESNOTEXIST)
        if value == DOESNOTEXIST:
            return 0

        return 1

    def keys(self):
        """
        Returns a list of the keys that can be accessed through
        __getitem__.

        @returns: list of key names
        @rtype: list of varies
        """
        keys = self.getMetadataKeys()
        if CONTENT_KEY not in keys:
            keys.append(CONTENT_KEY)
        return keys
