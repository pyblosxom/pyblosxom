# vim: tabstop=4 shiftwidth=4 expandtab
"""
Preformatter and entryparser for the MoinMoin wiki software

This preformatter/entryparser uses the services of MoinMoin
http://moin.sourceforge.net/ which is an excellent open source WikiWiki system.

Requirements:
    
    - A working MoinMoin installation
    - C{moin_config.py} at your sys path (not necessary though)

You can configure this as your default preformatter by configuring it in your
L{config} file as follows::

    py['parser'] = 'wiki'

or in your blosxom entries, place a C{#parser wiki} line after the title of
your blog::

    My Little Blog Entry
    #parser wiki
    This is a text in '''wiki''' format

To use this as an entryparser, all you need to do is to name your files with a
.wiki extension. For example a helloworld.wiki file could contain::

    Hello World <- The title
    This is the ''wiki'' text :)

@var __author__: Who's to blame for this
@var __version__: Revision of this module
@var PREFORMATTER_ID: This preformatter will activate on this ID
"""
__author__ = 'Wari Wahab <wari at wari dot per dot sg>'
__version__ = "$Id$"
PREFORMATTER_ID = 'wiki'

from MoinMoin.parser.wiki import Parser
from MoinMoin.formatter.text_html import Formatter
from MoinMoin.request import Request
from MoinMoin.Page import Page
from MoinMoin.user import User
from cStringIO import StringIO
from Pyblosxom import tools
import sys


def cb_preformat(args):
    """
    Preformat callback chain looks for this.

    @param args: a dict with 'parser' string and a list 'story'
    @type args: dict
    """
    if args['parser'] == PREFORMATTER_ID:
        return parse(''.join(args['story']))


def cb_entryparser(args):
    """
    Entryparser chain callback - This plugins takes in a *.wiki file and treats
    it like a normal blosxom entry file. Postformat callbacks are also called
    from this entryparser.

    @param args: dict containing function references for each extensions
    @type args: dict
    @returns: updated dict containing the reference for .wiki entryparser
    @rtype: dict
    """
    args['wiki'] = readfile
    return args


def readfile(filename, request):
    """
    Reads a file and passes it to L{parse} to format in moinmoin wiki

    @param filename: the file in question
    @param request: The request object
    @type filename: string
    @type request: L{Pyblosxom.Request.Request} object
    @returns: Data of the entry
    @rtype: dict
    """
    entryData = {}
    d = open(filename).read()
    entryData['title'] = d.split('\n')[0]
    d = d[len(entryData['title']):] 
    entryData['body'] = parse(d)
    # Call the postformat callbacks
    tools.run_callback('postformat',
            {'request': request,
             'entry_data': entryData})
    return entryData

    
def parse(story):
    """
    The main workhorse that does nothing but call MoinMoin to do its dirty
    laundry

    @param story: A text for conversion
    @type story: string
    @returns: formatted string
    @rtype: string
    """
    s = StringIO()
    oldstdout = sys.stdout
    form = None
    page = Page(None)
    page.hilite_re = None
    request = Request()
    request.user = User()
    formatter = Formatter(request)
    formatter.setPage(page)
    sys.stdout = s
    Parser(story, request).format(formatter, form)
    sys.stdout = oldstdout
    result = s.getvalue()
    s.close()
    return result
