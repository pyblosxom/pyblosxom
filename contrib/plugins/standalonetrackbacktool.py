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

import os, libs

class StandAloneTrackBackTool:
    """
    This class will spit out - or + depending on the existence of
    py['tb_data'] + self._ob[tb_id] + '.stor' file.
    """
    def __init__(self, ob):
        self._ob = ob
    
    def __str__(self):
        """
        Determine if the trackback file exists

        @returns: A '+' or '-' depending on the availability of the file
        produced by the standalone trackback tool
        @rtype: string
        """
        request = libs.tools.get_registry()["request"]
        config = request.getConfiguration()
        datadir = config["tb_data"]
        id = self._ob['tb_id']

        return (os.path.isfile(os.path.join(datadir, id + '.stor')) and '+' or '-')


def cb_prepare(args):
    """
    This method gets called in the prepareChain.  It gets passed
    the Request object as the first member of the args tuple.
    """
    request = args["request"]
    entry_list = request.getData()["entry_list"]
    for mem in entry_list:
        # this creates a loop--but since this is a cgi we don't
        # really care about potential garbage collection issues
        mem["tb"] = StandAloneTrackBackTool(mem)
