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
"""
import libs, os

def cb_story(args):
    """
    This method will spit out - or + depending on the existence of
    py['tb_data'] + entry['tb_id'] + '.stor' file.
    """
    entry = args['entry']
    request = libs.tools.get_registry()["request"]
    config = request.getConfiguration()

    datadir = config.get('tb_data', '')
    id = entry['tb_id'] or ''

    entry['tb'] = (os.path.isfile(os.path.join(datadir, id + '.stor')) and '+' or '-')
