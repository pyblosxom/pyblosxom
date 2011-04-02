#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (C) 2004, 2005, 2006 Wari Wahab
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

Walks through your blog root figuring out all the available monthly
archives in your blogs.  It generates html with this information and
stores it in the ``$archivelinks`` variable which you can use in your
head and foot templates.

You can change the format of the output in ``config.py`` with the 
``archive_template`` key.

A config.py example::

    py['archive_template'] = "<li><a href="%(base_url)s/%(Y)s/%(b)s">%(m)s/%(y)s</a></li>"

This displays the archives as list items, with a month number slash
year number, like 06/78.

.. Note::

   The syntax used here is the Python string formatting syntax---not
   the PyBlosxom template rendering syntax!


The formatting variables available in the ``archive_template`` are::

    b      'Jun'
    m      '6'
    Y      '1978'
    y      '78'


These work the same as ``time.strftime`` in python.

"""

__author__ = "Wari Wahab"
__email__ = "wari at wari dot per dot sg"
__version__ = "$Id$"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = "Builds month/year-based archives listing."
__category__ = "archives"
__license__ = "MIT"


from Pyblosxom import tools
import time
import os


def verify_installation(request):
    config = request.get_configuration()
    if not config.has_key("archive_template"):
        print "missing optional config property 'archive_template' which "
        print "allows you to specify how the archive links are created.  "
        print "refer to pyarchive plugin documentation for more details."
    return 1


class PyblArchives:
    def __init__(self, request):
        self._request = request
        self._archives = None

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
        fulldict = {}
        fulldict.update(config)
        fulldict.update(data)
        
        template = config.get('archive_template', 
                    '<a href="%(base_url)s/%(Y)s/%(b)s">%(Y)s-%(b)s</a><br />')
        for mem in archive_list:
            timetuple = tools.filestat(self._request, mem)
            timedict = {}
            for x in ["B", "b", "m", "Y", "y"]:
                timedict[x] = time.strftime("%" + x, timetuple)

            fulldict.update(timedict)
            if not archives.has_key(timedict['Y'] + timedict['m']):
                archives[timedict['Y'] + timedict['m']] = (template % fulldict)

        arc_keys = archives.keys()
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
