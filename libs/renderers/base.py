# vim: shiftwidth=4 tabstop=4 expandtab

import sys

class RendererBase:
    """
    Basic Renderer:
        - Pyblosxom Core handles the Input and Process of the system and passes
          the result of the process to the Renderers for output. All renderers
          are child classes of RendererBase. RenderBase will contain the public
          interfaces for all Renderer onject.
    """

    def __init__(self, request, out = sys.stdout):
        """
        Constructor: Initializes the Renderer

        @param request: The L{libs.Request.Request} object
        @type request: L{libs.Request.Request} object
        @param out: File like object to print to.
        @type out: file
        """
        self._request = request
        self._header = []
        self._out = out
        self._content = None
        self._needs_content_type = 1
        self.rendered = None


    def addHeader(self, headers):
        """
        Populates the HTTP header with lines of text

        @param headers: List of headers
        @type headers: list
        """
        self._header.extend(headers)


    def setContent(self, content):
        """
        Sets the content

        @param content: What content are we to show?
        @type content: C{list} List of entries to process or C{dict} Simple
            dict containing at least 'title' and 'body'
        """
        self._content = content

    
    def needsContentType(self, flag):
        """
        Use the renderer to determine 'Content-Type: x/x' default is to use the
        renderer for Content-Type, set flag to None to indicate no Content-Type
        generation.

        @param flag: True of false value
        """
        self._needs_content_type = flag


    def showHeaders(self):
        """
        Show HTTP Headers. Override this is your renderer uses headers in a
        different way
        """
        self._out.write('\n'.join(self._header))
        self._out.write('\n\n')


    def render(self, header = 1):
        """
        Do final rendering.

        @param header: Do we want to show headers?
        @type header: boolean
        """
        if header:
            if self._header:
                self.showHeader()
            else:
                self.addHeader('Content-Type: text/plain')
                self.showHeader()

        if self._content:
            self._out.write(self._content)
        self.rendered = 1

class Renderer(RendererBase):
    pass
