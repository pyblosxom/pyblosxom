# vim: tabstop=4 shiftwidth=4
"""
This module contains the classes necessary to get entries
from a file system.
"""
import time, string, os, re
from libs import tools
from base import EntryBase

class FileEntry(EntryBase):
    """
    This class gets it's data and metadata from a file.
    """
    def __init__(self, config, filename, root ):
        EntryBase.__init__( self )
        self._filename = filename
        self._config = config
        self.getProperties( root )

    def getProperties(self, root):
        """Returns an Entry class of file related contents"""

        mtime = tools.filestat(self._filename)[8]
        timeTuple = time.localtime(mtime)
        path = string.replace(self._filename, root, '')
        path = string.replace(path, os.path.basename(self._filename), '')
        path = path[1:][:-1]
        absolute_path = string.replace(self._filename, self._config['datadir'], '')
        absolute_path = string.replace(absolute_path, os.path.basename(self._filename), '')
        absolute_path = absolute_path[1:][:-1]
        fn = re.sub(r'\.txt$', '', os.path.basename(self._filename))
        if absolute_path == '':
            file_path = fn
        else:
            file_path = absolute_path+'/'+fn
        tb = '-'
        tb_id = '%s/%s' % (absolute_path, fn)
        tb_id = re.sub(r'[^A-Za-z0-9]', '_', tb_id)
        if os.path.isfile('%s/%s.stor' % (self._config.get('tb_data', ''), tb_id)):
            tb = '+'

        self['mtime'] = mtime
        self['path'] = path
        self['tb'] = tb
        self['tb_id'] = tb_id
        self['absolute_path'] = absolute_path
        self['file_path'] = file_path
        self['fn'] = fn
        self['filename'] = self._filename
        self.setTime(timeTuple)
