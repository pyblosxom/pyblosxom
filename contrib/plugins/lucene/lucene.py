"""
Get a list containing the file names returned by a lucene search for a set of terms

You need the LuceneSearch.java and BlosxomIndexer.java in order to make this all work.

You'll need to edit JAVA_HOME, lucene, bindir, classpath and index
"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id$"

import glob, os, urllib, cgi
from libs import api

# location of Java
JAVA_HOME = '/usr/bin/java'
# location of lucene jar files
lucene = '/home/twl/pyblog/lib/lucene-1.2/*.jar'
# location of lucene scripts and Java .class files
bindir = '/home/twl/pyblog/bin'
# java Classpath
classpath = ':'.join(glob.glob(lucene)+[bindir])
# location of lucene index file
index = '/home/twl/pyblog/index'

def search(py, term):
    urllib.quote(term)
    results = os.popen(JAVA_HOME+' -cp '+classpath+' LuceneSearch '+index+' '+term,'r').readlines()
    results = [ os.path.join(py['datadir'], x[2:-1]) for x in results ]
    f = file("/tmp/lucene","w")
    for x in results:
        f.write(x)
    f.close()
    return results

def searchHandler(py):
    # Lucene search handling
    form = cgi.FieldStorage()
    if not form.has_key("q"):
        return None
    py['luceneResults'] = search(py, form["q"].value)
    return py['luceneResults']

def initialize():
    api.fileListHandler.register(searchHandler,api.FIRST)
