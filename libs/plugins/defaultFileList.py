
"""
Get a list containing the file names returned by a normal bloxsom style treewalk

"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id$"

from libs import api, tools

def defaultFileListHandler(py):
    return (py['bl_type'] == 'dir' and 
            tools.Walk(py['root_datadir'], 
                       int(py['depth'])) or 
            [py['root_datadir']])

def initialize():
    api.fileListHandler.register(defaultFileListHandler, api.LAST)
