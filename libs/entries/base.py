# vim: tabstop=4 shiftwidth=4
"""
This module contains the base class for all the Entry classes.
"""
import time

class EntryBase:
    """
    EntryBase is the base class for all the Entry classes.
    Each instance of an Entry class represents a single entry
    in the weblog, whether it came from a file, or a database,
    or even somewhere off the InterWeeb.
    """

    CONTENT_KEY = "content"

    def __init__(self):
        self._data = None
        self._metadata = {}

    def getData(self):
        return self._data

    def setData(self, data):
        self._data = data

    def setTime(self, timeTuple):
        self['timetuple'] = timeTuple
        self['ti'] = time.strftime('%H:%M',timeTuple)
        self['mo'] = time.strftime('%b',timeTuple)
        self['mo_num'] = time.strftime('%m',timeTuple)
        self['da'] = time.strftime('%d',timeTuple)
        self['yr'] = time.strftime('%Y',timeTuple)
        self['fulltime'] = time.strftime('%Y%m%d%H%M%S',timeTuple)
        self['w3cdate'] = time.strftime('%Y-%m-%dT%H:%M:%S%Z',timeTuple) # YYYY-MM-DDThh:mm:ssTZD
        self['date'] = time.strftime('%a, %d %b %Y',timeTuple)

    # Conform to a dict-like interface, too.
    def __getitem__(self, key, default=None):
        if key == EntryBase.CONTENT_KEY:
            return self.getData()
        return self._metadata.get(key, default)

    def __setitem__(self, key, value):
        if key == EntryBase.CONTENT_KEY:
            self.setData( value )
        else:
            self._metadata[key] = value

    def __delitem__(self, key):
        del self._metadata[key]

    def has_key(self, key):
        if key == EntryBase.CONTENT_KEY:
            return true
        return self._metadata.has_key(key)

    def keys(self):
        return self._metadata.keys() + [EntryBase.CONTENT_KEY,]
