# vim: tabstop=4 shiftwidth=4
"""
This module contains the classes necessary to get entries
from a file system.
"""
import time, os, re
from libs import tools
import base

class FileEntry(base.EntryBase):
    """
    This class gets it's data and metadata from a file.
    """
    def __init__(self, config, filename, root):
        base.EntryBase.__init__(self)
        self._config = config
        self._filename = filename
        self._root = root

        self._original_metadata_keys = []
        self._populated_data = 0
        self.__populateBasicMetadata()


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
        Some of our metadata comes from os.stats--and the rest
        comes from running the entry parser on the file.  so
        we try to fulfill as many things from os.stats as we
        can before parsing the file.
        """
        if self._populated_data == 1 or key in self._original_metadata_keys:
            return self._metadata.get(key, default)

        self.__populateData()
        return self._metadata.get(key, default)
        
    def __populateBasicMetadata(self):
        """
        Fills the metadata dict with metadata about the given file.  This
        metadata consists of things we pick up from an os.stat call as
        well as knowledge of the filename and the root directory.
        The rest of the metadata comes from parsing the file itself which
        is done with __populateData.
        """
        # handle file manipulations
        file_basename = os.path.basename(self._filename)

        path = self._filename.replace(self._root, '')
        path = path.replace(os.path.basename(self._filename), '')
        path = path[1:][:-1]

        absolute_path = self._filename.replace(self._config['datadir'], '')
        absolute_path = absolute_path.replace(file_basename, '')
        absolute_path = absolute_path[1:][:-1]

        fn = re.sub(r'\.txt$', '', file_basename)
        if absolute_path == '':
            file_path = fn
        else:
            file_path = absolute_path + '/' + fn

        tb = '-'
        tb_id = '%s/%s' % (absolute_path, fn)
        tb_id = re.sub(r'[^A-Za-z0-9]', '_', tb_id)
        tb_data = self._config.get('tb_data', '')
        if os.path.isfile('%s/%s.stor' % (tb_data, tb_id)):
            tb = '+'

        self['path'] = path
        self['tb'] = tb
        self['tb_id'] = tb_id
        self['absolute_path'] = absolute_path
        self['file_path'] = file_path
        self['fn'] = fn
        self['filename'] = self._filename

        # handle the time portions
        mtime = tools.filestat(self._filename)[8]
        timeTuple = time.localtime(mtime)
        self['mtime'] = mtime
        self.setTime(timeTuple)

        # when someone does a getMetadata and they're looking for
        # a key not in this list, then we'll have to parse the
        # file and complete the list of keys.
        self._original_metadata_keys = self.keys()
        self._original_metadata_keys.remove(base.CONTENT_KEY)

    def __populateData(self):
        """
        Populates the rest of the data for this entry from a given
        file.  This could be just the contents of the file, but the
        file could also contain metadata that overrides the metadata
        we normally pull.
        """
        registry = tools.get_registry()
        request = registry["request"]
        data = request.getData()

        fileExt = re.search(r'\.([\w]+)$', self._filename)
        try:
            eparser = data['extensions'][fileExt.groups()[0]]
            entrydict = eparser.parse(self._filename, request)
            self.update(entrydict)
        except IOError:
            return None

        self._populated_data = 1
