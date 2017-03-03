#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2003-2005 Ted Leung
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

This plugin allows pyblosxom to process trackback
http://www.sixapart.com/pronet/docs/trackback_spec pings.


Install
=======

Requires the ``comments`` plugin.  Though you don't need to have
comments enabled on your blog in order for trackbacks to work.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.trackback`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Add this to your ``config.py`` file::

       py['trackback_urltrigger'] = "/trackback"

   These web forms are useful for testing.  You can use them to send
   trackback pings with arbitrary content to the URL of your choice:

   * http://kalsey.com/tools/trackback/
   * http://www.reedmaniac.com/scripts/trackback_form.php

3. Now you need to advertise the trackback ping link.  Add this to your
   ``story`` template::

       <a href="$(base_url)/trackback/$(file_path)" title="Trackback">TB</a>

4. You can supply an embedded RDF description of the trackback ping, too.
   Add this to your ``story`` or ``comment-story`` template::

       <!--
       <rdf:RDF
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:trackback="http://madskills.com/public/xml/rss/module/trackback/">
       <rdf:Description
            about="$(base_url)/$(file_path)"
            dc:title="$(title)"
            dc:identifier="$(base_url)/$(file_path)"
            trackback:ping="$(base_url)/trackback/$(file_path)"
       />
       </rdf:RDF>
       -->

"""

__author__ = "Ted Leung"
__email__ = ""
__version__ = ""
__url__ = "http://pyblosxom.github.com/"
__description__ = "Trackback support."
__category__ = "comments"
__license__ = "MIT"
__registrytags__ = "1.4, core"


from Pyblosxom import tools
from Pyblosxom.tools import pwrap


tb_good_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>0</error>
</response>"""


tb_bad_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>1</error>
<message>%s</message>
</response>"""


def verify_installation(request):
    config = request.get_configuration()

    # all config properties are optional
    if not 'trackback_urltrigger' in config:
        pwrap("missing optional property: 'trackback_urltrigger'")

    return True


def cb_handle(args):
    request = args['request']
    pyhttp = request.get_http()
    config = request.get_configuration()

    urltrigger = config.get('trackback_urltrigger', '/trackback')

    logger = tools.get_logger()

    path_info = pyhttp['PATH_INFO']
    if path_info.startswith(urltrigger):
        response = request.get_response()
        response.add_header("Content-type", "text/xml")

        form = request.get_form()

        message = ("A trackback must have at least a URL field (see "
                   "http://www.sixapart.com/pronet/docs/trackback_spec)")

        if "url" in form:
            from .comments import decode_form
            encoding = config.get('blog_encoding', 'iso-8859-1')
            decode_form(form, encoding)
            import time
            cdict = {'title': form.getvalue('title', ''),
                     'author': form.getvalue('blog_name', ''),
                     'pubDate': str(time.time()),
                     'link': form['url'].value,
                     'source': form.getvalue('blog_name', ''),
                     'description': form.getvalue('excerpt', ''),
                     'ipaddress': pyhttp.get('REMOTE_ADDR', ''),
                     'type': 'trackback'
                     }
            argdict = {"request": request, "comment": cdict}
            reject = tools.run_callback("trackback_reject",
                                        argdict,
                                        donefunc=lambda x: x != 0)
            if isinstance(reject, (tuple, list)) and len(reject) == 2:
                reject_code, reject_message = reject
            else:
                reject_code, reject_message = reject, "Trackback rejected."

            if reject_code == 1:
                print(tb_bad_response % reject_message, file=response)
                return 1

            from Pyblosxom.entries.fileentry import FileEntry

            datadir = config['datadir']

            from .comments import writeComment
            try:
                import os
                pi = path_info.replace(urltrigger, '')
                path = os.path.join(datadir, pi[1:])
                data = request.get_data()
                ext = tools.what_ext(list(data['extensions'].keys()), path)
                entry = FileEntry(request, '%s.%s' % (path, ext), datadir)
                data = {}
                data['entry_list'] = [entry]
                # Format Author
                cdict['author'] = (
                    'Trackback from %s' % form.getvalue('blog_name', ''))
                writeComment(request, config, data, cdict, encoding)
                print(tb_good_response, file=response)
            except OSError:
                message = 'URI ' + path_info + " doesn't exist"
                logger.error(message)
                print(tb_bad_response % message, file=response)

        else:
            logger.error(message)
            print(tb_bad_response % message, file=response)

        # no further handling is needed
        return 1
    return 0
