PREFORMATTER_ID = 'textile'
FILE_EXT = 'txtl'
"""
PyTextile is a Python port of Textile, Dean Allen's Humane Web Text Generator.
It supports all the features of the original, with the exception of converting
high-bit characters to their HTML numeric entity equivalent.
See: http://diveintomark.org/projects/pytextile/index.html for details

Install textile.py in a python searchable path, copy this file to your
pyblosxom Pyblosxom/plugins directory, and you're ready to go.  Files with a
.txtl extension will be marked up as textile. 

You can configure this as your default preformatter for .txt files by
configuring it in your config file as follows::

    py['parser'] = 'textile'

or in your blosxom .txt file entries, place a '#parser textile' line after the
title of your blog::

    My Little Blog Entry
    #parser textile
    My main story...
"""

__version__ = '$Id$'
__author__ = 'Wari Wahab <wari at home dot wari dot org>'

from Pyblosxom import tools
from textile import textile

def cb_entryparser(args):
    args[FILE_EXT] = readfile
    return args

def cb_preformat(args):
    if args['parser'] == PREFORMATTER_ID and \
           args['request'].getData()['flavour'] == "html":
        return parse(''.join(args['story']))
    else:
        return ''.join(args['story']).replace("&","&") 

def parse(story):
    return textile(story)

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
