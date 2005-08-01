PREFORMATTER_ID = 'reST'
FILE_EXT = 'rst'
"""
A reStructuredText entry formatter for pyblosxom.  reStructuredText is 
part of the docutils project (http://docutils.sourceforge.net/).  To 
use, you need a *recent* version of docutils.  A development snapshot 
(http://docutils.sourceforge.net/#development-snapshots) will work fine.  

Install docutils, copy this file to your pyblosxom Pyblosxom/plugins
directory, and you're ready to go.  Files with a .rst extension will be
marked up as reStructuredText. 

You can configure this as your default preformatter for .txt files by
configuring it in your config file as follows::

    py['parser'] = 'reST'

or in your blosxom .txt file entries, place a '#parser reST' line after the
title of your blog::

    My Little Blog Entry
    #parser reST
    My main story...

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright 2003, 2004, 2005 Sean Bowman
"""
__version__ = '$Id$'
__author__ = 'Sean Bowman <sean dot bowman at acm dot org>'

from docutils.core import publish_string
from Pyblosxom import tools

def cb_entryparser(args):
    args[FILE_EXT] = readfile
    return args

def cb_preformat(args):
    if args['parser'] == PREFORMATTER_ID:
        return parse(''.join(args['story']))

def parse(story):
    html = publish_string(story, writer_name='html')
    return html[html.find('<body>') + 6:html.find('</body>')]

def readfile(filename, request):
    entryData = {}
    d = open(filename).read()
    title = d.split('\n')[0]
    d = d[len(title):]
    body = parse(d)
    entryData = {'title': title,
                 'body': body}
    # Call the postformat callbacks
    tools.run_callback('postformat',
            {'request': request,
             'entry_data': entryData})
    
    return entryData
