"""
The rss2renderer is a renderer that will render your blog in RSS2
format.  This allows you to have RSS2 syndication WITHOUT writing
flavour templates for RSS2.

The following are required properties in your config.py file:

   blog_title        - the title of your blog
   blog_author       - your name
   blog_email        - your email address
   blog_description  - the description of your blog
   blog_language     - the language code for your blog
   blog_encoding     - the encoding of your blog (defaults to utf-8)

Optionally, you can specify:

   rss2_extension    - the extension (defaults to "/index.rss2") that
                       causes this renderer to be used

Miscellaneous notes about this plugin:

1. the Content-Type we return is "application/xml" so your links
   should match
2. this doesn't handle comments
3. this plugin requires pyxml be installed

FIXME - probably needs more information in this help portion!


This code is placed in the public domain.  Do with it as you will.


Originally written by Blake Winton.
Overhauled by Will Guaraldi.

Just for clarity sake, Blake wrote the majority of the code, but Will is
going to take responsibility to maintain the code going forward (unless
Blake really wants to--doesn't bother Will either way).

Revisions:
1.9 - (May 2, 2005) Fixed (again) problems with rss2renderer and conditionalhttp.
1.8 - (April 11, 2005) Changed instances of roughingit to the new web-site url.
1.7 - (March 9, 2005) Fixed problems with rss2renderer and conditionalhttp.
1.6 - (January 28, 2005) Fixed num_entries problem with PyBlosxom 1.2 (not yet
                         released).
1.5 - (September 27, 2004) Fixed num_entries issue with PyBlosxom 1.1.
1.4 - (September 15, 2004) Fixed encoding issues (thanks Aslak!)
1.3 - (September 14, 2004) Fixed the content type (thanks Gabor!)
                           Fixed spaces in the links (thanks Brett!)
1.2 - (September 13, 2004) Fixed minor issue causing invalidation (thanks Brett!)
1.1 - (September 12, 2004) Will's overhaul.
1.0 - Blake's original writing.
"""
__author__ = "Blake Winton and Will Guaraldi"
__version__ = "1.9 (May 2, 2005)"
__url__ = "http://pyblosxom.sourceforge.net/"
__description__ = "RSS2 renderer."

from Pyblosxom.renderers.base import RendererBase
from Pyblosxom.tools import Stripper
from xml.dom.minidom import Document
import urlparse

