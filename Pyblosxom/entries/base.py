#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
This module contains the base class for all the Entry classes.  The
EntryBase class is essentially the API for entries in Pyblosxom.  Reading
through the comments for this class will walk you through building your
own EntryBase derivatives.

This module also holds a generic generate_entry function which will generate
a BaseEntry with data that you provide for it.
"""

import time
import locale
from Pyblosxom import tools

BIGNUM = 2000000000
CONTENT_KEY = "body"
DOESNOTEXIST = "THISKEYDOESNOTEXIST"
DOESNOTEXIST2 = "THISKEYDOESNOTEXIST2"


class EntryBase:
    """
    EntryBase is the base class for all the Entry classes.  Each
    instance of an Entry class represents a single entry in the
    weblog, whether it came from a file, or a database, or even
    somewhere off the InterWeeb.

    EntryBase derivatives are dict-like except for one key difference:
    when doing ``__getitem__`` on a nonexistent key, it returns None by
    default.  For example:

    >>> entry = EntryBase('some fake request')
    >>> None == entry["some_nonexistent_key"]
    True
    """

    def __init__(self, request):
        self._data = ""
        self._metadata = dict(tools.STANDARD_FILTERS)
        self._id = ""
        self._mtime = BIGNUM
        self._request = request

    def __repr__(self):
        """
        Returns a friendly debug-able representation of self. Useful
        to know on what entry pyblosxom fails on you (though unlikely)

        :returns: Identifiable representation of object
        """
        return "<Entry instance: %s>\n" % self.getId()

    def get_id(self):
        """
        This should return an id that's unique enough for caching
        purposes.

        Override this.

        :returns: string id
        """
        return self._id

    getId = tools.deprecated_function(get_id)

    def get_data(self):
        """
        Returns the data string.  This method should be overridden to
        provide from pulling the data from other places.

        Override this.

        :returns: the data as a string
        """
        return str(self._data)

    getData = tools.deprecated_function(get_data)

    def set_data(self, data):
        """
        Sets the data content for this entry.  If you are not creating
        the entry, then you have no right to set the data of the
        entry.  Doing so could be hazardous depending on what
        EntryBase subclass you're dealing with.

        Override this.

        :param data: the data
        """
        self._data = data

    setData = tools.deprecated_function(set_data)

    def get_metadata(self, key, default=None):
        """
        Returns a given piece of metadata.

        Override this.

        :param key: the key being sought

        :param default: the default to return if the key does not
                        exist

        :return: either the default (if the key did not exist) or the
                 value of the key in the metadata dict
        """
        return self._metadata.get(key, default)

    getMetadata = tools.deprecated_function(get_metadata)

    def set_metadata(self, key, value):
        """
        Sets a key/value pair in the metadata dict.

        Override this.

        :param key: the key string

        :param value: the value string
        """
        self._metadata[key] = value

    setMetadata = tools.deprecated_function(set_metadata)

    def get_metadata_keys(self):
        """
        Returns the list of keys for which we have values in our
        stored metadata.

        .. Note::

            This list gets modified later downstream.  If you cache
            your list of metadata keys, then this method should return
            a copy of that list and not the list itself lest it get
            adjusted.

        Override this.

        :returns: list of metadata keys
        """
        return list(self._metadata.keys())

    getMetadataKeys = tools.deprecated_function(get_metadata_keys)

    def get_from_cache(self, entryid):
        """
        Retrieves information from the cache that pertains to this
        specific entryid.

        This is a helper method--call this to get data from the cache.
        Do not override it.

        :param entryid: a unique key for the information you're retrieving

        :returns: dict with the values or None if there's nothing for that
                  entryid
        """
        cache = tools.get_cache(self._request)

        # cache.__getitem__ returns None if the id isn't there
        if cache.has_key(entryid):
            return cache[entryid]

        return None

    getFromCache = tools.deprecated_function(get_from_cache)

    def add_to_cache(self, entryid, data):
        """
        Over-writes the cached dict for key entryid with the data
        dict.

        This is a helper method--call this to add data to the cache.
        Do not override it.

        :param entryid: a unique key for the information you're
                        storing

        :param data: the data to store--this should probably be a dict
        """
        mycache = tools.get_cache(self._request)
        if mycache:
            # This could be extended to cover all keys used by
            # set_time(), but this is the key most likely to turn
            # up in metadata. If #date is not blocked from caching
            # here, the templates will use the raw string value
            # from the user metadata, rather than the value
            # derived from mtime.
            if 'date' in data:
                data.pop('date')
            mycache[entryid] = data

    addToCache = tools.deprecated_function(add_to_cache)

    def set_time(self, timetuple):
        """
        This takes in a given time tuple and sets all the magic
        metadata variables we have according to the items in the time
        tuple.

        :param timetuple: the timetuple to use to set the data
                          with--this is the same thing as the
                          mtime/atime portions of an os.stat.  This
                          time is expected to be local time, not UTC.
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

        # YYYY-MM-DDThh:mm:ssZ
        self['w3cdate'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', gmtimetuple)

        # Temporarily disable the set locale, so RFC-compliant date is
        # really RFC-compliant: directives %a and %b are locale
        # dependent.  Technically, we're after english locale, but
        # only 'C' locale is guaranteed to exist.
        #loc = locale.getlocale(locale.LC_ALL)
        locale.setlocale(locale.LC_ALL, 'C')

        self['rfc822date'] = time.strftime('%a, %d %b %Y %H:%M GMT', \
                                           gmtimetuple)

        # set the locale back
        #locale.setlocale(locale.LC_ALL, loc)
        locale.resetlocale()

    setTime = tools.deprecated_function(set_time)

    # everything below this point involves convenience functions
    # that work with the above functions.

    def __getitem__(self, key, default=None):
        """
        Retrieves an item from this dict based on the key given.  If
        the item does not exist, then we return the default.

        If the item is ``CONTENT_KEY``, it calls ``get_data``,
        otherwise it calls ``get_metadata``.  Don't override this.

        .. Warning::

            There's no reason to override this--override ``get_data``
            and ``get_metadata`` instead.

        :param key: the key being sought

        :param default: the default to return if the key does not
                        exist

        :returns: the value of ``get_metadata`` or ``get_data``
        """
        if key == CONTENT_KEY:
            return self.get_data()

        return self.get_metadata(key, default)

    def get(self, key, default=None):
        """
        Retrieves an item from the internal dict based on the key
        given.

        All this does is turn aroun and call ``__getitem__``.

        .. Warning::

            There's no reason to override this--override ``get_data``
            and ``get_metadata`` instead.

        :param key: the key being sought

        :param default: the default to return if the key does not
                        exist

        :returns: the value of ``get_metadata`` or ``get_data``
                  (through ``__getitem__``)
        """
        return self.__getitem__(key, default)

    def __setitem__(self, key, value):
        """
        Sets the metadata[key] to the given value.

        This uses ``set_data`` and ``set_metadata``.  Don't override
        this.

        :param key: the given key name

        :param value: the given value
        """
        if key == CONTENT_KEY:
            self.set_data(value)
        else:
            self.set_metadata(key, value)

    def update(self, newdict):
        """
        Updates the contents in this entry with the contents in the
        dict.  It does so by calling ``set_data`` and
        ``set_metadata``.

        .. Warning::

            There's no reason to override this--override ``set_data``
            and ``set_metadata`` instead.

        :param newdict: the dict we're updating this one with
        """
        for mem in list(newdict.keys()):
            if mem == CONTENT_KEY:
                self.set_data(newdict[mem])
            else:
                self.set_metadata(mem, newdict[mem])

    def has_key(self, key):
        """
        Returns whether a given key is in the metadata dict.  If the
        key is the ``CONTENT_KEY``, then we automatically return true.

        .. Warning::

            There's no reason to override this--override
            ``get_metadata`` instead.

        :param key: the key to check in the metadata dict for

        :returns: whether (True) or not (False) the key exists
        """
        if key == CONTENT_KEY or key == CONTENT_KEY + "_escaped":
            return True

        value = self.get_metadata(key, DOESNOTEXIST)
        if value == DOESNOTEXIST:
            value = self.get_metadata(key, DOESNOTEXIST2)
            if value == DOESNOTEXIST2:
                return False

        return True

    def keys(self):
        """
        Returns a list of the keys that can be accessed through
        ``__getitem__``.

        .. Warning::

            There's no reason to override this--override
            ``get_metadata_keys`` instead.

        :returns: list of key names
        """
        keys = self.get_metadata_keys()
        if CONTENT_KEY not in keys:
            keys.append(CONTENT_KEY)
        return keys


def generate_entry(request, properties, data, mtime=None):
    """
    Takes a properties dict and a data string and generates a generic
    entry using the data you provided.

    :param request: the Request object

    :param properties: the dict of properties for the entry

    :param data: the data content for the entry

    :param mtime: the mtime tuple (as given by ``time.localtime()``).
                  if you pass in None, then we'll use localtime.
    """
    entry = EntryBase(request)

    entry.update(properties)
    entry.set_data(data)
    if mtime:
        entry.set_time(mtime)
    else:
        entry.set_time(time.localtime())
    return entry
