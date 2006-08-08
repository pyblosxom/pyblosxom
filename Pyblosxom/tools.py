#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003, 2004, 2005, 2006 Wari Wahab
# 
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#
# $Id$
#######################################################################
"""
Tools module

The swiss army knife for all things pyblosxom

@var month2num: A dict of literal months to its number format
@var num2month: A dict of number month format to its literal format
@var MONTHS: A list of valid literal and numeral months
@var VAR_REGEXP: Regular expression for detection and substituion of variables
"""

__revision__ = "$Revision$"

# Python imports
import sgmllib
import re
import os
import time
import os.path
import sys
import urllib

try:
    from xml.sax.saxutils import escape
except ImportError:
    from cgi import escape


# Pyblosxom imports
import plugin_utils

month2num = { 'nil' : '00',
              'Jan' : '01',
              'Feb' : '02',
              'Mar' : '03',
              'Apr' : '04',
              'May' : '05',
              'Jun' : '06',
              'Jul' : '07',
              'Aug' : '08',
              'Sep' : '09',
              'Oct' : '10',
              'Nov' : '11',
              'Dec' : '12'}

# This is not python 2.1 compatible (Nifty though)
# num2month = dict(zip(month2num.itervalues(), month2num))
num2month = {}
for month_abbr, month_num in month2num.items():
    num2month[month_num] = month_abbr
    num2month[int(month_num)] = month_abbr

# all the valid month possibilities
MONTHS = num2month.keys() + month2num.keys()

# regular expression for detection and substituion of variables.
VAR_REGEXP = re.compile(ur'(?<!\\)\$((?:\w|\-|::\w)+(?:\(.*?(?<!\\)\))?)')


# reference to the pyblosxom config dict
_config = None

def initialize(config):
    """
    Initialize the tools module. This gives the module a chance to use 
    configuration from the pyblosxom config.py file.
    This should be called from Pyblosxom.pyblosxom.PyBlosxom.initialize.
    """
    global _config
    _config = config

def cleanup():
    """
    Cleanup the tools module.
    This should be called from Pyblosxom.pyblosxom.PyBlosxom.cleanup.
    """
    global _loghandler_registry
    # try:
    #     import logging
    #     if _use_custom_logger:
    #         raise ImportError, "whatever"
    # except ImportError:
    #     import _logging as logging

    try:
        logging.shutdown()
        _loghandler_registry = {}
    except ValueError:
        pass

QUOTES = {"'": "&apos;", '"': "&quot;"}

def escape_text(s):
    """
    Takes in a string and escapes ' to &apos; and " to &quot;.
    If s is None, then we return None.

    @param s: the input string to escape
    @type s: string

    @returns: the escaped string
    @rtype: string
    """
    if s == None:
        return None
    return escape(s, QUOTES)

def urlencode_text(s):
    """
    Calls urllib.quote on the string.  If is None, then we return
    None.

    @param s: the string to be urlencoded.
    @type s:  string

    @returns: the urlencoded string
    @rtype: string
    """
    if s == None:
        return None
    return urllib.quote(s)


