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

There's two optional configuration parameter you can for additional control
over the rendered HTML::

  # To set the starting level for the rendered heading elements.
  # 1 is the default.
  py['reST_initial_header_level'] = 1
  
  # Enable or disable the promotion of a lone top-level section title to
  # document title (and subsequent section title to document subtitle
  # promotion); enabled by default.
  py['reST_transform_doctitle'] = 1
    
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

Copyright 2003-2005 Sean Bowman
"""
__version__ = '$Id$'
__author__ = 'Sean Bowman <sean dot bowman at acm dot org>'

from docutils.core import publish_parts
from Pyblosxom import tools

def cb_entryparser(args):
    args[FILE_EXT] = readfile
    return args

def cb_preformat(args):
    if args.get("parser", None) == PREFORMATTER_ID:
        return parse(''.join(args['story']), args['request'])
    
def parse(story, request):
    config = request.getConfiguration()
    initial_header_level = config.get('reST_initial_header_level', 1)
    transform_doctitle = config.get('reST_transform_doctitle', 1)
    settings = {
        'initial_header_level': initial_header_level, 
        'doctitle_xform': transform_doctitle
        }
    parts = publish_parts(
        story, writer_name='html', settings_overrides=settings)
    return parts['html_body']

def readfile(filename, request):
    entryData = {}
    lines = open(filename).readlines()
    title = lines.pop(0)
    body = parse(''.join(lines), request)
    entryData = {'title': title, 'body': body}
    # Call the postformat callbacks
    tools.run_callback(
        'postformat', {'request': request, 'entry_data': entryData})
    return entryData
