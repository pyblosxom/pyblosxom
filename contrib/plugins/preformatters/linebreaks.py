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

Copyright 2004, 2005 Wari Wahab
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
