# vim: tabstop=4 shiftwidth=4 expandtab
"""
Pings Weblogs.com and blo.gs with every new entry

Requires a file in the server that is writable by the webserver. (Default file
is py['datadir']/LATEST).

If your py['datadir'] is read only to the web server, you can create a
directory and make sure that it's writable by the webserver, e.g. 'chmod 777
directory' or using some other methods (mine runs pyblosxom in SuExec mode).

After doing so, change the self._file value in __init__() and you're game.

You can read the data of the self._file using cPickle in python interactive
mode to see if your ping is successful:
>>> import cPickle
>>> cPickle.load(file('/path/to/data/file'))
"""
__author__ = "Wari Wahab pyblosxom@wari.per.sg"
__version__ = "$Id$"

import xmlrpclib, os, time
import cPickle as pickle

class weblogsPing:
    def __init__(self, py, entryList):
        self.pingData = {}
        self._latest = entryList[0]['mtime']
        self._file = os.path.join(py['datadir'], 'LATEST')
        self._title = py['blog_title']
        self._site = 'http://%s%s' % (os.environ['HTTP_HOST'], 
                     os.environ['SCRIPT_NAME'])
        self._xml = self._site + '?flav=rss'

    def ping(self):
        if os.path.isfile(self._file):
            try:
                fp = file(self._file, 'rb')
                self.pingData = pickle.load(fp)
                fp.close()
            except IOError:
                # Something wrong with the file, abort.
                return
        else:
            # If we cannot save, forget about pinging
            if not self.__saveResults(0, 'fresh', 'fresh'):
                return
        
        # Timecheck.
        if self._latest > self.pingData['lastPing'] or \
           self._latest > self.pingData['latest']:
            self.__doPing()
        return

    def __doPing(self):
        pingTime = int(time.time())
        # Save this data first else we'll go crazy with looping
        if not self.__saveResults(pingTime, 'buffer', 'buffer'):
            return
        # Ping both servers now.
        rpc = xmlrpclib.Server('http://ping.blo.gs/')
        response = rpc.weblogUpdates.extendedPing(self._title, 
                    self._site, self._xml, self._xml)
        rpc = xmlrpclib.Server('http://rpc.weblogs.com/RPC2')
        response1 = rpc.weblogUpdates.ping(self._title, self._site)
        # save result of ping in self._file, note, no output is done
        self.__saveResults(pingTime, response, response1)

    def __saveResults(self, pingTime, response, response1):
        latest = (pingTime == 0 and 1 or self._latest)
        self.pingData = {'lastPing' : pingTime,
                         'response' : response,
                         'response1' : response1,
                         'latest' : latest}
        try:
            fp = file(self._file, 'w+b')
            pickle.dump(self.pingData, fp, 1)
            fp.close()
            return 1
        except IOError:
            # Something wrong with the file, abort.
            return 0

def load(py, entryList, renderer):
    weblogsPing(py, entryList).ping()