class VariableDict:
    """
    Wraps around a standard dict allowing for escaped and urlencoding
    of internal data by tacking on a "_urlencoded" or a "_escaped"
    to the end of the key name.
    """
    def __init__(self):
        """
        Initializes the internal dict.
        """
        self._dict = {}

    def __getitem__(self, key, default=None):
        """
        If the key ends with "_escaped", then this will retrieve
        the value for the key and escape it.

        If the key ends with "_urlencoded", then this will retrieve
        the value for the key and urlencode it.

        Otherwise, this calls get(key, default) on the wrapped
        dict.

        @param key: the key to retrieve
        @type  key: string

        @param default: the default value to use if the key doesn't
                        exist.
        @type  default: string

        @returns: the value; escaped if the key ends in "_escaped";
                  urlencoded if the key ends in "_urlencoded".
        @rtype: string
        """
        if key.endswith("_escaped"):
            key = key[:-8]
            return escape_text(self._dict.get(key, default))

        if key.endswith("_urlencoded"):
            key = key[:-11]
            return urlencode_text(self._dict.get(key, default))

        return self._dict.get(key, default)

    def get(self, key, default=None):
        """
        This turns around and calls __getitem__(key, default).

        @param key: the key to retrieve
        @type  key: string

        @param default: the default value to use if the key doesn't exist.
        @type  default: string

        @returns: __getitem__(key, default)
        @rtype: string
        """
        return self.__getitem__(key, default)

    def __setitem__(self, key, value):
        """
        This calls __setitem__(key, value) on the wrapped dict.

        @param key: the key
        @type  key: string

        @param value: the value
        @type  value: string
        """
        self._dict.__setitem__(key, value)

    def update(self, newdict):
        """
        This calls update(newdict) on the wrapped dict.
        """
        self._dict.update(newdict)

    def has_key(self, key):
        """
        If the key ends with _encoded or _urlencoded, we strip that off
        and then check the wrapped dict to see if it has the adjusted key.

        Otherwise we call has_key(key) on the wrapped dict.

        @param key: the key to check for
        @type  key: string

        @returns: 1 if the key exists, 0 if not
        @rtype: boolean
        """
        if key.endswith("_encoded"):
            key = key[:-8]

        if key.endswith("_urlencoded"):
            key = key[:-11]

        return self._dict.has_key(key)

    def keys(self):
        """
        Returns a list of the keys that can be accessed through
        __getitem__.

        Note: this does not include the _encoded and _urlencoded
        versions of these keys.

        @returns: list of key names
        @rtype: list of varies
        """
        return self._dict.keys()

    def values(self):
        """
        Returns a list of the values in this dict.

        @returns: list of values
        @rtype: list of strings
        """
        return self._dict.values()

class Stripper(sgmllib.SGMLParser):
    """
    SGMLParser that removes HTML formatting code.
    """
    def __init__(self):
        """
        Initializes the instance.
        """
        self.data = []
        sgmllib.SGMLParser.__init__(self)

    def unknown_starttag(self, tag, attrs): 
        """
        Implements unknown_starttag.  Appends a " " to the buffer.
        """
        self.data.append(" ")

    def unknown_endtag(self, tag): 
        """
        Implements unknown_endtag.  Appends a " " to the buffer.
        """
        self.data.append(" ")

    def handle_data(self, data): 
        """
        Implements handle_data.  Appends data to the buffer.
        """
        self.data.append(data)

    def gettext(self): 
        """
        Returns the buffer.
        """
        return "".join(self.data)


class Replacer:
    """
    Class for replacing variables in a template

    This class is a utility class used to provide a bound method to the
    C{re.sub()} function.  Gotten from OPAGCGI.
    """
    def __init__(self, request, encoding, var_dict):
        """
        It's only duty is to populate itself with the replacement dictionary
        passed.

        @param request: the Request object
        @type  request: Request 

        @param encoding: the encoding to use
        @type  encoding: string

        @param var_dict: The dict for variable substitution
        @type var_dict: dict
        """
        self._request = request
        self._encoding = encoding
        self.var_dict = var_dict

    def replace(self, matchobj):
        """
        The replacement method. 
        
        This is passed a match object by re.sub(), which it uses to index the
        replacement dictionary and find the replacement string.

        @param matchobj: A C{re} object containing substitutions
        @type  matchobj: C{re} object

        @returns: Substitutions
        @rtype: string
        """
        request = self._request
        key = matchobj.group(1)

        if key.find("(") != -1 and key.find(")"):
            args = key[key.find("(")+1:key.rfind(")")]
            key = key[:key.find("(")]

        else:
            args = None

        if self.var_dict.has_key(key):
            r = self.var_dict[key]

            # if the value turns out to be a function, then we call it
            # with the args that we were passed.
            if callable(r):
                # FIXME - security issue here because we're using eval.
                # course, the things it allows us to do can be done using
                # plugins much more easily--so it's kind of a moot point.
                if args:
                    r = eval("r(request, " + args + ")")
                else:
                    r = r()

            if not isinstance(r, str) and not isinstance(r, unicode):
                r = str(r)

            if not isinstance(r, unicode):
                # convert strings to unicode, assumes strings in iso-8859-1
                r = unicode(r, self._encoding, 'replace')

            return r

        else:
            return u''

