# vim: tabstop=4 shiftwidth=4 expandtab
"""
This plugin can help save bandwidth for low bandwidth quota sites (how
unfortunate).

This is done by outputing cache friendly HTTP header tags like Last-Modified
and ETag. These values are calculated from the first entry returned by
entryList.
"""
__author__ = "Wari Wahab pyblosxom@wari.per.sg"
__version__ = "$Id$"

def cb_prepare(args):
    request = args["request"]

    data = request.getData()
    config = request.getConfiguration()
    entryList = data["entry_list"]
    renderer = data["renderer"]

    if entryList and entryList[0].has_key('mtime'):
        mtime = entryList[0]['mtime']
        latest_cmtime = - 1
        for i in entryList:
            if i.has_key('comment_latest_mtime'):
                cmtime = i['comment_latest_mtime'] 
                if cmtime > latest_cmtime:
                    latest_cmtime = cmtime
        if latest_cmtime > mtime:
            mtime = latest_cmtime
        import os, time
        # Get our first file timestamp for ETag and Last Modified
        # Last-Modified: Wed, 20 Nov 2002 10:08:12 GMT
        # ETag: "2bdc4-7b5-3ddb5f0c"
        lastModed = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(mtime))
        if ((os.environ.get('HTTP_IF_NONE_MATCH','') == '"%s"' % mtime) or
            (os.environ.get('HTTP_IF_NONE_MATCH','') == '%s' % mtime) or
            (os.environ.get('HTTP_IF_MODIFIED_SINCE','') == lastModed)):
            renderer.addHeader(['Status: 304 Not Modified',
                    'ETag: "%s"' % mtime,
                    'Last-Modified: %s' % lastModed])
#            renderer.needsContentType(None)
            renderer.render()

        from libs import tools
        # Log request as "We have it!"
        tools.run_callback("logrequest",
                {'filename':config.get('logfile',''),
                'return_code': '304',
                'request': request})
                                                                                                  
        renderer.addHeader(['ETag: "%s"' % mtime,
            'Last-Modified: %s' % lastModed])
