PREFORMATTER_ID = 'reST'
FILE_EXT = 'rst'
"""
A reStructuredText entry formatter for pyblosxom.  reStructuredText is 
part of the docutils project (http://docutils.sourceforge.net/).  To 
use, you need a *recent* version of docutils.  A development snapshot 
(http://docutils.sourceforge.net/#development-snapshots) will work fine.  

Install docutils, copy this file to your pyblosxom libs/plugins
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
"""
__version__ = '$Id$'
__author__ = 'Sean Bowman <sean dot bowman at acm dot org>'

from docutils.core import publish_string
from libs import tools

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
    d = file(filename).read()
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
