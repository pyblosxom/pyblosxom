"""
options for config.py:

if py['xmlrpc_metaweblog_ping'] == 'True' then autoping will be invoked to
generate trackbacks and pingbacks

Implements the metaWeblog XML-RPC interface.
See spec here: http://www.xmlrpc.com/metaWeblogApi

Implemented methods:
  - metaWeblog.newPost
  - metaWeblog.editPost
  - metaWeblog.getPost
  - metaWeblog.getCategories
  - metaWeblog.getRecentPosts

"""
import os, xmlrpclib, re, time
from Pyblosxom import tools, plugin_utils
from Pyblosxom.entries.fileentry import FileEntry

tools.make_logger('/tmp/metaweblog.log')

#
# Pyblosxom callback API functions
#
    
def verify_installation(request):
    config = request.getConfiguration()
    retval = 1

    # all config properties are optional
    if not config.has_key('xmlrpc_metaweblog_ping'):
        print("missing optional property: 'xmlrpc_metaweblog_ping'")

    return retval

def cb_xmlrpc_register(args):
    """
    Binds the methods that we handle with the function instances.
    Part of the pyblosxom callback api

    @param args: the callback arguments
    @type args: dict
    """
    args["methods"].update( 
            {'metaWeblog.newPost':metaWeblog_newPost,
             'metaWeblog.editPost':metaWeblog_editPost,
             'metaWeblog.getPost':metaWeblog_getPost,
             'metaWeblog.newMediaObject':metaWeblog_newMediaObject,
             'metaWeblog.getCategories':metaWeblog_getCategories,
             'metaWeblog.getRecentPosts':metaWeblog_getRecentPosts})
    
    return args

def authenticate(request, username, password):
    """
    Handles authentication.  This works by getting the xmlrpc dispatcher
    plugin Python module and then calling authenticate on that.

    @param request: the pyblosxom Request instance
    @type  request: Request

    @param username: the username
    @type  username: string

    @param password: the password
    @type  password: string
    """
    xmlrpc_plugin = plugin_utils.get_plugin_by_name("xmlrpc")
    xmlrpc_plugin.authenticate(request, username, password)

#
# metaWeblog API functions
#

def metaWeblog_editPost(request, postid, username, password, struct, publish):
    """
    Edit an existing post
    Part of the metaWeblog API

    @param request: the pyblosxom Request instance
    @type  request: Request

    @param username: the username
    @type  username: string

    @param password: the password
    @type  password: string

    @param struct: the metaWeblog api struct
    @type  struct: dict

    @param publish: to publish (true) or not
    @type  publish: boolean

    @returns an xmlrpclib boolean -- true if the edit was successful, false otherwise
    """
    tools.log("editPost %s %s %s" % (postid, struct, publish))
    authenticate(request, username, password)
    config = request.getConfiguration()
    ping = config.get('xmlrpc_metaweblog_ping',0)

    return xmlrpclib.Boolean(_writePost(config, username, postid, struct, publish, ping))

def metaWeblog_newPost(request, blogid, username, password, struct, publish):
    """
    Create a new entry on the server
    Part of the metaWeblog API

    if py['xmlrpc_metaweblog_ping'] == 'True' then autoping will be invoked to
    generate trackbacks and pingbacks

    @param request: the pyblosxom Request instance
    @type  request: Request

    @param username: the username
    @type  username: string

    @param password: the password
    @type  password: string

    @param struct: the metaWeblog API struct
    @type  struct: dict

    @param publish: to publish (true) or not
    @type  publish: boolean
    """
    tools.log("newPost %s %s %s" % (blogid, struct, publish))
    authenticate(request, username, password)
    config = request.getConfiguration()
    ping = config.get('xmlrpc_metaweblog_ping',0)

    postId = _buildPostId(request, blogid, struct)
    result = _writePost(config, username, postId, struct, publish, ping)
    
    if result:
        return postId
    else:
        return xmlrpclib.Boolean(False)

    
