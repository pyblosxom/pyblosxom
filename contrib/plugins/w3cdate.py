"""
Add a 'w3cdate' key to every entry -- this contains the date in ISO8601 format

WARNING: you must have PyXML installed as part of your python installation 
in order for this plugin to work

Place this plugin early in your load_plugins list, so that the w3cdate will
be available to subsequent plugins
"""
__author__ = "Ted Leung <twl@sauria.com>"
__version__ = "$Id:"
__copyright__ = "Copyright (c) 2003 Ted Leung"
__license__ = "Python"

import xml.utils.iso8601
import time
from Pyblosxom import tools

def cb_story(args):
    request = tools.get_registry()["request"]
    data = request.getData()

    entry_list = data['entry_list']
        
    for i in range(len(entry_list)):
        entry = entry_list[i]
        t = entry['timetuple']
        # adjust for daylight savings time
        tzoffset = 0
        if time.timezone != 0:
            tzoffset = time.altzone
        entry['w3cdate'] = xml.utils.iso8601.tostring(time.mktime(t),tzoffset)
