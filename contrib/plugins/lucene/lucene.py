"""
Allow searching of the blog by using a Lucene search for a set of terms

To install:
1) Put lucene.py in pyblosxom/Pyblosxom/plugins
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
     <td><input type="text" id="search" name="search" size="18" maxlength="255" value="" /></td>
     <td><input type="submit" value=Search /></td>
    </tr>
   </table>
  </form>

   The action of the form should be the top level URI of your blog

9) You should add $searchHeader somewhere in the header of your webpage; this
   is where statements like, "Your search returned X results for Y" are
   placed. This statement is enclosed in a div tag with a class of 
   "searchtext" so that you can define it as you like in your stylesheet.

"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id$"

import glob, os, urllib
from Pyblosxom.entries import fileentry

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
    cmd =JAVA_HOME+' -cp '+classpath+' LuceneSearch '+index+' '+term
    pipe = os.popen(cmd,'r')
    results = pipe.readlines()
    status = pipe.close()
    results = [ os.path.join(config['datadir'], x[2:-1]) for x in results ]
    entries = [ makeEntry(x, config) for x in results]
    entries = [ ( x._mtime, x ) for x in entries ]
    entries.sort()
    entries.reverse()
    return [ x[1] for x in entries ]

def cb_prepare(args):
    """
    Add a nice header for the Lucene search, this header
    goes into the $searchHeader variable for including in
    the header template file.
    """
    # do nothing if the form is not a lucene form
    request = args["request"]
    form = request.getHttp()['form']
    if not form.has_key("search"):
        return None
                                                                                
    data = request.getData()

    resultnumber = len(data['luceneResults'])

    if resultnumber < 1:
	data['searchHeader'] = "<div class=\"searchtext\">Your search returned no results. Maybe I just never talk about <b>" + form["search"].value + "</b>. Try again.</div><div>"
    else:
	data['searchHeader'] = "<div class=\"searchtext\">Your search returned " + str(resultnumber) + " results for <b>" + form["search"].value + "</b>. They are below:</div>"

def cb_filelist(args):
    """
    Lucene search handling
    
    @param request: the Pyblosxom request
    @type request: a Pyblosxom request object
    """
    # do nothing if the form is not a lucene form
    request = args["request"]
    form = request.getHttp()['form']
    if not form.has_key("search"):
        return None
  
    config = request.getConfiguration()
    data = request.getData()
    
    data['luceneResults'] = search(config, form["search"].value)
    return data['luceneResults']