def parse(request, encoding, var_dict, template):
    """
    This method parses the open file object passed, replacing any keys
    found using the replacement dictionary passed.  Uses the L{Replacer} 
    object.  From OPAGCGI library

    @param request: the Request object
    @type  request: Request

    @param encoding: the encoding to use
    @type  encoding: string

    @param var_dict: The name value pair list containing variable replacements
    @type  var_dict: dict

    @param template: A template file with placeholders for variable 
        replacements
    @type  template: string

    @returns: Substituted template
    @rtype: string
    """
    if not isinstance(template, unicode):
        # convert strings to unicode, assumes strings in iso-8859-1
        template = unicode(template, encoding, 'replace')

    return u'' + VAR_REGEXP.sub(Replacer(request, encoding, var_dict).replace, 
                                template)


def Walk( request, root='.', recurse=0, pattern='', return_folders=0 ):
    """
    This function walks a directory tree starting at a specified root folder,
    and returns a list of all of the files (and optionally folders) that match
    our pattern(s). Taken from the online Python Cookbook and modified to own
    needs.

    It will look at the config "ignore_directories" for a list of 
    directories to ignore.  It uses a regexp that joins all the things
    you list.  So the following::

       config.py["ignore_directories"] = ["CVS", "dev/pyblosxom"]

    turns into the regexp::

       .*?(CVS|dev/pyblosxom)$

    It will also skip all directories that start with a period.

    @param request: the Request object
    @type  request: Request

    @param root: Starting point to walk from
    @type root: string

    @param recurse: Depth of recursion,
        - 0: All the way
        - 1: Just this level
        - I{n}: I{n} depth of recursion
    @type recurse: integer

    @param pattern: A C{re.compile}'d object
    @type pattern: object

    @param return_folders: If true, just return list of folders
    @type return_folders: boolean

    @returns: A list of file paths
    @rtype: list
    """
    # expand pattern
    if not pattern:
        ext = request.getData()['extensions']
        pattern = re.compile(r'.*\.(' + '|'.join(ext.keys()) + r')$')

    ignore = request.getConfiguration().get("ignore_directories", None)
    if isinstance(ignore, str):
        ignore = [ignore]

    if ignore:
        ignore = map(re.escape, ignore)
        ignorere = re.compile(r'.*?(' + '|'.join(ignore) + r')$')
    else:
        ignorere = None

    # must have at least root folder
    try:
        os.listdir(root)
    except os.error:
        return []

    return __walk_internal(root, recurse, pattern, ignorere, return_folders)

def __walk_internal( root, recurse, pattern, ignorere, return_folders ):
    """
    Note: This is an internal function--don't use it and don't expect it to
    stay the same between PyBlosxom releases.
    """
    # initialize
    result = []

    try:
        names = os.listdir(root)
    except:
        return []

    # check each file
    for name in names:
        fullname = os.path.normpath(os.path.join(root, name))

        # grab if it matches our pattern and entry type
        if pattern.match(name):
            if (os.path.isfile(fullname) and not return_folders) or \
                    (return_folders and os.path.isdir(fullname) and \
                    (not ignorere or not ignorere.match(fullname))):
                result.append(fullname)
                
        # recursively scan other folders, appending results
        if (recurse == 0) or (recurse > 1):
            if name[0] != "." and os.path.isdir(fullname) and \
                    not os.path.islink(fullname) and \
                    (not ignorere or not ignorere.match(fullname)):
                result = result + \
                         __walk_internal(fullname, 
                                        (recurse > 1 and recurse -  1 or 0), 
                                        pattern, ignorere, return_folders)

    return result


