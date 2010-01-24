# vim: tabstop=4 shiftwidth=4 expandtab
"""
This plugin can help save bandwidth for low bandwidth quota sites (how
unfortunate).

This is done by outputing cache friendly HTTP header tags like Last-Modified
and ETag. These values are calculated from the first entry returned by
entry_list.


Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright 2004, 2005 Wari Wahab
Copyright 2010 Will Kahn-Greene
"""
__author__ = "Wari Wahab pyblosxom@wari.per.sg"
__version__ = "$Id$"
__url__ = "http://pyblosxom.sourceforge.net/"
__description__ = "Allows for caching if-not-modified-since...."

def cb_prepare(args):
    request = args["request"]

    data = request.get_data()
    config = request.get_configuration()
    http = request.get_http()
    entry_list = data["entry_list"]
    renderer = data["renderer"]

    if entry_list and entry_list[0].has_key('mtime'):
        # FIXME - this should be generalized to a callback for updated
        # things.
        mtime = entry_list[0]['mtime']
        latest_cmtime = - 1
        if config.has_key('comment_dir'):
            import os
            latest_filename = os.path.join(config['comment_dir'], 'LATEST.cmt')

            if os.path.exists(latest_filename):
                latest = open(latest_filename)
                import cPickle
                latest_cmtime = cPickle.load(latest)
                latest.close()

        if latest_cmtime > mtime:
            mtime = latest_cmtime

        import time

        # Get our first file timestamp for ETag and Last Modified
        # Last-Modified: Wed, 20 Nov 2002 10:08:12 GMT
        # ETag: "2bdc4-7b5-3ddb5f0c"
        last_modified = time.strftime('%a, %d %b %Y %H:%M:%S GMT',
                                      time.gmtime(mtime))
        if (((http.get('HTTP_IF_NONE_MATCH','') == '"%s"' % mtime) or
             (http.get('HTTP_IF_NONE_MATCH','') == '%s' % mtime) or
             (http.get('HTTP_IF_MODIFIED_SINCE','') == last_modified))):

            renderer.add_header('Status', '304 Not Modified')
            renderer.add_header('ETag', '"%s"' % mtime)
            renderer.add_header('Last-Modified', '%s' % last_modified)

            # whack the content here so that we don't then go render it
            renderer.set_content(None)

            renderer.render()

            from Pyblosxom import tools

            # Log request as "We have it!"
            tools.run_callback("logrequest",
                               {'filename': config.get('logfile',''),
                                'return_code': '304',
                                'request': request})

            return

        renderer.add_header('ETag', '"%s"' % mtime)
        renderer.add_header('Last-Modified', '%s' % last_modified)
