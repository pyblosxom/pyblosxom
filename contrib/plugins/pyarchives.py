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
"""
__author__ = "Wari Wahab - wari at wari dot per dot sg"
__version__ = "$Id$"

from Pyblosxom import tools
import time

class PyblArchives:
    def __init__(self, request):
        self._request = request
        self._archives = None

    def __str__(self):
        if self._archives == None:
            self.genLinearArchive()
        return self._archives

    def genLinearArchive(self):
        config = self._request.getConfiguration()
        data = self._request.getData()
        root = config["datadir"]
        archives = {}
        archiveList = tools.Walk(self._request, root)
        fulldict = {}
        fulldict.update(config)
        fulldict.update(data)
        
        template = config.get('archive_template', 
                    '<a href="%(base_url)s/%(Y)s/%(b)s">%(Y)s-%(b)s</a><br />')
        for mem in archiveList:
            timetuple = tools.filestat(self._request, mem)
            timedict = dict([(x, time.strftime('%' + x, timetuple)) 
                            for x in list('bmYy')])
            fulldict.update(timedict)
            if (timedict['Y'] + timedict['m']) not in archives:
                archives[timedict['Y'] + timedict['m']] = (template % fulldict)

        arcKeys = archives.keys()
        arcKeys.sort()
        arcKeys.reverse()
        result = []
        for key in arcKeys:
            result.append(archives[key])
        self._archives = '\n'.join(result)

def cb_prepare(args):
    request = args["request"]
    data = request.getData()
    data["archivelinks"] = PyblArchives(request)
