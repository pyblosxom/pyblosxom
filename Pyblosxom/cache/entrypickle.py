#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
This cache driver creates pickled data as cache in a directory.

To use this driver, add the following configuration options in your config.py

py['cacheDriver'] = 'entrypickle'
py['cacheConfig'] = '/path/to/a/cache/directory'

If successful, you will see the cache directory filled up with files that ends
with .entryplugin extention in the drectory.
"""

from Pyblosxom import tools
from Pyblosxom.cache.base import BlosxomCacheBase

import pickle as pickle
import os
from os import makedirs
from os.path import normpath, dirname, exists, abspath


class BlosxomCache(BlosxomCacheBase):
    """
    This cache stores each entry as a separate pickle file of the
    entry's contents.
    """
    def __init__(self, req, config):
        """
        Takes in a Pyblosxom request object and a configuration string
        which determines where to store the pickle files.
        """
        BlosxomCacheBase.__init__(self, req, config)
        self._cachefile = ""

    def load(self, entryid):
        """
        Takes an entryid and keeps track of the filename.  We only
        open the file when it's requested with getEntry.
        """
        BlosxomCacheBase.load(self, entryid)
        filename = os.path.join(self._config, entryid.replace('/', '_'))
        self._cachefile = filename + '.entrypickle'

    def getEntry(self):
        """
        Open the pickle file and return the data therein.  If this
        fails, then we return None.
        """
        try:
            filep = open(self._cachefile, 'rb')
            data = pickle.load(filep)
            filep.close()
            return data
        except IOError:
            return None

    def isCached(self):
        """
        Check to see if the file is updated.
        """
        return os.path.isfile(self._cachefile) and \
            os.stat(self._cachefile)[8] >= os.stat(self._entryid)[8]

    def saveEntry(self, entrydata):
        """
        Save the data in the entry object to a pickle file.
        """
        filep = None
        try:
            self.__makepath(self._cachefile)
            filep = open(self._cachefile, "w+b")
            entrydata.update({'realfilename': self._entryid})
            pickle.dump(entrydata, filep, 1)
        except IOError:
            pass

        if filep:
            filep.close()

    def rmEntry(self):
        """
        Removes the pickle file for this entry if it exists.
        """
        if os.path.isfile(self._cachefile):
            os.remove(self._cachefile)

    def keys(self):
        """
        Returns a list of the keys found in this entrypickle instance.
        This corresponds to the list of entries that are cached.

        @returns: list of full paths to entries that are cached
        @rtype: list of strings
        """
        import re
        keys = []
        cached = []
        if os.path.isdir(self._config):
            cached = tools.walk(self._request,
                                self._config,
                                1,
                                re.compile(r'.*\.entrypickle$'))
        for cache in cached:
            cache_data = pickle.load(open(cache))
            key = cache_data.get('realfilename', '')
            if not key and os.path.isfile(cache):
                os.remove(cache)
            self.load(key)
            if not self.isCached():
                self.rmEntry()
            else:
                keys.append(key)
        return keys

    def __makepath(self, path):
        """
        Creates the directory and all parent directories for a
        specified path.

        @param path: the path to create
        @type  path: string

        @returns: the normalized absolute path
        @rtype: string
        """
        dpath = normpath(dirname(path))
        if not exists(dpath):
            makedirs(dpath)
        return normpath(abspath(path))
