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
This module contains FileEntry class which is used to retrieve entries 
from a file system.  Since pulling data from the file system and parsing 
it is expensive (especially when you have 100s of entries) we delay
fetching data until it's demanded.

The FileEntry calls the entries.base.EntryBase.getFromCache and
entries.base.EntryBase.updateCache to handle entry-level caching.
"""

__revision__ = "$Revision$"

import time
import os
import re
from Pyblosxom import tools
from Pyblosxom.entries import base

class FileEntry(base.EntryBase):
    """
    This class gets it's data and metadata from the file specified
    by the filename argument.
    """
    def __init__(self, request, filename, root, datadir=""):
        """
        @param request: the Request object
        @type  request: Request

        @param filename: the complete filename for the file in question
            including path
        @type  filename: string

        @param root: FIXME - i have no clue what this is
        @type  root: string

        @param datadir: the datadir
        @type  datadir: string
        """
        base.EntryBase.__init__(self, request)
        self._config = request.getConfiguration()
        self._filename = filename.replace(os.sep, '/')
        self._root = root.replace(os.sep, '/')

        self._datadir = datadir or self._config["datadir"]
        if self._datadir.endswith(os.sep):
            self._datadir = self._datadir[:-1]

        self._mtimetuple = tools.filestat(self._request, self._filename)
        self._mtime = time.mktime(self._mtimetuple)

        self._populated_data = 0

    def __repr__(self):
        return "<fileentry f'%s' r'%s'>" % (self._filename, self._root)

    def getId(self):
        return self._filename

    def __populatedata(self):
        """
        Fills the metadata dict with metadata about the given file.  This
        metadata consists of things we pick up from an os.stat call as
        well as knowledge of the filename and the root directory.
        We then parse the file and fill in the rest of the information
        that we know.
        """
        file_basename = os.path.basename(self._filename)

        path = self._filename.replace(self._root, '')
        path = path.replace(os.path.basename(self._filename), '')
        path = path[:-1]

        absolute_path = self._filename.replace(self._datadir, '')
        absolute_path = self._filename.replace(self._datadir, '', 1)
        absolute_path = absolute_path.replace(file_basename, '')
        absolute_path = absolute_path[1:][:-1]

        if absolute_path and absolute_path[-1] == "/":
            absolute_path = absolute_path[0:-1]

        filenamenoext = os.path.splitext(file_basename)[0]
        if absolute_path == '':
            file_path = filenamenoext
        else:
            file_path = '/'.join((absolute_path, filenamenoext))

        tb_id = '%s/%s' % (absolute_path, filenamenoext)
        tb_id = re.sub(r'[^A-Za-z0-9]', '_', tb_id)

        self['path'] = path
        self['tb_id'] = tb_id
        self['absolute_path'] = absolute_path
        self['file_path'] = file_path
        self['fn'] = filenamenoext
        self['filename'] = self._filename

        self.setTime(self._mtimetuple)

        data = self._request.getData()

        entrydict = self.getFromCache()
        if not entrydict:
            fileext = os.path.splitext(self._filename)
            if fileext:
                fileext = fileext[1][1:]

            eparser = data['extensions'][fileext]
            entrydict = eparser(self._filename, self._request)

        self.update(entrydict)
        self.updateCache(entrydict)

        body = entrydict['body']
        del entrydict['body']

        # call the postformat callbacks
        body = tools.run_callback('postformat',
                                  {'request': self._request, 'body': body, 'metadata': entrydict },
                                  mappingfunc=tools.pass_updated("body"),
                                  defaultfunc=tools.default_returnitem("body"),
                                  donefunc=tools.done_never)
        self.update( { "body": body } )

        self._populated_data = 1

    def lazily_populate(func):
        def lazy_decorator(self, *args, **kwargs):
            if self._populated_data == 0:
                self.__populatedata()
            return func(self, *args, **kwargs)
        return lazy_decorator

    @lazily_populate
    def getData(self):
        """
        Returns the data for this file entry.  The data is the parsed
        (via the entryparser) content of the entry.  We do this on-demand
        by checking to see if we've gotten it and if we haven't then
        we get it at that point.

        @returns: the content for this entry
        @rtype: string
        """
        return self._data.read()

    @lazily_populate
    def getMetadata(self, key, default=None):
        """
        This overrides the L{base.EntryBase} getMetadata method.

        Note: We populate our metadata lazily--only when it's requested.
        This delays parsing of the file as long as we can.

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
