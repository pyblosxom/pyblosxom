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

    def __init__(self, request, stdoutput = sys.stdout):
        """
        Constructor: Initializes the Renderer

        @param request: The L{Pyblosxom.pyblosxom.Request} object
        @type request: L{Pyblosxom.pyblosxom.Request} object
        @param stdoutput: File like object to print to.
        @type stdoutput: file
        """
        self._request = request
        self._header = {}
        self._out = stdoutput
        self._content = None
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
        not want you to write to C{stdout} directly, this method assists
        you nicely. For example::

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

        This simple piece of pseudocode explains what you could do with
        this method, though I highly don't recommend this, unless
        pyblosxom is running continuously.

        @param data: Piece of string you want printed
        @type data: string
        """
        self._out.write(data)


    def addHeader(self, *args):
        """
        Populates the HTTP header with lines of text

        @param args: Paired list of headers
        @type args: argument lists
        @raises ValueError: This happens when the parameters are not correct
        """
        args = list(args)
        if not len(args) % 2:
            while args:
                key = args.pop(0).strip()
                if key.find(' ') != -1 or key.find(':') != -1:
                    raise ValueError, 'There should be no spaces in header keys'
                value = args.pop(0).strip()
                self._header.update({key: value})
        else:
            raise ValueError, 'Headers recieved are not in the correct form'


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
        Show HTTP Headers. Override this if your renderer uses headers in a
        different way
        """
        self.write('\n'.join(['%s: %s' % (x, self._header[x]) 
                for x in self._header.keys()]))
        self.write('\n\n')


    def render(self, header = 1):
        """
        Do final rendering.

        @param header: Do we want to show headers?
        @type header: boolean
        """
        if header:
            if self._header:
                self.showHeaders()
            else:
                self.addHeader('Content-Type', 'text/plain')
                self.showHeaders()

        if self._content:
            self.write(self._content)
        self.rendered = 1

class Renderer(RendererBase):
    pass