def filestat(request, filename):     
    """     
    Returns the filestat on a given file.  We store the filestat    
    in case we've already retrieved it this time.   
    
    @param request: the Pyblosxom Request object    
    @type  request: Request     
    
    @param filename: the name of the file to stat   
    @type  filename: string     
    
    @returns: the mtime of the file (same as returned by time.localtime(...))   
    @rtype: tuple of 9 ints     
    """     
    data = request.getData()    
    filestat_cache = data.setdefault("filestat_cache", {})      
    
    if filestat_cache.has_key(filename):    
        return filestat_cache[filename]     
    
    argdict = {"request": request, "filename": filename,    
               "mtime": os.stat(filename)}      
    argdict = run_callback("filestat",      
                           argdict,     
                           mappingfunc=lambda x,y:y,    
                           defaultfunc=lambda x:x)      
    timetuple = time.localtime(argdict["mtime"][8])     
    filestat_cache[filename] = timetuple    
     
    return timetuple


def what_ext(extensions, filepath):
    """
    Takes in a filepath and a list of extensions and tries them all until
    it finds the first extension that works.

    @param extensions: the list of extensions to test
    @type  extensions: list of strings

    @param filepath: the complete file path (minus the extension) to test
    @type  filepath: string

    @return: the extension that was successful or None
    @rtype: string
    """
    for ext in extensions:
        if os.path.isfile(filepath + '.' + ext):
            return ext
    return None


def is_year(checks):
    """
    Checks to see if the string is likely to be a year or not.  In order to 
    be considered to be a year, it must pass the following criteria:

      1. four digits
      2. first two digits are either 19 or 20.

    @param checks: the string to check for "year-hood"
    @type  checks: string

    @return: 1 if checks is likely to be a year or 0 if it is not
    @rtype: boolean
    """
    if not checks:
        return 0

    if len(checks) == 4 and checks.isdigit() and \
            (checks.startswith("19") or checks.startswith("20")):
        return 1
    return 0


def importname(modulename, name):
    """
    Imports modules for modules that can only be determined during 
    runtime.

    @param modulename: The base name of the module to import from
    @type modulename: string

    @param name: The name of the module to import from the modulename
    @type name: string

    @returns: If successful, returns an imported object reference, else C{None}
    @rtype: object
    """
    try:
        module = __import__(modulename, globals(), locals(), [name])
    except ImportError:
        return None
    try:
        return vars(module)[name]
    except:
        return None


def generateRandStr(minlen=5, maxlen=10):
    """
    Generate a random string
    
    Tool to generate a random string between C{minlen} to C{maxlen} characters

    @param minlen: The minimum length the string should be
    @type minlen: integer

    @param maxlen: The maximum length the string could be
    @type maxlen: integer

    @returns: A string containing random characters
    @rtype: string
    """
    import random, string
    chars = string.letters + string.digits
    randstr = []
    randstr_size = random.randint(minlen, maxlen)
    x = 0
    while x < randstr_size:
        randstr.append(random.choice(chars))
        x += 1
    return "".join(randstr)


