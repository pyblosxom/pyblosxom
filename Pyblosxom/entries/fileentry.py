# vim: tabstop=4 shiftwidth=4
"""
This module contains FileEntry class which is used to retrieve entries 
from a file system.  Since pulling data from the file system and parsing 
it is expensive (especially when you have 100s of entries) we delay
fetching data until it's demanded.

The FileEntry calls EntryBase methods addToCache and getFromCache
to handle caching.
"""
import time, os, re
from Pyblosxom import tools
import base

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

        @param root: i have no clue what this is
        @type  root: string

        @param datadir: the datadir
        @type  datadir: string
        """
        base.EntryBase.__init__(self, request)
        self._config = request.getConfiguration()
        self._filename = filename
        self._root = root

        self._datadir = datadir or self._config["datadir"]
        if self._datadir.endswith(os.sep):
            self._datadir = self._datadir[:-1]

        self._timetuple = tools.filestat(self._request, self._filename)
        self._mtime = time.mktime(self._timetuple)
        self._fulltime = time.strftime("%Y%m%d%H%M%S", self._timetuple)

        self._populated_data = 0

    def __repr__(self):
        return "<fileentry f'%s' r'%s'>" % (self._filename, self._root)

    def getId(self):
        """
        Returns the id for this content item--in this case, it's the
        filename.
        """
        return self._filename

    def getData(self):
        """
        Returns the data for this file entry.  The data is the parsed
        (via the entryparser) content of the entry.  We do this on-demand
        by checking to see if we've gotten it and if we haven't then
        we get it at that point.

        @returns: the content for this entry
        @rtype: string
        """
        if self._populated_data == 0:
            self.__populateData()
        return self._data

    def getMetadata(self, key, default=None):
        """
        We populate our metadata lazily--only when it's requested.
        This delays parsing of the file as long as we can.
        """
        if self._populated_data == 0:
            self.__populateData()

        return self._metadata.get(key, default)
        
    def __populateData(self):
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
        absolute_path = absolute_path.replace(file_basename, '')
        absolute_path = absolute_path[1:][:-1]

        fn, ext = os.path.splitext(file_basename)
        if absolute_path == '':
            file_path = fn
        else:
            file_path = os.path.join(absolute_path, fn)

        tb_id = '%s/%s' % (absolute_path, fn)
        tb_id = re.sub(r'[^A-Za-z0-9]', '_', tb_id)

        self['path'] = path
        self['tb_id'] = tb_id
        self['absolute_path'] = absolute_path
        self['file_path'] = file_path
        self['fn'] = fn
        self['filename'] = self._filename

        # handle the time portions
        timeTuple = tools.filestat(self._request, self._filename)
        self.setTime(timeTuple)

        data = self._request.getData()

        entrydict = self.getFromCache(self._filename)
        if not entrydict:
            fileExt = os.path.splitext(self._filename)
            if fileExt:
                fileExt = fileExt[1][1:]
            try:
                eparser = data['extensions'][fileExt]
                entrydict = eparser(self._filename, self._request)
                self.addToCache(self._filename, entrydict)
            except IOError:
                return None

        self.update(entrydict)
        self._populated_data = 1
