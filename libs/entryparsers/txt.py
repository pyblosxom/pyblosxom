# vim: shiftwidth=4 tabstop=4 expandtab
"""
The standard pyblosxom entry parser, uses preformatters that's located in
libs/preformatters/ After retrieving all the relevant information, it saves all
the data in the cache

To define a default parser add this line in your config.py
py['parser'] = xxxx

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

def parse(filename, py, cache):
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

    preformatter = tools.importName('libs.preformatters', py.get('parser', 'plain'))
    if preformatter:
        entryData['body'] = preformatter.PreFormatter(story).parse()
    else:
        entryData['body'] = ''.join(story)
    
    cache.saveEntry(entryData)

    return entryData
