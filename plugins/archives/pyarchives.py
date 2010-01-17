# vim: tabstop=4 shiftwidth=4
"""
Walks through your blog root figuring out all the available monthly archives in
your blogs.  It generates html with this information and stores it in the
$archivelinks variable which you can use in your head or foot templates.

You can format the output with the key "archive_template".

A config.py example:

    py['archive_template'] = '<li><a href="%(base_url)s/%(Y)s/%(b)s">%(m)s/%(y)s</a></li>'

Displays the archives as list items, with a month number slash year number, like 06/78.

The vars available with typical example values are:
    b      'Jun'
    m      '6'
    Y      '1978'
    y      '78'


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
__author__ = "Wari Wahab - wari at wari dot per dot sg"
__version__ = "$Id$"

from Pyblosxom import tools
import time, os

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
