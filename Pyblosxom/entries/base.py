#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003, 2004, 2005, 2006 Wari Wahab
# 
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#
# $Id$
#######################################################################
"""
This module contains the base class for all the Entry classes.  The
EntryBase class is essentially the API for entries in PyBlosxom.  Reading
through the comments for this class will walk you through building your
own EntryBase derivatives.

This module also holds a generic generate_entry function which will generate
a BaseEntry with data that you provide for it.
"""

__revision__ = "$Revision$"

import time, locale
from Pyblosxom import tools

BIGNUM = 2000000000
CONTENT_KEY = "body"
DOESNOTEXIST = "THISKEYDOESNOTEXIST"
DOESNOTEXIST2 = "THISKEYDOESNOTEXIST2"

class EntryBase:
    """
    EntryBase is the base class for all the Entry classes.  Each 
    instance of an Entry class represents a single entry in the weblog, 
    whether it came from a file, or a database, or even somewhere off 
    the InterWeeb.
    """
    def __init__(self, request):
        self._data = None
        self._metadata = dict(tools.STANDARD_FILTERS)
        self._id = ""
        self._mtime = BIGNUM
        self._request = request

    def __repr__(self):
        """
        Returns a friendly debuggable representation of self. Useful to know on
        what entry pyblosxom fails on you (though unlikely)

        returns: Identifiable representation of object
        rtype: string
        """
        return "<Entry instance: %s>\n" % self.getId()

    def getId(self):
        """
        This should return an id that's unique enough for caching 
        purposes.

        Override this.

        @returns: string id
        @rtype: string
        """
        return self._id

    def getData(self):
        """
        Returns the data string.  This method should be overridden to
        provide from pulling the data from other places.

        Override this.

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

        Override this.

        @param data: the data
        @type  data: string
        """
        self._data = data

    def getMetadata(self, key, default=None):
        """
        Returns a given piece of metadata.

        Override this.

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

        Override this.

        @param key: the key string
        @type  key: string

        @param value: the value string
        @type  value: string (or an object with a __str__ method)
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

        Override this.

        @returns: list of metadata keys
        @rtype: list of strings
        """
        return self._metadata.keys()

    def getFromCache(self, request, entryid):
        """Retrieves information from the cache that pertains to this
        specific entryid.

        This is a helper method--call this to get data from the 
        entry-level cache.  Do not override it.

        This turns around and calls the entrycache_get callback 
        to handle retrieving the data from the cache.

        @param request: the PyBlosxom Request
        @type request: the PyBlosxom Request

        @param entryid: a unique key for the information you're retrieving
        @type  entryid: string

        @returns: cached dict with the values or None if there's nothing 
            cached for that entryid
        @rtype: dict or None
        """
        argdict = { "request": request, "id": entryid }
        cachedentry = tools.run_callback("entrycache_get",
                                         argdict, 
                                         mappingfunc = lambda x, y: x,
                                         donefunc = lambda x: x != None,
                                         defaultfunc = lambda x: None)
        return cachedentry

    def updateCache(self, request, entryid, data):
        """Updates entry data in the entry-level cache.

        This is a helper method--call this to put data into the
        entry-level cache.  Do not override it.

        This turns around and calls the entrycache_update callback to 
        handle updating the entry data in the entry-level cache.

        Note: If the data dict is empty or None, remove the entry from
        the cache.

        @param request: the PyBlosxom Request
        @type request: the PyBlosxom Request

        @param entryid: a unique key for the information you're storing
        @type  entryid: string

        @param data: a dict of entry data--if empty or None, remove the
            entry from the cache
        @type  data: dict
        """
        argdict = { "request": request, "id": entryid, "data": data }
        cachedentry = tools.run_callback("entrycache_update",
                                         argdict, 
                                         mappingfunc = lambda x, y: x,
                                         donefunc = lambda x: 0,
                                         defaultfunc = lambda x: x)


    # everything below this point are convenience functions that
    # work use the above methods.

    def setTime(self, timetuple):
        """
        This takes in a given time tuple and sets all the magic metadata
        variables we have according to the items in the time tuple.

        @param timetuple: the timetuple to use to set the data with--this
            is the same thing as the mtime/atime portions of an os.stat.
        @type  timetuple: tuple of ints
        """
        self['timetuple'] = timetuple
        self._mtime = time.mktime(timetuple)
        gmtimetuple = time.gmtime(self._mtime)
        self['mtime'] = self._mtime
        self['ti'] = time.strftime('%H:%M', timetuple)
        self['mo'] = time.strftime('%b', timetuple)
        self['mo_num'] = time.strftime('%m', timetuple)
        self['da'] = time.strftime('%d', timetuple)
        self['dw'] = time.strftime('%A', timetuple)
        self['yr'] = time.strftime('%Y', timetuple)
        self['fulltime'] = time.strftime('%Y%m%d%H%M%S', timetuple)
        self['date'] = time.strftime('%a, %d %b %Y', timetuple)

        # Temporarily disable the set locale, so RFC-compliant dates are
        # really RFC-compliant
        loc = locale.getlocale(locale.LC_ALL)
        locale.setlocale(locale.LC_ALL, 'C')

        # YYYY-MM-DDThh:mm:ssZ
        self['w3cdate'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', gmtimetuple)
        self['rfc822date'] = time.strftime('%a, %d %b %Y %H:%M GMT', \
                                           gmtimetuple)
        
        # set the locale back
        locale.setlocale(locale.LC_ALL, loc)

    def __getitem__(self, key):
        """
        If the item is CONTENT_KEY then we return the result from 
        self.getData().

        This calls getData() and getMetadata()--there's no reason to 
        override this; override getData and getMetadata instead.

        @param key: the key being sought
        @type  key: varies

        @returns: the value of self._metadata.get(key, default) or 
            self.getData()
        @rtype: varies
        """
        if key == CONTENT_KEY:
            return self.getData()

        return self.getMetadata(key)

    def get(self, key, default=None):
        """
        Retrieves an item from the internal dict based on the key
        given.

        All this does is turn aroun and call __getitem__.

        There's no reason to override this--override getData and
        getMetadata instead.

        @param key: the key being sought
        @type  key: varies

        @param default: the default to return if the key does not
            exist
        @type  default: varies

        @returns: the value of self._metadata.get(key, default) or 
            self.getData() (through __getitem__)
        @rtype: varies
        """
        try:
            return self.__getitem__(key)
        except:
            return default

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

    def __delitem__(self, key):
        """
        Deletes metadata[key].

        If key is CONTENT_KEY, raises ValueError.

        @param key: the given key name
        @type key: varies
        """
        if key == CONTENT_KEY:
            raise ValueError()
        else:
            del self._metadata[key]

    def update(self, newdict):
        """
        Updates the contents in this entry with the contents in the
        dict.  It does so by calling setData and setMetadata.

        @param newdict: the dict we're updating this one with
        @type newdict: dict
        """
        for mem in newdict:
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

        value = self.getMetadata(key, DOESNOTEXIST)
        if value == DOESNOTEXIST:
            value = self.getMetadata(key, DOESNOTEXIST2)
            if value == DOESNOTEXIST2:
                return 0

        return 1

    def __contains__(self, key):
        """
        Returns whether a given key is in the metadata dict. Implements the
        membership test operators 'in' and 'not in'.
        """
        return self.has_key(key)

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


def generate_entry(request, properties, data, mtime):
    """
    Takes a properties dict and a data string and generates a generic
    entry using the data you provided.

    @param request: the Request object
    @type  request: Request

    @param properties: the dict of properties for the entry
    @type  properties: dict

    @param data: the data content for the entry
    @type  data: string

    @param mtime: the mtime tuple (as given by time.localtime()).  
        if you pass in None, then we'll use localtime.
    @type  mtime: tuple of ints
    """
    entry = EntryBase(request)

    entry.update(properties)
    entry.setData(data)
    if mtime:
        entry.setTime(mtime)
    else:
        entry.setTime(time.localtime())
    return entry

# vim: tabstop=4 shiftwidth=4
