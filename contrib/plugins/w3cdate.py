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
    entry = args['entry']
    time_tuple = entry['timetuple']
    tzoffset = time.timezone
		# if is_dst flag set, adjust for daylight savings time
    if time_tuple[8] == 1:
        tzoffset = time.altzone
    entry['w3cdate'] = xml.utils.iso8601.tostring(time.mktime(time_tuple),tzoffset)    