def run_callback(chain, input, 
        mappingfunc=lambda x,y:x, 
        donefunc=lambda x:0,
        defaultfunc=None):
    """
    Executes a callback chain on a given piece of data.
    passed in is a dict of name/value pairs.  Consult the documentation
    for the specific callback chain you're executing.

    Callback chains should conform to their documented behavior.
    This function allows us to do transforms on data, handling data,
    and also callbacks.

    The difference in behavior is affected by the mappingfunc passed
    in which converts the output of a given function in the chain
    to the input for the next function.

    If this is confusing, read through the code for this function.

    @param chain: the callback chain to run
    @type  chain: string

    @param input: data is a dict filled with name/value pairs--refer
        to the callback chain documentation for what's in the data 
        dict.
    @type  input: dict

    @param mappingfunc: the function that maps output arguments
        to input arguments for the next iteration.  It must take
        two arguments: the original dict and the return from the
        previous function.  It defaults to returning the original
        dict.
    @type  mappingfunc: function

    @param donefunc: this function tests whether we're done doing
        what we're doing.  This function takes as input the output
        of the most recent iteration.  If this function returns 
        true (1) then we'll drop out of the loop.  For example,
        if you wanted a callback to stop running when one of the
        registered functions returned a 1, then you would pass in
        "donefunc=lambda x:x".
    @type  donefunc: function

    @param defaultfunc: if this is set and we finish going through all
        the functions in the chain and none of them have returned something
        that satisfies the donefunc, then we'll execute the defaultfunc
        with the latest version of the input dict.
    @type  defaultfunc: function

    @returns: the transformed dict
    @rtype: dict
    """
    chain = plugin_utils.get_callback_chain(chain)

    output = None

    for func in chain:
        # we call the function with the input dict it returns an output.
        output = func(input)

        # we fun the output through our donefunc to see if we should stop
        # iterating through the loop.  the donefunc should return a 1
        # if we're done--all other values cause us to continue.
        if donefunc(output) == 1:
            break

        # we pass the input we just used and the output we just got
        # into the mappingfunc which will give us the input for the
        # next iteration.  in most cases, this consists of either
        # returning the old input or the old output--depending on
        # whether we're transforming the data through the chain or not.
        input = mappingfunc(input, output)

    # if we have a defaultfunc and we haven't satisfied the donefunc
    # conditions, then we return whatever the defaultfunc returns
    # when given the current version of the input.
    if callable(defaultfunc) and donefunc(output) != 1:
        return defaultfunc(input)
        
    # we didn't call the defaultfunc--so we return the most recent
    # output.
    return output


def get_cache(request):
    """
    Retrieves the cache from the request or fetches a new CacheDriver
    instance.

    @param request: the Request object for this run
    @type  request: Request

    @returns: A BlosxomCache object reference
    @rtype: L{Pyblosxom.cache.base.BlosxomCacheBase} subclass
    """
    data = request.getData()
    mycache = data.get("data_cache", "")

    if not mycache:
        config = request.getConfiguration()

        cache_driver_config = config.get('cacheDriver', 'base')
        cache_config = config.get('cacheConfig', '')

        cache_driver = importname('Pyblosxom.cache', cache_driver_config)
        mycache = cache_driver.BlosxomCache(request, cache_config)

        data["data_cache"] = mycache

    return mycache


def update_static_entry(cdict, entry_filename):
    """
    This is a utility function that allows plugins to easily update
    statically rendered entries without going through all the rigamarole.

    First we figure out whether this blog is set up for static rendering.
    If not, then we return--no harm done.

    If we are, then we call render_url for each static_flavour of the entry
    and then for each static_flavour of the index page.

    @param cdict: the config.py dict
    @type  cdict: dict

    @param entry_filename: the filename of the entry (ex. /movies/xmen2)
    @type  entry_filename: string
    """
    staticdir = cdict.get("static_dir", "")

    if not staticdir:
        return

    staticflavours = cdict.get("static_flavours", ["html"])

    renderme = []
    for mem in staticflavours:
        renderme.append( "/index" + "." + mem, "" )
        renderme.append( entry_filename + "." + mem, "" )
    
    for mem in renderme:
        render_url(cdict, mem[0], mem[1])


