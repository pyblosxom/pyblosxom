# vim: tabstop=4 shiftwidth=4 expandtab
"""
Preformatter for the MoinMoin wiki software

This preformatter uses the services of MoinMoin http://moin.sourceforge.net/
which is an excellent open source WikiWiki system.

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
import sys


def cb_preformat(args):
    """
    Preformat callback chain looks for this.

    @params args: a dict with 'parser' string and a list 'story'
    @type args: dict
    """
    if args['parser'] == PREFORMATTER_ID:
        return parse(''.join(args['story']))


def parse(story):
    """
    The main workhorse that does nothing but call MoinMoin to do its dirty
    laundry

    @params story: A text for conversion
    @type story: string
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
