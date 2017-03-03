#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
The is the base renderer module.  If you were to dislike the blosxom
renderer and wanted to build a renderer that used a different
templating system, you would extend the RendererBase class and
implement the functionality required by the other rendering system.

For examples, look at the BlosxomRenderer and the Renderer in the
debug module.
"""

import sys
import time

from Pyblosxom import tools


class RendererBase:
    """
    Pyblosxom core handles the Input and Process of the system and
    passes the result of the process to the Renderers for output. All
    renderers are child classes of RendererBase. RenderBase will
    contain the public interfaces for all Renderer object.
    """
    def __init__(self, request, stdoutput=sys.stdout):
        """
        Constructor: Initializes the Renderer

        :param request: The ``Pyblosxom.pyblosxom.Request`` object
        :param stdoutput: File like object to print to.
        """
        self._request = request

        # this is a list of tuples of the form (key, value)
        self._header = []

        self._out = stdoutput
        self._content = None
        self._content_mtime = None
        self._needs_content_type = 1
        self.rendered = None

    def write(self, data):
        """
        Convenience method for programs to use instead of accessing
        self._out.write()

        Other classes can override this if there is a unique way to
        write out data, for example, a two stream output, e.g. one
        output stream and one output log stream.

        Another use for this could be a plugin that writes out binary
        files, but because renderers and other frameworks may probably
        not want you to write to ``stdout`` directly, this method
        assists you nicely. For example::

            def cb_start(args):
                req = args['request']
                renderer = req['renderer']

                if reqIsGif and gifFileExists(theGifFile):
                    # Read the file
                    data = open(theGifFile).read()

                    # Modify header
                    renderer.addHeader('Content-type', 'image/gif')
                    renderer.addHeader('Content-Length', len(data))
                    renderer.showHeaders()

                    # Write to output
                    renderer.write(data)

                    # Tell pyblosxom not to render anymore as data is
                    # processed already
                    renderer.rendered = 1

        This simple piece of pseudo-code explains what you could do
        with this method, though I highly don't recommend this, unless
        pyblosxom is running continuously.

        :param data: Piece of string you want printed
        """

        self._out.write(data)

    def add_header(self, *args):
        """
        Populates the HTTP header with lines of text

        :param args: Paired list of headers

        :raises ValueError: This happens when the parameters are not
                            correct
        """
        args = list(args)
        if len(args) % 2 != 0:
            raise ValueError('Headers recieved are not in the correct form')

        while args:
            key = args.pop(0).strip()
            if key.find(' ') != -1 or key.find(':') != -1:
                raise ValueError('There should be no spaces in header keys')
            value = args.pop(0).strip()
            self._header.append( (key, value) )

    addHeader = tools.deprecated_function(add_header)

    def set_content(self, content):
        """
        Sets the content.  The content can be any of the following:

        * dict
        * list of entries

        :param content: the content to be displayed
        """
        self._content = content
        if isinstance(self._content, dict):
            mtime = self._content.get("mtime", time.time())
        elif isinstance(self._content, list):
            mtime = self._content[0].get("mtime", time.time())
        else:
            mtime = time.time()
        self._content_mtime = mtime

    setContent = tools.deprecated_function(set_content)

    def get_content(self):
        """
        Return the content field

        This is exposed for blosxom callbacks.

        :returns: content
        """
        return self._content

    getContent = tools.deprecated_function(get_content)

    def needs_content_type(self, flag):
        """
        Use the renderer to determine 'Content-Type: x/x' default is
        to use the renderer for Content-Type, set flag to None to
        indicate no Content-Type generation.

        :param flag: True of false value
        """
        self._needs_content_type = flag

    needsContentType = tools.deprecated_function(needs_content_type)

    def show_headers(self):
        """
        Updated the headers of the
        ``Response<Pyblosxom.pyblosxom.Response>`` instance.

        This is here for backwards compatibility.
        """
        response = self._request.getResponse()
        for k, v in self._header:
            response.addHeader(k, v)

    showHeaders = tools.deprecated_function(show_headers)

    def render(self, header=True):
        """
        Do final rendering.

        :param header: whether (True) or not (False) to show the
                       headers
        """
        if header:
            if self._header:
                self.show_headers()
            else:
                self.add_header('Content-Type', 'text/plain')
                self.show_headers()

        if self._content:
            self.write(self._content)
        self.rendered = 1


class Renderer(RendererBase):
    """
    This is a null renderer.
    """
    pass