def render_url(cdict, pathinfo, querystring=""):
    """
    Takes a url and a querystring and renders the page that corresponds
    with that by creating a Request and a PyBlosxom object and passing
    it through.

    @param cdict: the config.py dict
    @type  cdict: dict

    @param pathinfo: the path_info string.  ex: "/dev/pyblosxom/firstpost.html"
    @type  pathinfo: string

    @param querystring: the querystring (if any).  ex: "debug=yes"
    @type  querystring: string
    """
    staticdir = cdict.get("static_dir", "")

    # if there is no staticdir, then they're not set up for static
    # rendering.
    if not staticdir:
        raise Exception("You must set static_dir in your config file.")

    from pyblosxom import PyBlosxom

    env = {
        "HTTP_USER_AGENT": "static renderer",
        "REQUEST_METHOD": "GET",
        "HTTP_HOST": "localhost",
        "PATH_INFO": pathinfo,
        "QUERY_STRING": querystring,
        "REQUEST_URI": pathinfo + "?" + querystring,
        "PATH_INFO": pathinfo,
        "HTTP_REFERER": "",
        "REMOTE_ADDR": "",
        "SCRIPT_NAME": "",
        "wsgi.errors": sys.stderr,
        "wsgi.input": None
    }
    data = {"STATIC": 1}
    p = PyBlosxom(cdict, env, data)
    p.run(static=True)
    response = p.getResponse()
    response.seek(0)

    fn = os.path.normpath(staticdir + os.sep + pathinfo)
    if not os.path.isdir(os.path.dirname(fn)):
        os.makedirs(os.path.dirname(fn))

    # by using the response object the cheesy part of removing 
    # the HTTP headers from the file is history.
    f = open(fn, "w")
    f.write(response.read())
    f.close()




#******************************
# Logging
#******************************

# If you have Python >=2.3 and want to use/test the custom logging 
# implementation set this flag to True.
_use_custom_logger = False

try:
    import logging
    if _use_custom_logger:
        raise ImportError, "whatever"
except ImportError:
    import _logging as logging

# A dict to keep track of created log handlers.
# Used to prevent multiple handlers from beeing added to the same logger.
_loghandler_registry = {}


class LogFilter(object):
    """
    Filters out messages from log-channels that are not listed in the
    log_filter config variable.
    """
    def __init__(self, names=None):
        """
        Initializes the filter to the list provided by the names
        argument (or [] if names is None).

        @param names: list of name strings to filter out
        @type  names: list of strings
        """
        if names == None:
            names = []
        self.names = names

    def filter(self, record):
        if record.name in self.names:
            return 1
        return 0

def getLogger(log_file=None):
    """
    Creates and retuns a log channel.
    If no log_file is given the system-wide logfile as defined in config.py
    is used. If a log_file is given that's where the created logger logs to.

    @param log_file: optional, the file to log to.
    @type log_file: C{str}

    @return: a log channel (Logger instance)
    @rtype: L{logging.Logger} for Python >=2.3, 
            L{Pyblosxom._logging.Logger} for Python <2.3
    """
    custom_log_file = False
    if log_file == None:
        log_file = _config.get('log_file', 'stderr')
        f = sys._getframe(1)
        filename = f.f_code.co_filename
        module = f.f_globals["__name__"]
        # by default use the root logger
        log_name = ""
        for path in _config.get('plugin_dirs', []):
            if filename.startswith(path):
                # if it's a plugin, use the module name as the log channels 
                # name
                log_name = module
                break
        # default to log level WARNING if it's not defined in config.py
        log_level = _config.get('log_level', 'warning')
    else:
        # handle custom log_file
        custom_log_file = True
        # figure out a name for the log channel
        log_name = os.path.splitext(os.path.basename(log_file))[0]
        # assume log_level debug (show everything)
        log_level = "debug"

    global _loghandler_registry

    # get the logger for this channel
    logger = logging.getLogger(log_name)
    # don't propagate messages up the logger hierarchy
    logger.propagate = 0

    # setup the handler if it doesn't allready exist.
    # only add one handler per log channel.
    key = "%s|%s" % (log_file, log_name)
    if not key in _loghandler_registry:

        # create the handler
        if log_file == "stderr":
            hdlr = logging.StreamHandler(sys.stderr)
        else:
            if log_file == "NONE": # user disabled logging
                if os.name == 'nt': # windoze
                    log_file = "NUL"
                else: # assume *nix
                    log_file = "/dev/null"
            try:
                hdlr = logging.FileHandler(log_file)
            except IOError:
                # couldn't open logfile, fallback to stderr
                hdlr = logging.StreamHandler(sys.stderr)

        # create and set the formatter
        if log_name:
            fmtr_s = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        else: # root logger
            fmtr_s = '%(asctime)s [%(levelname)s]: %(message)s'

        hdlr.setFormatter(logging.Formatter(fmtr_s))

        logger.addHandler(hdlr)
        int_level = getattr(logging, log_level.upper())
        logger.setLevel(int_level)

        if not custom_log_file:
            # only log messages from plugins listed in log_filter.
            # add 'root' to the log_filter list to still allow application 
            # level messages.
            log_filter = _config.get('log_filter', None)
            if log_filter:
                lfilter = LogFilter(log_filter)
                logger.addFilter(lfilter)

        # remember that we've seen this handler
        _loghandler_registry[key] = True

    return logger