def metaWeblog_getPost(request, postid, username, password):
    """
    Get a single post from the server
    Part of the metaWeblog API

    @param request: the pyblosxom Request instance
    @type  request: Request

    @param postid: the id of the post
    @type postid: string

    @param username: the username
    @type  username: string

    @param password: the password
    @type  password: string

    @returns the post whose id is postid
    @rtype dict
    """
    tools.log("getPost: postid: %s" % (postid,))
    authenticate(request, username, password)
    config = request.getConfiguration()

    tools.log("datadir = %s, file = %s.txt" % (config['datadir'], postid))
    entry = FileEntry(request, os.path.join(config['datadir'],"%s.txt" % postid), config['datadir'])
    post = { 'permaLink': "%s/%s/%s/%s#%s" % (config['base_url'], entry['yr'],entry['mo_num'],entry['da'],entry['fn']),
             'title':entry['title'],
             'description':entry['body'], 
             'postid':re.sub(r'^/', '', "%s/%s"% (entry['absolute_path'], entry['fn'])),
             'categories':[entry['absolute_path']],
             'dateCreated':xmlrpclib.DateTime(entry['w3cdate']) }
    return post

def metaWeblog_getCategories(request, blogid, username, password):
    """
    Get the available categories
    Part of the metaWeblog API

    @param request: the pyblosxom Request instance
    @type  request: Request

    @param blogid: the id of the blog
    @type blogid: string

    @param username: the username
    @type  username: string

    @param password: the password
    @type  password: string

    @returns list of categories (each category is a string)
    @rtype list
    """
    tools.log("getCategories blogid: %s" % blogid)
    authenticate(request, username, password)
    config = request.getConfiguration()

    clist = _getCategories(request)

    return clist

def metaWeblog_getRecentPosts(request, blogid, username, password, numberOfPosts):
    """
    Get the most recent posts
    Part of the metaWeblog API

    @param request: the pyblosxom Request instance
    @type  request: Request

    @param blogid: the id of the blog
    @type blogid: string

    @param username: the username
    @type  username: string

    @param password: the password
    @type  password: string

    @param numberOfPosts: the number of posts to retreive
    @type  numberOfPosts: int

    @returns list of dicts, one per post
    @rtype list
    """
    tools.log("getRecentPosts blogid:%s count:%s" % (blogid, numberOfPosts))
    authenticate(request, username, password)
    config = request.getConfiguration()

    filelist = tools.Walk(request, config['datadir'], int(config['depth']), pattern=_allEntriesPattern(request))

    entryList = []
    for f in filelist:
        entry = FileEntry(request, f, config['datadir'])
        entryList.append((entry._mtime, entry))
    entryList.sort()
    entryList.reverse()
    try:
        numberOfPosts = int(numberOfPosts)
    except:
        tools.log("Couldn't convert numberOfPosts")
        numberOfPosts = 5
    entryList = [ x[1] for x in entryList ][: numberOfPosts]

    posts = [ { 'permaLink': "%s/%s/%s/%s#%s" % (config['base_url'], x['yr'],x['mo_num'],x['da'],x['fn']),
                'title':x['title'],
                'description':x['body'], 
                'postid':re.sub(r'^/', '', "%s/%s"% (x['absolute_path'], x['fn'])),
                'categories':[x['absolute_path']],
                'dateCreated':xmlrpclib.DateTime(x['w3cdate']) }  for x in entryList ]

    return posts

def metaWeblog_newMediaObject(request, blogid, username, password, struct):
    """
    Create a new media object
    Part of the metaWeblog API

    @param request: the pyblosxom Request instance
    @type  request: Request

    @param blogid: the id of the blog
    @type blogid: string

    @param username: the username
    @type  username: string

    @param password: the password
    @type  password: string

    @param struct: the metaWeblog API struct
    @type  struct: dict
    """
    tools.log("newMediaObject: ", struct)
    pass

