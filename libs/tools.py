# vim: tabstop=4 shiftwidth=4 expandtab
"""
Tools module

The swiss army knife for all things pyblosxom

@var month2num: A dict of literal months to its number format
@var num2month: A dict of number month format to its literal format
@var MONTHS: A list of valid literal and numeral months
"""
import plugins.__init__
import sgmllib, re, os, string,  types

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
for k,v in month2num.items():
    num2month[v] = k
    num2month[int(v)] = k

# all the valid month possibilities
MONTHS = num2month.keys() + month2num.keys()


class Stripper(sgmllib.SGMLParser):
    """
    Strips HTML
    
    An C{SGMLParser} subclass to strip away HTMLs
    """
    def __init__(self):
        self.data = []
        sgmllib.SGMLParser.__init__(self)
    def unknown_starttag(self, tag, attrs): self.data.append(" ")
    def unknown_endtag(self, tag): self.data.append(" ")
    def handle_data(self, data): self.data.append(data)
    def gettext(self):
        text = string.join(self.data, "")
        #return string.join(string.split(text)) # normalize whitespace
        return text # non - normalized whitespace


class Replacer:
    """
    Class for replacing variables in a template

    This class is a utility class used to provide a bound method to the
    C{re.sub()} function. Gotten from OPAGCGI
    """
    def __init__(self, dict):
        """
        It's only duty is to populate itself with the replacement dictionary
        passed.

        @param dict: The dict for variable substitution
        @type dict: dict
        """
        self.dict = dict

    def replace(self, matchobj):
        """
        The replacement method. 
        
        This is passed a match object by re.sub(), which it uses to index the
        replacement dictionary and find the replacement string.

        @param matchobj: A C{re} object containing substitutions
        @type matchobj: C{re}
        @returns: Substitutions
        @rtype: string
        """
        key = matchobj.group(1)
        if self.dict.has_key(key):
            r = self.dict[key]
            if type(r) != types.StringType and type(r) != types.UnicodeType:
                r = str(r)
            if type(r) != types.UnicodeType: 
                # convert strings to unicode, assumes strings in iso-8859-1
                r = unicode(r, 'iso-8859-1', 'replace')
            return r
        else:
            return u''

def parse(dict, template):
    """
    parse(dict) -> string
    
    This method parses the open file object passed, replacing any keys
    found using the replacement dictionary passed. Uses the L{Replacer} object.
    From OPAGCGI library

    @param dict: The name value pair list containing variable replacements
    @type dict: dict
    @param template: A template file with placeholders for variable replacements
    @type template: string
    @returns: Substituted template
    @rtype: string
    """
    replacer = Replacer(dict).replace
    replaced = u'' + re.sub(ur'(?<!\\)\$([A-Za-z0-9_\-]+)', replacer, template)
    return replaced


def Walk(root = '.', recurse = 0, pattern = '', return_folders = 0 ):
    """
    This function walks a directory tree starting at a specified root folder,
    and returns a list of all of the files (and optionally folders) that match
    our pattern(s). Taken from the online Python Cookbook and modified to own
    needs

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
    # initialize
    result = []

    # must have at least root folder
    try:
        names = os.listdir(root)
    except os.error:
        return result

    # expand pattern
    if not pattern:
        import libs.entryparsers.__init__
        libs.entryparsers.__init__.initialize_extensions()
        pattern = re.compile(r'.*\.(' + '|'.join(libs.entryparsers.__init__.ext) + r')$')

    #pattern = pattern or re.compile('.*\.txt$')
    pat_list = string.splitfields( pattern , ';' )
    
    # check each file
    for name in names:
        fullname = os.path.normpath(os.path.join(root, name))

        # grab if it matches our pattern and entry type
        for pat in pat_list:
            if pattern.match(name):
                if (os.path.isfile(fullname) and not return_folders) or (return_folders and os.path.isdir(fullname)):
                    result.append(fullname)
                break
                
        # recursively scan other folders, appending results
        if (recurse == 0) or (recurse > 1):
            if os.path.isdir(fullname) and not os.path.islink(fullname):
                result = result + Walk(fullname, 
                (recurse > 1 and recurse -  1 or 0), 
                pattern, return_folders)

    return result


def importName(modulename, name):
    """
    Module importer
    
    For modules that can only be determined during runtime

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


def sortDictBy(list, key):
    """
    Sort dict by a key

    Sorts a list of dicts with a specific key in the dict

    @param list: A list of dicts
    @type list: list

    @param key: The key in the list to sort with
    @type key: string

    @returns: A new list with sorted entries
    @rtype: list
    """
    nlist = map(lambda x, key=key: (x[key], x), list)
    nlist.sort()
    nlist.reverse()
    return map(lambda (key, x): x, nlist)


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
    import whrandom
    chars = string.letters + string.digits
    randStr = ""
    randStr_size = whrandom.randint(minlen, maxlen)
    for x in range(randStr_size):
        randStr += whrandom.choice(chars)
    return randStr


def run_blosxom_callback(chain, input):
    """
    Makes calling blosxom callbacks a bit easier since they all have the
    same mechanics.  This function merely calls run_callback with
    the arguments given and a mappingfunc.

    The mappingfunc copies the "template" value from the output to the 
    input for the next function.

    Refer to run_callback for more details.
    """
    return run_callback(chain, input, 
            lambda x,y: x.update({"template": y["template"]}))


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
        what we're doing.  If this function returns true (1) then
        we'll drop out of the loop.
    @type  donefunc: function

    @param defaultfunc: if this is set and we finish going through all
        the functions in the chain and none of them have returned something
        that satisfies the donefunc, then we'll execute the defaultfunc
        with the latest version of the input dict.
    @type  defaultfunc: function

    @returns: the transformed dict
    @rtype: dict
    """
    chain = plugins.__init__.get_callback_chain(chain)

    output = None

    for mem in chain:
        output = mem(input)
        if donefunc(output) == 1:
            break
        input = mappingfunc(input, output)

    if defaultfunc != None and callable(defaultfunc) and donefunc(output) != 1:
        return defaultfunc(input)
        
    return output



# These next few lines are to save a sort of run-time global registry
# of important things so that they're global to all the components
# of pyblosxom whether or not we actually pass them through.

my_registry = {}

def get_registry():
    """
    Returns the registry of run-time global things which really should
    be global to everything in the system.

    @returns: the run-time global registry of things
    @rtype: dict
    """
    return my_registry

def get_cache():
    """
    Retrieves the cache from the registry or fetches a new CacheDriver
    instance.

    @returns: A BlosxomCache object reference
    @rtype: L{libs.cache.base.BlosxomCacheBase} subclass
    """
    registry = get_registry()

    mycache = registry.get("cache", "")

    if not mycache:
        request = registry["request"]
        config = request.getConfiguration()

        cacheDriverConfig = config.get('cacheDriver', 'base')
        cacheConfig = config.get('cacheConfig', '')

        cache_driver = importName('libs.cache', cacheDriverConfig)
        mycache = cache_driver.BlosxomCache(cacheConfig)

        registry["cache"] = mycache

    return mycache
