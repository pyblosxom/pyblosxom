"""
Copyright (c) 2003-2005 Ted Leung

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Keep statistics based on HTTP Log information

At the moment it computes a list of referrrers
Generate a string containing the last 15 referrers, marked up with HTML
<a> tag.  If the string is longer than 40 characters, truncate by displaying ...
You can access the list of referrers as the variable $referrers

You can control the number of referrers displayed in config.py::
    py['num_referrers'] = n  

You can control the length of the referrer string in config.py::
    py['referrer_length'] = l

You can prevent some referrers from showing up in the list with the
refer_blacklist property in config.py:

    py['refer_blacklist'] = "bluesock.org,sauria.com"

TODO:
Compute some additional statistics

(2/15/2004 - Added locking [will])
(1/10/2004 - Added referrer page [will])
"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id$"

import os, re, string, time, pickle
from Pyblosxom import tools, entries

INIT_KEY = "logstats_static_file_initiated"

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
        
        @param uri: - uri being referenced
        @type uri: string
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
        l = self._config.get('refer_blacklist','')
        if l:
            bad_list = string.split(l,',')
        else:
            bad_list = []

        def url(tuple):
            """
            Markup (and truncate) a referrer URL
            """
            uri = tuple[0]
            count = tuple[1]
            size = self._referrer_length
            vis = uri
            if len(bad_list) > 0:
                for pat in bad_list:
                    if uri == "" or re.search(pat, uri):
                        return ""
            if len(uri) > size: vis = vis[:size]+'...'
            return ("""<a href="%(uri)s" title="%(uri)s">%(vis)s</a> (%(count)d)<br />\n""" 
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


    def genReferrersFiltered(self):
        """
        Generate the list of referring files
        """
        # initialize blacklist
        bad_list = self._config.get('refer_blacklist','')
        if bad_list:
            bad_list = string.split(bad_list,',')
        else:
            bad_list = []

        search_list = []
        search_list.append("www.google")
        search_list.append("google.com")
        search_list.append("search.yahoo.com")
        search_list.append("search.virgilio.it")
        search_list.append("aolsearch.aol.com")
        search_list.append("aolsearch.aol.co.uk")
        search_list.append("search.netscape.com")
        search_list.append("home.excite.co")
        search_list.append("search.earthlink.net")
        search_list.append("dion.excite.co.jp")
        search_list.append("altavista.com")
        search_list.append("mysearch.com")
        search_list.append("mysearch.myway.com")
        search_list.append("search.aol.com")
        search_list.append("search.msn.com")
        search_list.append("mail.yahoo.com")
        search_list.append("mywebsearch.com")

        def url(tuple):
            """
            Markup (and truncate) a referrer URL
            """
            uri = tuple[0]
            count = tuple[1]
            size = self._referrer_length
            vis = uri

            if len(bad_list) > 0:
                for pat in bad_list:
                    if uri == "" or re.search(pat, uri):
                        return ""

            for pat in search_list:
               if uri == "" or re.search(pat, uri):
                  return ""

            if len(uri) > size: vis = vis[:size]+'...'
            return ("""<a href="%(uri)s" title="%(uri)s">%(vis)s</a> (%(count)d)<br />\n""" 
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


    def genReferrerStats(self):
        output = ["<p>"]
        output.append("<b>Top %d referers (raw):</b><br><br>" % self._num_referrers)
        output.append(self.genReferrers())
        output.append("</p>")

        output.append("<p>")
        output.append("<b>Top %d referrers (filtered):</b><br><br>" % self._num_referrers)
        output.append(self.genReferrersFiltered())
        output.append("</p>")

        return "".join(output)


def cb_prepare(args):
    """
    Callback registered with prepareChain.  This does all the work
    
    @param args: args dict containing the request
    @type args: dict
    """
    request = args["request"]
    config = request.getConfiguration()
    data = request.getData()
    httpData = request.getHttp()
    datadir = config["datadir"]

    try:
        f = open(datadir + "/logfile.dat", "r+")
        tools.lock(f, tools.LOCK_EX)

        stats = pickle.load(f)
        f.seek(0, 0)

    except:
        f = open(datadir + "/logfile.dat", "w")
        tools.lock(f, tools.LOCK_EX)

        stats = PyblStats(config)

    stats._request = request
    stats._config = config
    stats._referrer_length = int(config.get('referrer_length', 15))
    stats._num_referrers = int(config.get('num_referrers', 15))

    stats.addReferer(httpData.get('HTTP_REFERER', '-'))
    stats.addDestination(httpData.get('REQUEST_URI', '-'))
    stats.addVisitor(httpData.get('REMOTE_ADDR', '-'))

    data["referrers"] = stats.genReferrers()

    # next 2 lines null out modules vars for pickling
    stats._request = None
    stats._config = None

    pickle.dump(stats, f)

    tools.unlock(f)
    f.close()


def generate_entry(request, output):
    """
    Takes a bunch of text and generates an entry out of it.  It creates
    a timestamp so that conditionalhttp can handle it without getting
    all fussy.
    """
    entry = entries.base.EntryBase(request)

    entry['title'] = "Referrers List"
    entry['filename'] = "referrerlist"
    entry['file_path'] = "referrerlist"
    entry._id = "referrerlist"

    entry.setTime(time.localtime())

    entry.setData(output)
    return entry


def cb_date_head(args):
    request = args["request"]
    data = request.getData()
    if data.has_key(INIT_KEY):
        entry = args["entry"]
        entry["date"] = ""
    return args


def cb_filelist(args):
    request = args["request"]
    pyhttp = request.getHttp()
    data = request.getData()
    config = request.getConfiguration()
    datadir = config["datadir"]

    if not pyhttp["PATH_INFO"].startswith("/referrers"):
        return

    data[INIT_KEY] = 1

    filename = datadir + '/logfile.dat'
    try:
        f = open(filename)
        stats = pickle.load(f)
        stats._request = request
        stats._config = config
        stats._referrer_length = int(config.get('referrer_length', 15))
        stats._num_referrers = int(config.get('num_referrers', 15))
        f.close()

    except (EOFError, IOError):
        stats = PyblStats(config)
    return [generate_entry(request, stats.genReferrerStats())]

def verify_installation(request):
    config = request.getConfiguration()
    retval = 1

    # all config properties are optional
    props = ['referrer_length','num_referrers', 'refer_blacklist']
    for i in props:
        if not config.has_key(i):
            print("missing optional property: '%s'" % i)

    return retval
