"""
Allow searching of the blog by using a Lucene search for a set of terms

To install:
1) Put lucene.py in pyblosxom/libs/plugins
2) In config.py add lucene to py['load_plugins']
3) Place the contents of pyblosxom/contrib/plugins/lucene/bin in a
   directory readable by pybloxsom.  In config.py, set py['lucene_bin'] to
   this path
4) Download lucene from http://jakarta.apache.org/lucene and unzip/untar it.
   In config.py, set py['lucene_home'] to the lucene directory (which contains
   lucene-1.2.jar and lucene-demos-1.2.jar)
5) In config.py set py['lucene_index'] to the name of the Lucene index file
   (pybosxom must be able to read and write this file)
6) In config.py set py['JAVA_HOME'] to point at the 'java' command
7) Set up a cron job to run py['lucene_bin']/index.sh periodically to
   reindex your blog
8) Somewhere in your web page you need a lucene search form:

  <form id="searchform" method="get" action="/blog">
   <table>
    <tr>
     <td><input type="text" id="q" name="q" size="18" maxlength="255" value="" /></td>
     <td><input type="submit" value=Search /></td>
    </tr>
   </table>
  </form>

  The action of the form should be the top level URI of your blog
"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id$"

import glob, os, urllib
from libs.entries import fileentry

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
    JAVA_HOME=config['JAVA_HOME']
    classpath = ':'.join(glob.glob(config['lucene_home']+'/*.jar')+[config['lucene_bin']])
    index = config['lucene_index']
    results = os.popen(JAVA_HOME+' -cp '+classpath+' LuceneSearch '+index+' '+term,'r').readlines()
    results = [ os.path.join(config['datadir'], x[2:-1]) for x in results ]
    return [ makeEntry(x, config) for x in results]

def cb_filelist(args):
    """
    Lucene search handling
    
    @param request: the Pyblosxom request
    @type request: a Pyblosxom request object
    """
    # do nothing if the form is not a lucene form
    request = args["request"]
    form = request.getHttp()['form']
    if not form.has_key("q"):
        return None
  
    config = request.getConfiguration()
    data = request.getData()
    
    data['luceneResults'] = search(config, form["q"].value)
    return data['luceneResults']

