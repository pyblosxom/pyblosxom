"""
Keep statistics based on HTTP Log information

At the moment it computes a list of referrrers
Generate a string containing the last 15 referrers, marked up with HTML
<a> tag.  If the string is longer than 40 characters, truncate by displaying ...
You can access the list of referrers as the variable $referrers

TODO:
Allow number of referrers as parameters
Compute some additional statistics
"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id$"

import string, re, time, cPickle
from libs import api

class PyblStats:
    def __init__(self, py):
        self._py = py
        self._referrers ={}
        self._referrersText = ""
        self._requestors = {}
        self._destinations = {}


    def __str__(self):
        """
        Returns the on-demand generated string - part of pybloxsom plugin fwk
        """
        if self._referrers == None:
            self.genReferrers()
        return self._referrersText

    def addReferer(self, uri):
        # process -
        if uri == '-':
            return

        if self._referrers.has_key(uri):
            count = self._referrers[uri]
        else:
            count = 1
        self._referrers[uri]=count+1

    def addDestination(self, uri):
        return uri

    def addVisitor(self, uri):
        return uri

    def genReferrers(self):
        """
        Generate the list of referring files
        """
        # initialize blacklist
        if self._py.has_key('refer_blacklist'):
            bad_list = string.split(self._py['refer_blacklist'],',')

        def url(tuple):
            """
            Markup (and truncate) a referrer URL
            """
            uri = tuple[0]
            count = tuple[1]
            size = 32
            vis = uri
            if len(bad_list) > 0:
                for pat in bad_list:
                    if re.search(pat, uri):
                        return ""
            if len(uri) > size: vis = vis[:size]+'...'
            return '<a href="'+uri+'" title="'+uri+'">'+vis+' ('+str(count)+')'+'</a><br />\n'

        def compareCounts(tuple1, tuple2):
            count1 = tuple1[1]
            count2 = tuple2[1]
            if count1 > count2:
                return -1 # reverse order
            if count1 < count2:
                return 1
            return 0
        
        items = self._referrers.items()
        # sort list by number of occurances
        items.sort(compareCounts)
        # make a list of urls
        refs = [ url(x) for x in items ]
        # remove blanks
        refs = [ x for x in refs if x != "" ]

        self._referrersText = string.join(refs[0:24])
        return self._referrersText

def processRequest(args):
    if args == None or args[0] == '':
        return
    import os
    filename = args[0]+'.dat'
    returnCode = args[1]

    try:
        f = file(filename)
        stats = cPickle.load(f)
        f.close()
    except IOError:
        stats = PyblStats({})

    stats.addReferer(os.environ.get('HTTP_REFERER', '-'))
    stats.addDestination(os.environ.get('REQUEST_URI', '-'))
    stats.addVisitor(os.environ.get('REMOTE_ADDR', '-'))

    f = file(filename,"w")
    cPickle.dump(stats, f)


def initialize():
    api.logRequest.register(processRequest)

def load(py, entryList, renderer):
    """
    part of the pyblosxom framework
    """
    try:
        filename = py['logfile']+'.dat'
        f = file(filename)
        stats = cPickle.load(f)
        stats._py = py
        f.close()
    except IOError:
        stats = PyblStats(py)

    py["referrers"] = stats.genReferrers()


# command line testing
if __name__ == '__main__':
    pass