#
# helper functions
#
def _allEntriesPattern(request):
    """
    Return a regular expression pattern that includes all valid entry
    extensions and their unpublished (suffexed with '-') versions.  This
    allows these entries to be displayed in getRecentPosts, and to be counted
    in _getEntryCount()

    @param request: the HTTP Request
    @type request: Request

    @returns a regular expression pattern
    @rtype string
    """
    # make sure to count file with extensions ending in -
    ext = request.getData()['extensions']
    pats = list(ext.keys()) # copy it
    for p in ext.keys():
        pats.append(p+"-")
    entryPattern = re.compile(r'.*\.(' + '|'.join(pats) + r')$')

    return entryPattern

def _buildPostId(request, blogid, struct):
    """
    Construct the id for the post

    The algorithm used for constructing the post id is to concatenate the
    pyblosxom category (directory path, with the datadir prefix removed) with
    the count of entries.  This means that postids are increasing integers.

    @param request: the HTTP Request
    @type request: Request

    @param blogid: the id of the blog
    @type blogid: string

    @param struct: the metaWeblog API struct
    @type struct: dict

    @return the post id
    @rtype string
    """
    config = request.getConfiguration()

    category = ''
    try:
        category = struct['categories'][0]
    except:
        pass

    count = _getEntryCount(request)

    if not category == '':
        postId = os.path.join(structCategories[0], "%d" % count)
    else:
        postId = os.path.join("%d" % count)

    return postId

def _getEntryCount(request):
    """
    Return a count of the number of published and unpublished
    (suffixed with '-') entries

    @param request: the HTTP Request
    @type request: Request

    @return the number of published an unpublished entries
    @rtype int
    """
    config = request.getConfiguration()
    root = config['datadir']

    elist = tools.Walk(request, root, pattern=_allEntriesPattern(request))
    elist = [mem[len(root)+1:] for mem in elist]
    
    elistmap = {}
    for mem in elist:
        mem = os.path.dirname(mem)
        elistmap[mem] = 1 + elistmap.get(mem, 0)
        mem = mem.split(os.sep)
    return len(elist)

def _getCategories(request):
    """
    Return a list of all the categories in this pyblosxom blog,
    excluding CVS and comments directories, but including category directories
    which have no entries (newly created categories)

    @param request: the HTTP Request
    @type request: Request

    @return a list of the available categories
    @rtype list
    """
    # now make a list of all the categories
    # bypass tools.walk in order to pickup empty categories
    config = request.getConfiguration()
    root = config['datadir']

    def walk_filter(arg, dirname, files):
        if dirname==root:
            return
        if not dirname.endswith('CVS') and not dirname.startswith(root+'/comments'):
            arg.append(dirname.replace(root+'/',''))

    clist = []
    os.path.walk(root, walk_filter, clist)
    clist.append("")
    clist.sort()                   

    return clist

def _writePost(config, username, postid, struct, publish=True, ping=False):    
    """
    Write a post file into pyblosxom

    @param config: the pyblosxom configuration
    @type config: config

    @param username: the username of the poster
    @type username: string

    @param postid: the id of the post to be written
    @type postid: string

    @param struct: the metaWeblog API struct
    @type struct: dict

    @param publish: to publish (true) or not
    @type publish: boolean

    @param ping: whether or not to invoke autoping (true) or not
    @type ping: boolean
    """
    root = config['datadir']
    path = os.path.join(root,"%s.txt" % postid)
    tools.log("path = "+path)
    if not publish:
        path += '-'

    content = "%s\n#author %s\n%s" % (struct['title'], username, struct['description'])

    try:
        atime, mtime = (0, 0)
        if os.path.isfile(path):
            atime, mtime = os.stat(path)[7:9]
        if struct.has_key('dateCreated'):
            mtime = time.mktime(time.strptime(struct['dateCreated'], '%Y%m%dT%H:%M:%S'))

        f = open(path,'w')
        f.write(content)
        f.close()

        if atime != 0 and mtime != 0:
            try:
                os.utime(path, (atime, mtime))
            except:
                pass
    except: 
        if f is not None:
            f.close()
        return 0
    if ping:
        try:
            os.chdir(root)
            autoping.autoping("%s.txt" % postid)
        except:
            tools.log("autoping failed for %s" % path)
    return 1
