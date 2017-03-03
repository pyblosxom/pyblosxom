#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2004-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

Walks through your blog root figuring out all the available monthly
archives in your blogs.  It generates html with this information and
stores it in the ``$(archivelinks)`` variable which you can use in
your head and foot templates.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.pyarchives`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Configure using the following configuration variables.

``archive_template``

    Let's you change the format of the output for an archive link.

    For example::

        py['archive_template'] = ('<li><a href="%(base_url)s/%(Y)s/%(b)s">'
                                  '%(m)s/%(y)s</a></li>')

    This displays the archives as list items, with a month number,
    then a slash, then the year number.

    The formatting variables available in the ``archive_template``
    are::

        b         'Jun'
        m         '6'
        Y         '1978'
        y         '78'

    These work the same as ``time.strftime`` in python.

    Additionally, you can use variables from config and data.

    .. Note::

       The syntax used here is the Python string formatting
       syntax---not the Pyblosxom template rendering syntax!


Usage
=====

Add ``$(archivelinks)`` to your head and/or foot templates.

"""

__author__ = "Wari Wahab"
__email__ = "wari at wari dot per dot sg"
__version__ = "2011-10-22"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Builds month/year-based archives listing."
__category__ = "archives"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"

from Pyblosxom import tools
from Pyblosxom.memcache import memcache_decorator
from Pyblosxom.tools import pwrap
import time


def verify_installation(request):
    config = request.get_configuration()
    if not "archive_template" in config:
        pwrap(
            "missing optional config property 'archive_template' which "
            "allows you to specify how the archive links are created.  "
            "refer to pyarchive plugin documentation for more details.")
    return True


class PyblArchives:
    def __init__(self, request):
        self._request = request
        self._archives = None

    @memcache_decorator('pyarchives', True)
    def __str__(self):
        if self._archives == None:
            self.gen_linear_archive()
        return self._archives

    def gen_linear_archive(self):
        config = self._request.get_configuration()
        data = self._request.get_data()
        root = config["datadir"]
        archives = {}
        archive_list = tools.walk(self._request, root)
        full_dict = {}
        full_dict.update(config)
        full_dict.update(data)

        template = config.get('archive_template',
                              '<a href="%(base_url)s/%(Y)s/%(b)s">%(Y)s-%(b)s</a><br />')
        for mem in archive_list:
            timetuple = tools.filestat(self._request, mem)
            time_dict = {}
            for x in ["B", "b", "m", "Y", "y"]:
                time_dict[x] = time.strftime("%" + x, timetuple)

            full_dict.update(time_dict)
            if not (time_dict['Y'] + time_dict['m']) in archives:
                archives[time_dict['Y'] + time_dict['m']] = (template % full_dict)

        arc_keys = list(archives.keys())
        arc_keys.sort()
        arc_keys.reverse()
        result = []
        for key in arc_keys:
            result.append(archives[key])
        self._archives = '\n'.join(result)


def cb_prepare(args):
    request = args["request"]
    data = request.get_data()
    data["archivelinks"] = PyblArchives(request)
