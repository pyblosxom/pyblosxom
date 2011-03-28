#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003-2005 Ted Leung
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

This plugin allows pyblosxom to process trackback
http://www.sixapart.com/pronet/docs/trackback_spec pings.


Setup
=====

You must have the comments plugin installed as well, although you
don't need to enable comments on your blog in order for trackbacks to
work.

Add this to your ``config.py`` file::

    py['trackback_urltrigger'] = "/trackback"

These web forms are useful for testing.  You can use them to send
trackback pings with arbitrary content to the URL of your choice:

* http://kalsey.com/tools/trackback/
* http://www.reedmaniac.com/scripts/trackback_form.php

For more detailed installation, read the README file that comes with
the comments plugins.
"""

__author__ = "Ted Leung"
__email__ = ""
__version__ = ""
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "Trackback support."
__category__ = "comments"
__license__ = "MIT"


import cgi, os, os.path
from Pyblosxom import tools

tb_good_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>0</error>
</response>"""

tb_bad_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>1</error>
<message>%s</message>
</response>"""

def cb_start(args):
    request = args["request"]
    config = request.getConfiguration()
    logdir = config.get("logdir", "/tmp")
    logfile = os.path.normpath(logdir + os.sep + "trackback.log")

def verify_installation(request):
    config = request.getConfiguration()
    retval = 1

    # all config properties are optional
    if not config.has_key('trackback_urltrigger'):
        print("missing optional property: 'trackback_urltrigger'")

    return retval

def cb_handle(args):
    """

    @param args: a dict of plugin arguments
    @type args: dict
    """
    request = args['request']
    pyhttp = request.getHttp()
    config = request.getConfiguration()

    urltrigger = config.get('trackback_urltrigger','/trackback')

    logger = tools.getLogger()

    path_info = pyhttp['PATH_INFO']
    if path_info.startswith(urltrigger):
        response = request.getResponse()
        response.addHeader("Content-type", "text/xml")

        form = request.getForm()

        message = "A trackback must have at least a URL field (see http://www.sixapart.com/pronet/docs/trackback_spec )"

        if form.has_key("url"):
            from comments import decode_form
            encoding = config.get('blog_encoding', 'iso-8859-1')
            decode_form(form, encoding)
            import time
            cdict = { 'title': form.getvalue('title', ''),
                      'author' : form.getvalue('blog_name', ''),
                      'pubDate' : str(time.time()),
                      'link' : form['url'].value,
                      'source' : form.getvalue('blog_name', ''),
                      'description' : form.getvalue('excerpt', ''),
                      'ipaddress': pyhttp.get('REMOTE_ADDR', ''),
                      'type' : 'trackback'
                      }
            argdict = { "request": request, "comment": cdict }
            reject = tools.run_callback("trackback_reject",
                                        argdict,
                                        donefunc=lambda x:x != 0)
            if ((isinstance(reject, tuple) or isinstance(reject, list))
                and len(reject) == 2):
                reject_code, reject_message = reject
            else:
                reject_code, reject_message = reject, "Trackback rejected."
            if reject_code == 1:
                print >> response, tb_bad_response % reject_message
                return 1

            from Pyblosxom.entries.fileentry import FileEntry
            from Pyblosxom.pyblosxom import Request
            from Pyblosxom.pyblosxom import PyBlosxom

            datadir = config['datadir']

            from comments import writeComment    
            try:
                import os
                pi = path_info.replace(urltrigger,'')
                path = os.path.join(datadir, pi[1:])
                data = request.getData()
                ext = tools.what_ext(data['extensions'].keys(), path)
                entry = FileEntry(request, '%s.%s' % (path, ext), datadir )
                data = {}
                data['entry_list'] = [ entry ]
                # Format Author
                cdict['author'] = 'Trackback from %s' % form.getvalue('blog_name', '')
                writeComment(request, config, data, cdict, encoding)
                print >> response, tb_good_response
            except OSError:
                message = 'URI '+path_info+" doesn't exist"
                logger.error(message)
                print >> response, tb_bad_response % message

        else:
            logger.error(message)
            print >> response, tb_bad_response % message

        # no further handling is needed
        return 1
    else:
        return 0
