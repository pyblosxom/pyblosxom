#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2004, 2005 Wari Wahab
# Copyright (c) 2010, 2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

This plugin can help save bandwidth for low bandwidth quota sites.

This is done by output-ing cache friendly HTTP header tags like Last-Modified
and ETag. These values are calculated from the first entry returned by
``entry_list``.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. In your ``config.py`` file, add ``Pyblosxom.plugins.conditionalhttp`` to
   the ``load_plugins`` variable.
"""

__author__ = "Wari Wahab"
__email__ = "pyblosxom at wari dot per dot sg"
__version__ = "2011-10-22"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Allows browser-side caching with if-not-modified-since."
__category__ = "headers"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


import time
import os
import pickle
import calendar

from Pyblosxom import tools


def verify_installation(request):
    # This should just work--no configuration needed.
    return True


def cb_prepare(args):
    request = args["request"]

    data = request.get_data()
    config = request.get_configuration()
    http = request.get_http()
    entry_list = data["entry_list"]
    renderer = data["renderer"]

    if entry_list and 'mtime' in entry_list[0]:
        # FIXME - this should be generalized to a callback for updated
        # things.
        mtime = entry_list[0]['mtime']
        latest_cmtime = - 1
        if 'comment_dir' in config:
            latest_filename = os.path.join(config['comment_dir'], 'LATEST.cmt')

            if os.path.exists(latest_filename):
                latest = open(latest_filename)
                latest_cmtime = pickle.load(latest)
                latest.close()

        if latest_cmtime > mtime:
            mtime = latest_cmtime

        # Get our first file timestamp for ETag and Last Modified
        # Last-Modified: Wed, 20 Nov 2002 10:08:12 GMT
        # ETag: "2bdc4-7b5-3ddb5f0c"
        last_modified = time.strftime(
            '%a, %d %b %Y %H:%M:%S GMT', time.gmtime(mtime))
        modified_since = http.get('HTTP_IF_MODIFIED_SINCE', '')

        if ((http.get('HTTP_IF_NONE_MATCH', '') == '"%s"' % mtime) or
             (http.get('HTTP_IF_NONE_MATCH', '') == '%s' % mtime) or
             (modified_since and calendar.timegm(time.strptime(modified_since,'%a, %d %b %Y %H:%M:%S GMT' )) >= int(mtime))):

            renderer.add_header('Status', '304 Not Modified')
            renderer.add_header('ETag', '"%s"' % mtime)
            renderer.add_header('Last-Modified', '%s' % last_modified)

            # whack the content here so that we don't then go render it
            renderer.set_content(None)

            renderer.render()

            # Log request as "We have it!"
            tools.run_callback("logrequest",
                               {'filename': config.get('logfile', ''),
                                'return_code': '304',
                                'request': request})

            return

        renderer.add_header('ETag', '"%s"' % mtime)
        renderer.add_header('Last-Modified', '%s' % last_modified)
