# vim: tabstop=4 shiftwidth=4 expandtab
"""
This plugin replaces the legacy $tb in older pyblosxoms <= 0.6

Since there is a proper plugin for feedback, this is deprecated as it
uses the MovableType's Standalone Trackback Utility. Since I have no
idea how python can read perl's Storable data, to know if you've got a
trackback or not means $tb is either a '+' or a '-'.

Trackback data directory (If you install Standalone Trackback Tool) is
configured in your config.py this way::

    py['tb_data'] = '/path/to/tb_data/directory'

The Movabletype Standalone Trackback tool can be found at
http://www.movabletype.org/docs/tb-standalone.html This is useful for blosxom
users :)

Using this plugin:

Please refer to the documentation at:

    - http://www.movabletype.org/docs/tb-standalone.html
    - http://wiki.subtlehints.net/moin/PyBlosxom_2fTemplateVariables
    - http://www.raelity.org/archives/computers/internet/weblogs/blosxom/youve_got_trackbacks.html
    - http://www.raelity.org/archives/computers/internet/weblogs/blosxom/trackback_blosxom_conversion_chart.html


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
__version__ = "$Id$"

import Pyblosxom, os

def cb_story(args):
    """
    This method will spit out - or + depending on the existence of
    py['tb_data'] + entry['tb_id'] + '.stor' file.
    """
    entry = args['entry']
    request = args["request"]
    config = request.getConfiguration()

    datadir = config.get('tb_data', '')
    id = entry['tb_id'] or ''

    entry['tb'] = (os.path.isfile(os.path.join(datadir, id + '.stor')) and '+' or '-')
