# vim: tabstop=4 shiftwidth=4 expandtab
"""
Preformatter for people who are lazy to type <p>s, <br />s, and </p>

Let's face it, HTML is hard, and us non-html slaves do not need treatment that
HTML markups do to us.

This preformat plugin will help you with all the silly linebreaks markup and
convert them to either a <br /> for those one liners, or a <p> for those blank
lines.

You can configure this as your default preformatter by configuring it in your
L{config} file as follows::

    py['parser'] = 'linebreaks'

or in your blosxom entries, place a C{#parser wiki} line after the title of
your blog::

    My Little Blog Entry
    #parser linebreaks
    This is a text
    that will become

    properly tagged html for simple 
    linebreaks

@var __author__: Who's to blame for this
@var __version__: Revision of this module
@var PREFORMATTER_ID: This preformatter will activate on this ID
"""
__author__ = 'Wari Wahab <wari at wari dot per dot sg>'
__version__ = "$Id$"
PREFORMATTER_ID = 'linebreaks'

import re
def cb_preformat(args):
    """
    Preformat callback chain looks for this.

    @param args: a dict with 'parser' string and a list 'story'
    @type args: dict
    """
    if args['parser'] == PREFORMATTER_ID:
        return parse(''.join(args['story']))


def parse(text):
    """
    Load some text and add linebreaks markup

    @param text: A text for conversion
    @type text: string
    """
    text = re.sub('\n\n+','</p><p>',text)
    text = re.sub('\n','<br />',text)
    return '<p>%s</p>' % text
