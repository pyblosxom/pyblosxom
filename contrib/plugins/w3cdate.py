"""
Add a 'w3cdate' key to every entry -- this contains the date in ISO8601 format

WARNING: you must have PyXML installed as part of your python installation 
in order for this plugin to work

Place this plugin early in your load_plugins list, so that the w3cdate will
be available to subsequent plugins
"""

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
        entry['w3cdate'] = xml.utils.iso8601.ctime(time.mktime(entry['timetuple']))
