# vim: shiftwidth=4 tabstop=4 expandtab
"""
The standard pyblosxom entry parser, uses preformat and postformat plugins
that's located in C{/contrib/plugins/preformatters} and C{/contrib/plugins}.

To define a default parser/preformatter add this line in your config.py
py['parser'] = xxxx

Where xxxx is the preformatter id (Look at the preformatter's plugin
documentation)

To use other preformatters than the default one you define, add the following
text in your entry text file:
--------------------
Your title
#parser yourpreferredparser
Text of entry, etc, etc
--------------------
"""
from libs import tools
import re

def parse(filename, request):
    """
    Open up a txt file and read its contents

    @param filename: A filename to extra data and meta data from
    @type filename: string
    @param request: A standard request object
    @type request: L{libs.Request.Request} object
    @returns: A dict containing parsed data and meta data with the particular
            file (and plugin)
    @rtype: dict
    """
    config = request.getConfiguration()

    entryData = {}

    try:
        story = file(filename).readlines()
    except IOError:
        raise IOError

    if len(story) > 0:
        entryData['title'] = story.pop(0).strip()

    while len(story) > 0:
        match = re.match(r'^#(\w+)\s+(.*)', story[0])
        if match:
            story.pop(0)
            entryData[match.groups()[0]] = match.groups()[1].strip()
        else:
            break

    # Call the preformat function
    entryData['body'] = tools.run_callback('preformat',
            {'parser': (entryData.get('parser', '') 
                    or config.get('parser', 'plain')),
             'story': story,
             'request': request},
            donefunc = lambda x:x != None,
            defaultfunc = lambda x: ''.join(x['story']))

    # Call the postformat callbacks
    tools.run_callback('postformat',
            {'request': request,
             'entry_data': entryData})
            
    return entryData
