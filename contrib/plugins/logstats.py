"""
Keep statistics based on HTTP Log information

At the moment it computes a list of referrrers
Generate a string containing the last 15 referrers, marked up with HTML
<a> tag.  If the string is longer than 40 characters, truncate by displaying ...
You can access the list of referrers as the variable $referrers

You can control the number of referrers displayed in config.py:
py['num_referrers'] = n  

You can control the length of the referrer string in config.py:
py['referrer_length'] = l

TODO:
Compute some additional statistics
"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id$"

import os, re, string, time, cPickle
from libs import api

class PyblStats:
    def __init__(self, config):
        self._config = config
        self._referrers ={}
        self._referrersText = ""
        self._requestors = {}
        self._destinations = {}
        self._referrer_length = int(config.get('referrer_length', 10))
        self._num_referrers = int(config.get('num_referrers', 15))

    def __str__(self):
        """
        Returns the on-demand generated string - part of pybloxsom plugin fwk
        """
        if self._referrers == None:
            self.genReferrers()
        return self._referrersText

    def addReferer(self, uri):
        """
        Add a reference to a uri.
        
        @param uri - uri being referenced
        @type string
        """
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
        list = self._config.get('refer_blacklist','')
        if list:
            bad_list = string.split(list,',')
        else:
            bad_list = []

        def url(tuple):
            """
            Markup (and truncate) a referrer URL
            """
            uri = tuple[0]
            count = tuple[1]
            size = self._referrer_length
            vis = string.replace(uri,'http://','')
            if len(bad_list) > 0:
                for pat in bad_list:
                    if re.search(pat, uri):
                        return ""
            if len(uri) > size: vis = vis[:size]+'...'
            return ("""<a href="%(uri)s" title="%(uri)s">%(vis)s (%(count)d)</a><br />\n""" 
                    % {'uri': uri, 'vis': vis, 'count': count})

        def compareCounts(tuple1, tuple2):
            """
            Compare tuple1 and tuple2 by their second element
            """
            count1 = tuple1[1]
            count2 = tuple2[1]
            if count1 > count2:
                return -1 # reverse order
            if count1 < count2:
                return 1
            return 0

        items = self._referrers.items()
        # sort in alphabetical order first
        items.sort()
        # sort list by number of occurances
        items.sort(compareCounts)
        # make a list of urls
        refs = [ url(x) for x in items ]
        # remove blanks
        refs = [ x for x in refs if x != "" ]

        self._referrersText = string.join(refs[0:self._num_referrers-1])
        return self._referrersText

def prepare(args):
    """
    Callback registered with prepareChain.  This does all the work
    
    @param: args dict containing the request
    @type: dict
    """
    request = args["request"]
    config = request.getConfiguration()
    data = request.getData()

    try:
        filename = config['logfile']+'.dat'
        f = file(filename)
        stats = cPickle.load(f)
        stats._request = request
        stats._config = config
        stats._referrer_length = int(config.get('referrer_length', 15))
        stats._num_referrers = int(config.get('num_referrers', 15))
        f.close()

    except (EOFError, IOError):
        stats = PyblStats(config)

    stats.addReferer(os.environ.get('HTTP_REFERER', '-'))
    stats.addDestination(os.environ.get('REQUEST_URI', '-'))
    stats.addVisitor(os.environ.get('REMOTE_ADDR', '-'))

    data["referrers"] = stats.genReferrers()

    # next 2 lines null out modules vars for pickling
    stats._request = None
    stats._config = None
    f = file(filename,"w")
    cPickle.dump(stats, f)

def initialize():
    """
    Register the prepareChain handler
    """
    api.prepareChain.register(prepare)
