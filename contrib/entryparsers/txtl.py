PREFORMATTER_ID = 'textile'
FILE_EXT = 'txtl'
"""
PyTextile is a Python port of Textile, Dean Allen's Humane Web Text Generator.
It supports all the features of version 2 and some more.
See: http://dealmeida.net/projects/textile/ for details.

Install textile.py in a python searchable path, copy this file to your
pyblosxom Pyblosxom/plugins directory, and you're ready to go.  Files with a
.txtl extension will be marked up as textile. 

If you want PyTextile to syntax-highlight Python snippets, you need the 
htmlizer module from twisted.python. If you don't have Twisted installed, you
can download htmlizer.py from http://dealmeida.net/code/htmlizer.py.txt.

To highlight Python code, use the "blockcode" signature, specifying the 
language as Python:

    bc[python].. from Pyblosxom import tools
    from textile import textile

    pass

Keywords in the code will receive <span> tags, which should be customized
using CSS. This is the CSS I use:

    .py-src-keyword {
        color: blue;
        font-weight: bold;
    }

    .py-src-triple {
        color: red;
    }

    .py-src-comment {
        color: green;
        font-style: italic;
    }

    .py-src-identifier {
        color: teal;
        font-weight: bold;
    }

    .py-src-string {
        color: purple;
    }

    .py-src-op {
        color: #333;
        font-weight: bold;
    }

PyTextile can optionally validate the generated XHTML, using either Mx.Tidy
(http://www.egenix.com/files/python/mxTidy.html) or uTidyLib
(http://utidylib.sourceforge.net/). Both depend on TidyLib. To enable the
validation, add the following to your config file:

    py['txtl_validate'] = 1

It's also a good thing to set your encoding and the desired output:

    py['txtl_encoding'] = 'latin-1'
    py['txtl_output'    = 'ascii'

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


def verify_installation(request):
    
    config = request.getConfiguration()

    # First let's see if we can find the textile module.
    try:
        from textile import textile
    except ImportError:
        print "I couldn't find the textile module. Did you add it to the path?"
        print
        return 0

    # Now let's search for the htmlizer module.
    try:
        from twisted.python import htmlizer
    except ImportError:
        try:
            import htmlizer
        except ImportError:
            print "I couldn't find the optional htmlizer module. If you want"
            print "PyTextile to syntax-highlight Python code, download it from"
            print "http://dealmeida.net/code/htmlizer.py.txt"
            print

    # Search for the Tidy modules.
    try:
        from mx.Tidy import Tidy as tidy
    except ImportError:
        try:
            import tidy
        except ImportError:
            print "I couldn't find any wrapper to TidyLib. If you want PyTextile"
            print "validating the generated XHTML, download either mx.Tidy"
            print "(http://www.egenix.com/files/python/mxTidy.html) or uTidyLib"
            print "(http://utidylib.sourceforge.net/)"
            print
            tidy = None

    if tidy and not config.has_key('txtl_validate'):
        print "You can enable/disable automatic validation of your posts with"
        print "this variable on your config file:"
        print
        print "    py['txtl_validate'] = 0  # disable"
        print "    py['txtl_validate'] = 1  # enable"
        print

    # Low let's discover the value of head_offset.
    # Search story.html.
    try:
        f = open('%s/story.html' % config['datadir'])
        story = f.read()
        f.close()

        import re

        headers = re.findall(r'<h(\d).*?>', story)
        if headers:
            headers.sort()
            max_header = headers[-1]
        
        else:
            # Let's look at head.html.
            f = open('%s/head.html' % config['datadir'])
            head = f.read()
            f.close()

            headers = re.findall(r'<h(\d).*?>', head)
            if headers:
                headers.sort()
                max_header = headers[-1]
            else:
                max_header = 0
    
        if max_header:
            print ""

    except:
        max_header = 0

    if max_header and not config.has_key('txtl_head_offset'):
        print "It is a good idea to specify a header offset for the headers on your"
        print "posts. This way, you can always set the first header on your post"
        print "to <h1>, and PyTextile will adjust it for you according to your"
        print "template. My suggestion is that you add the following to your config:"
        print
        print "    py['txtl_head_offset'] = %s" % max_header
        print
    
    return 1


from Pyblosxom import tools
from textile import textile


def cb_entryparser(args):
    args[FILE_EXT] = readfile
    return args


def cb_preformat(args):
    if args['parser'] == PREFORMATTER_ID:
        return parse(''.join(args['story']))
    else:
        return ''.join(args['story'])


def readfile(filename, request):
    entryData = {}
    d = open(filename).read()

    # Grab title and body.
    title = d.split('\n')[0]
    body  = d[len(title):]

    # Grab textile configuration.
    config = request.getConfiguration()
    head_offset = config.get('txtl_head_offset', 0)
    validate    = config.get('txtl_validate', 0)
    output      = config.get('txtl_output', 'ascii')
    encoding    = config.get('txtl_encoding', 'latin-1')
    
    body = textile(body, head_offset=head_offset, validate=validate, output=output, encoding=encoding)

    entryData = {'title': title,
                 'body': body}

    # Call the postformat callbacks
    tools.run_callback('postformat',
            {'request': request,
             'entry_data': entryData})
    
    return entryData
