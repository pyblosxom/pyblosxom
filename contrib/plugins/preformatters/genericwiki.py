# vim: tabstop=4 shiftwidth=4 expandtab
"""
Generic wiki markup PreFormatter 2002-11-18, for pyblosxom
CHANGE wikibaseurl to point to your wiki, & wikinamepattern to yours
Bug reports, comments, presents, etc. to John Abbe at johnca@ourpla.net
ToDo: Lists; code/<pre>; InterWiki links; other wikinamepatterns

You can configure this as your default preformatter by configuring it in your
L{config} file as follows::

    py['parser'] = 'genericwiki'

or in your blosxom entries, place a C{#parser wiki} line after the title of
your blog::

    My Little Blog Entry
    #parser genericwiki
    This is a text in '''wiki''' format

@var __author__: Who's to blame for this
@var __version__: Revision of this module
@var PREFORMATTER_ID: This preformatter will activate on this ID
"""
__author__ = 'John Abbe <johnca at ourpla dot net>'
__version__ = "$Id$"
PREFORMATTER_ID = 'genericwiki'
import re

def cb_preformat(args):
    """
    Preformat callback chain looks for this.

    @params args: a dict with 'parser' string and a list 'story'
    @type args: dict
    """
    if args['parser'] == PREFORMATTER_ID:
        return parse(args['story'])


def parse(text):
    """
    The main workhorse that convert normal text into rudimentary wiki format

    @params text: A list of text for conversion
    @type text: list
    """
    # url of your wiki up to page name
    wikibaseurl = "http://ourpla.net/cgi/pikie?"
    # WikiName pattern used in your wiki
    wikinamepattern = r'\b(([A-Z]+[a-z]+){2,})\b' # original
    mailurlpattern = r'mailto\:[\"\-\_\.\w]+\@[\-\_\.\w]+\w'
    newsurlpattern = r'news\:(?:\w+\.){1,}\w+'
    fileurlpattern = r'(mailto|http(s)?|ftp):(//)?[\w]+(\.[\w]+)([-\w.,@?^=%&;:/~+#]*)?'
    result = ''
    for line in text:
        result += line

    # Turn '[xxx:address label]' into labeled link
    result = re.sub(r'\[(' +
             fileurlpattern + '|' +
             mailurlpattern + '|' +
             newsurlpattern + ')\ (.+?)\]',
             r'<a href="\1">\2</a>', result)

    # Convert naked URLs into links -- skip ones with a " before
    result = re.sub(r'(?<!")(' +
             fileurlpattern + '|' +
             mailurlpattern + '|' +
             newsurlpattern + ')',
             r'<a href="\1">\1</a>', result)

    # Convert WikiNames into links
    result = re.sub(r'(?<![\?\/\=])' +
             wikinamepattern, '<a href="' +
             wikibaseurl + r'\1">\1</a>', result)

    # '' for emphasis, ''' for strong, ---- for a horizontal rule
    result = re.sub(r"'''(.*?)'''", r"<strong>\1</strong>", result)
    result = re.sub(r"''(.*?)''", r"<em>\1</em>", result)
    result = re.sub(r"\n(-{4,})\n", "<hr>", result)

    # Convert two or more newlines into <p>
    result = re.sub(r'\n{2,}', r'</p>\n<p>', result)

    return "<p>" + result + "</p>"