class RSS2Renderer(RendererBase):
    """
    This renderer is to create valid RSS2 documents without the need for a
    pyblosxom template. I mostly expect you to know what you are doing, before
    attempting this
    """
    # How long you want the simple description to be
    desc_length = 20 # 20 words, at the most for me

    # Create the big html? <content:encoded>, yes, then 1, else 0
    create_entry = 1
    entry_type = 'CDATA' # or 'escaped' - choose your poison

    # Namespaces for you to pick and choose
    namespaces = {
        'admin': "http://webns.net/mvcb/",
        'content': "http://purl.org/rss/1.0/modules/content/",
        'creativeCommons': "http://backend.userland.com/creativeCommonsRssModule",
        'dc': "http://purl.org/dc/elements/1.1/",
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'html': "http://www.w3.org/1999/html",
        'slash': "http://purl.org/rss/1.0/modules/slash/",
    }

    def _addText(self, element, text, baseElement):
        e = self._doc.createElement(element)
        e.appendChild(self._doc.createTextNode(text))
        baseElement.appendChild(e)
        return e

    def _addCDATA(self, element, text, baseElement):
        e = self._doc.createElement(element)
        e.appendChild(self._doc.createCDATASection(text))
        baseElement.appendChild(e)
        return e

    def _addElemAttr(self, element, attr, content, baseElement, text = None):
        e = self._doc.createElement(element)
        e.setAttribute(attr, content)
        if text:
            e.appendChild(self._doc.createTextNode(text))
        baseElement.appendChild(e)
        return e

    def _addAttr(self, element, attr, content):
        element.setAttribute(attr, content)

    def _addNameSpaces(self, element, namespace_dict):
        for attr in namespace_dict:
            self._addAttr(element, 'xmlns:' + attr, namespace_dict[attr])

    def _urlEncode(self, txt):
        # I'm doing it here because it's only a partial url-encoding
        txt = txt.replace(" ", "%20")
        return txt

    def _createChannel(self):
        # Start our RSS document here
        self._doc = Document()
        d = self._doc
        rss = d.createElement('rss')
        rss.setAttribute('version', '2.0')
        self._addNameSpaces(rss, self.namespaces)
        d.appendChild(rss)
        self._channel = d.createElement('channel')
        channel = self._channel
        rss.appendChild(channel)

        # Add details about our blog here
        self._addText('title', self._config['blog_title'], channel)
        self._addText('link', self._urlEncode(self._config['base_url']), channel)
        self._addText('description', self._config['blog_description'], channel)
        self._addText('language', self._config['blog_language'], channel)
        self._addText('ttl', '60', channel)
        self._addText('dc:creator', self._config['blog_author'], channel)
        self._addElemAttr('admin:generatorAgent', \
                          'rdf:resource', \
                          'http://pyblosxom.sourceforge.net/', \
                          channel)
        self._addElemAttr('admin:errorReportsTo', \
                          'rdf:resource', \
                          "mailto:" + self._config.get("blog_email", "none"), \
                          channel)

    def _generateDesc(self, html):
        s = Stripper()
        s.feed(html)
        str = s.gettext()
        frag = str.split()
        if len(frag) > self.desc_length:
            frag = frag[:self.desc_length]
            frag.append('...')
        return ' '.join(frag)

    def _createItem(self, entry):
        burl = self._config['base_url']

        d = urlparse.urlsplit(self._config['base_url'])
        domain = '%s://%s' % (d[0], d[1])
        item = self._doc.createElement('item')
        self._channel.appendChild(item)
        self._addText('title', entry['title'], item)
        self._addElemAttr('guid', 'isPermaLink', 'false', item, entry['file_path'])
        url = urlparse.urljoin(burl + "/", entry["file_path"])
        self._addText('link', self._urlEncode(url), item)

        # Text entry
        self._addText('description', self._generateDesc(entry['body']), item)
        if self.create_entry:
            if self.entry_type == 'CDATA':
                self._addCDATA('content:encoded', entry['body'], item)
            else:
                self._addText('content:encoded', entry['body'], item)
        # Metadata stuff
        # Category
        if entry['path'].strip():
            # category or dc:subject, but NOT both
            self._addElemAttr('category', 'domain', domain, item, entry['path'])
            #self._addText('dc:subject', entry['path'], item)
        self._addText('dc:date', entry['w3cdate'], item)

    def render(self, header = 1):
        if self.rendered == 1:
            return

        self._data = self._request.getData()
        self._config = self._request.getConfiguration()

        self.addHeader('Content-Type', 'application/xml')
        self.showHeaders()

        self._createChannel()

        if self._config.get("num_entries", 0):
            max_entries = self._config["num_entries"]
        else:
            max_entries = 20

        if self._content:
            if max_entries > len(self._content):
                num_entries = len(self._content)
            else:
                num_entries = max_entries

            for count in xrange(num_entries):
                self._createItem(self._content[count])

            # We are now ready to present the xml

            # FIXME this is totally hokey, but if I pass the encoding into
            # toxml, then it tries to convert the data to the new encoding
            # and assumes the data is ascii (which is wrong).
            text = self._doc.toxml()
            if self._config.has_key("blog_encoding"):
                text = "<?xml version=\"1.0\" encoding=\"%s\" ?>" % self._config["blog_encoding"] + text[text.find("\n"):]
            
            self.write(text)

        self.rendered = 1

def cb_renderer(args):
    import sys
    req = args['request']
    http = req.getHttp()
    conf = req.getConfiguration()

    ext = conf.get("rss2_extension", "/index.rss2")
    if http['PATH_INFO'].endswith( ext ):
        http['PATH_INFO'] = http['PATH_INFO'][:-len(ext)]
        return RSS2Renderer(req, conf.get('stdoutput', sys.stdout))

# vim: tabstop=4 shiftwidth=4 expandtab
