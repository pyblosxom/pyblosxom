import sgmllib, re, os, string
import api

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

class Stripper(sgmllib.SGMLParser):
    """Strips HTML"""
    def __init__(self):
        self.data = []
        sgmllib.SGMLParser.__init__(self)
    def unknown_starttag(self, tag, attrib): self.data.append(" ")
    def unknown_endtag(self, tag): self.data.append(" ")
    def handle_data(self, data): self.data.append(data)
    def gettext(self):
        text = string.join(self.data, "")
        #return string.join(string.split(text)) # normalize whitespace
        return text # non - normalized whitespace
    
class Replacer:
    """This class is a utility class used to provide a bound method to the
    re.sub() function. Gotten from OPAGCGI"""
    def __init__(self, dict):
        """The constructor. It's only duty is to populate itself with the
        replacement dictionary passed."""
        self.dict = dict

    def replace(self, matchobj):
        """The replacement method. This is passed a match object by re.sub(),
        which it uses to index the replacement dictionary and find the
        replacement string."""
        key = matchobj.group(1)
        if self.dict.has_key(key):
            return str(self.dict[key])
        else:
            return ''

def parse(dict, template):
    """parse(dict) -> string
    This method parses the open file object passed, replacing any keys
    found using the replacement dictionary passed. From OPAGCGI library"""
    replacer = Replacer(dict).replace
    replaced = '' + re.sub(r'(?<!\\)\$([A-Za-z0-9_\-]+)', replacer, template)
    return replaced


def parseitem(entry_dict, text_string):
    """
    Takes in an entry dict and a text string and passes it through the 
    parseitem CallbackChain, allowing plugins to expand variables they 
    know about.

    This calls the chain with (entry_dict, text_string) and returns
    the final string.
    """
    return api.parseitem.executeChain((entry_dict, text_string))[1]

def filestat(filename):
    """
    Calls the api's filestat callback chain to figure out what the
    stats on a given file are.  

    This calls the chain with (filename, os.stat(filename)) and returns
    just the os.stats-type tuple.
    """
    return api.filestat.executeChain((filename, os.stat(filename)))[1]

def logRequest(filename = '', returnCode = '200'):
    """
    Calls the api's logRequest callback chain to do some statistical analysis
    based on the current request.

    This calls the chain with (filename, returnCode) and returns None
    """
    api.logRequest.executeChain((filename, returnCode))

def Walk(root = '.', 
         recurse = 0, 
         pattern = re.compile(r'.*\.txt$'), 
         return_folders = 0 ):
    """
    This function walks a directory tree starting at a specified root folder,
    and returns a list of all of the files (and optionally folders) that match
    our pattern(s). Taken from the online Python Cookbook and modified to own
    needs
    """
    # initialize
    result = []

    # must have at least root folder
    try:
        names = os.listdir(root)
    except os.error:
        return result

    # expand pattern
    pattern = pattern or '*'
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
    """Module importer, for modules that can only be determined during runtime"""
    try:
        module = __import__(modulename, globals(), locals(), [name])
    except ImportError:
        return None
    try:
        return vars(module)[name]
    except:
        return None


def sortDictBy(list, key):
    nlist = map(lambda x, key=key: (x[key], x), list)
    nlist.sort()
    nlist.reverse()
    return map(lambda (key, x): x, nlist)


def generateRandStr(minlen=5, maxlen=10):
    import whrandom
    chars = string.letters + string.digits
    randStr = ""
    randStr_size = whrandom.randint(minlen, maxlen)
    for x in range(randStr_size):
        randStr += whrandom.choice(chars)
    return randStr
