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

def cb_prepare(args):
    request = args["request"]
    form = request.getHttp()['form']
    config = request.getConfiguration()
    data = request.getData()

    entry_list = data['entry_list']
        
    for i in range(len(entry_list)):
        entry = entry_list[i]
        t = entry['timetuple']
        # adjust for daylight savings time
        t = t[0],t[1],t[2],t[3]+time.localtime()[-1],t[4],t[5],t[6],t[7],t[8]
        entry['w3cdate'] = xml.utils.iso8601.ctime(time.mktime(t))
