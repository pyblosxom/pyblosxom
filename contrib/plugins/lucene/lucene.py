"""
Get a list containing the file names returned by a lucene search for a set of terms

You need the LuceneSearch.java and BlosxomIndexer.java in order to make this all work.

You'll need to edit JAVA_HOME, lucene, bindir, classpath and index
"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id$"

import glob, os, urllib
from libs import api
from libs.entries import fileentry

# TODO - move these to config

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

def makeEntry(filename,config):
    """
    @param filename: filename of matching entry
    @type  filename: string
        
    @param config: a pyblosxom config dict
    @type  config: a dict
    """
    return fileentry.FileEntry(config, filename, config['datadir'])                                              
def search(config, term):
    """
    Search for the specified search term
    
    @param config: a pyblosxom config dict
    @type config:  a dict
        
    @param term: the search term
    @type term: a string
    """
    urllib.quote(term)
    results = os.popen(JAVA_HOME+' -cp '+classpath+' LuceneSearch '+index+' '+term,'r').readlines()
    results = [ os.path.join(config['datadir'], x[2:-1]) for x in results ]
    f = file("/tmp/lucene","w")
    for x in results:
        f.write(x)
    f.close()
    return [ makeEntry(x, config) for x in results]

def searchHandler(request):
    """
    Lucene search handling
    
    @param request: the Pyblosxom request
    @type request: a Pyblosxom request object
    """
    # do nothing if the form is not a lucene form
    form = request.getHttp()['form']
    if not form.has_key("q"):
        return None
  
    config = request.getConfiguration()
    data = request.getData()
    
    data['luceneResults'] = search(config, form["q"].value)
    return data['luceneResults']

def initialize():
    """
    Call back chain initialization
    """
    api.fileListHandler.register(searchHandler,api.FIRST)
