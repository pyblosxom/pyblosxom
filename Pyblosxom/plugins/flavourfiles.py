#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2010, 2011 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

This plugin allows flavour templates to use file urls that will
resolve to files in the flavour directory.  Those files will then get
served by PyBlosxom.

This solves the problem that flavour packs are currently difficult to
package, install, and maintain because static files (images, css, js,
...) have to get put somewhere else and served by the web server and
this is difficult to walk a user through.

It handles urls that start with ``flavourfiles/``, then the flavour
name, then the path to the file.

For example::

    http://example.com/blog/flavourfiles/html/style.css


.. Note::

   This plugin is very beta!  It's missing important functionality,
   probably has bugs, and hasn't been well tested!


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.flavourfiles`` to the ``load_plugins`` list
   of your ``config.py`` file.

2. In templates you want to use flavourfiles, use urls like this::

       $(base_url)/flavourfiles/$(flavour)/path-to-file

   For example::

       <img src="$(base_url)/flavourfiles/$(flavour)/header_image.jpg">

The ``$(base_url)`` will get filled in with the correct url root.

The ``$(flavour)`` will get filled in with the name of the url.  This
allows users to change the flavour name without having to update all
the templates.

"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2011-10-22"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "Serves static files related to flavours (css, js, ...)"
__license__ = "MIT License"
__registrytags__ = "1.5, core, experimental"

import os
import mimetypes
import sys

from Pyblosxom.renderers import base

TRIGGER = "/flavourfiles/"


class FileRenderer(base.RendererBase):
    def set_filepath(self, filepath):
        self.filepath = filepath

    def render(self, header=True):
        if not os.path.exists(self.filepath):
            self.render_404()
            self.rendered = 1
            return

        # FIXME - handle e-tag/etc conditional stuff here

        try:
            fp = open(self.filepath, "r")
        except OSError:
            # FIXME - this could be a variety of issues, but is
            # probably a permission denied error.  should catch the
            # error message and send it to the 403 page.
            self.render_403()
            self.rendered = 1
            return

        # mimetype
        mimetype = mimetypes.guess_type(self.filepath)
        if mimetype:
            mimetype = mimetype[0]
        if mimetype is None:
            mimetype = "application/octet-stream"
        self.add_header('Content-type', mimetype)

        # content length
        length = os.stat(self.filepath)[6]
        self.add_header('Content-Length', str(length))

        if header:
            self.show_headers()

        self.write(fp.read())
        fp.close()
        self.rendered = 1

    def render_403(self):
        resp = self._request.getResponse()
        resp.set_status("403 Forbidden")

    def render_404(self):
        resp = self._request.getResponse()
        resp.set_status("404 Not Found")


def cb_handle(args):
    """This is the flavour file handler.

    This handles serving static files related to flavours.  It handles
    paths like /flavourfiles/<flavour>/<path-to-file>.

    It calls the prepare callback to do any additional preparation
    before rendering the entries.

    Then it tells the renderer to render the entries.

    :param request: the request object.
    """
    request = args["request"]

    path_info = request.get_http()["PATH_INFO"]
    print path_info, TRIGGER
    if not path_info.startswith(TRIGGER):
        return

    config = request.get_configuration()
    data = request.get_data()

    # get the renderer object
    rend = FileRenderer(request, config.get("stdoutput", sys.stdout))

    data['renderer'] = rend

    filepath = path_info.replace(TRIGGER, "")
    while filepath.startswith(("/", os.sep)):
        filepath = filepath[1:]

    if not filepath:
        rend.render_404()
        return

    filepath = filepath.split("/")
    flavour = filepath[0]
    filepath = "/".join(filepath[1:])

    root = config.get("flavourdir", config["datadir"])
    root = os.path.join(root, flavour + ".flav")
    filepath = os.path.join(root, filepath)

    filepath = os.path.normpath(filepath)
    if not filepath.startswith(root) or not os.path.exists(filepath):
        rend.render_404()
        return

    rend.set_filepath(filepath)
    rend.render()
    return 1