def log_exception(log_file=None):
    """
    Logs an exception to the given file.
    Uses the system-wide log_file as defined in config.py if none 
    is given here.

    @param log_file: optional, the file to log to
    @type log_file: C{str}
    """
    log = getLogger(log_file)
    log.exception("Exception occured:")


def log_caller(frame_num=1, log_file=None):
    """
    Logs some info about the calling function/method.
    Useful for debugging.

    Usage:
        import tools
        tools.log_caller() # logs frame 1
        tools.log_caller(2)
        tools.log_caller(3, log_file="/path/to/file")

    @param frame_num: optional, index of the frame
    @type frame_num: C{int}

    @param log_file: optional, the file to log to
    @type log_file: C{str}
    """
    f = sys._getframe(frame_num)
    module = f.f_globals["__name__"]
    filename = f.f_code.co_filename
    line = f.f_lineno
    subr = f.f_code.co_name

    log = getLogger(log_file)
    log.info("\n  module: %s\n  filename: %s\n  line: %s\n  subroutine: %s", 
        module, filename, line, subr)



# %<-------------------------
# BEGIN portalocking block from Python Cookbook.
# LICENSE is located in docs/LICENSE.portalocker.
# It's been modified for use in Pyblosxom.

# """Cross-platform (posix/nt) API for flock-style file locking.
# 
# Synopsis:
# 
#    import portalocker
#    file = open("somefile", "r+")
#    portalocker.lock(file, portalocker.LOCK_EX)
#    file.seek(12)
#    file.write("foo")
#    file.close()
# 
# If you know what you're doing, you may choose to
# 
#    portalocker.unlock(file)
# 
# before closing the file, but why?
# 
# Methods:
# 
#    lock( file, flags )
#    unlock( file )
# 
# Constants:
# 
#    LOCK_EX
#    LOCK_SH
#    LOCK_NB
# 
# I learned the win32 technique for locking files from sample code
# provided by John Nielsen <nielsenjf@my-deja.com> in the documentation
# that accompanies the win32 modules.
# 
# Author: Jonathan Feinberg <jdf@pobox.com>
# Version: $Id$

if os.name == 'nt':
    import win32con
    import win32file
    import pywintypes
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0 # the default
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    # is there any reason not to reuse the following structure?
    __overlapped = pywintypes.OVERLAPPED()
elif os.name == 'posix':
    import fcntl
    LOCK_EX = fcntl.LOCK_EX
    LOCK_SH = fcntl.LOCK_SH
    LOCK_NB = fcntl.LOCK_NB
else:
    raise RuntimeError("PortaLocker only defined for nt and posix platforms")

if os.name == 'nt':
    def lock(f, flags):
        hfile = win32file._get_osfhandle(f.fileno())
        win32file.LockFileEx(hfile, flags, 0, 0xffff0000, __overlapped)

    def unlock(f):
        hfile = win32file._get_osfhandle(f.fileno())
        win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)

elif os.name =='posix':
    def lock(f, flags):
        fcntl.flock(f.fileno(), flags)

    def unlock(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

# END portalocking block from Python Cookbook.
# %<-------------------------
