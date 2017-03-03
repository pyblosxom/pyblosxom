#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""Utility module for functions that are useful to Pyblosxom and plugins.
"""

from html.parser import HTMLParser
import re
import os
import time
import os.path
import stat
import sys
import locale
import urllib.request, urllib.parse, urllib.error
import inspect
import textwrap

# Pyblosxom imports
from Pyblosxom import plugin_utils

# Note: month names tend to differ with locale

# month name (Jan) to number (1)
month2num = None
# month number (1) to name (Jan)
num2month = None
# list of all month numbers and names
MONTHS    = None

# regular expression for detection and substituion of variables.
_VAR_REGEXP = re.compile(r"""
    (?<!\\)   # if the $ is escaped, then this isn't a variable
    \$        # variables start with a $
    (
        (?:\w|\-|::\w)+       # word char, - or :: followed by a word char
        (?:
            \(                # an open paren
            .*?               # followed by non-greedy bunch of stuff
            (?<!\\)\)         # with an end paren that's not escaped
        )?    # 0 or 1 of these ( ... ) blocks
    |
        \(
        (?:\w|\-|::\w)+       # word char, - or :: followed by a word char
        (?:
            \(                # an open paren
            .*?               # followed by non-greedy bunch of stuff
            (?<!\\)\)         # with an end paren that's not escaped
        )?    # 0 or 1 of these ( ... ) blocks
        \)
    )
    """, re.VERBOSE)

# reference to the pyblosxom config dict
_config = {}


def initialize(config):
    """Initializes the tools module.

    This gives the module a chance to use configuration from the
    pyblosxom config.py file.

    This should be called from ``Pyblosxom.pyblosxom.Pyblosxom.initialize``.
    """
    global _config
    _config = config

    # Month names tend to differ with locale
    global month2num

    try:
        month2num = {'nil': '00',
                     locale.nl_langinfo(locale.ABMON_1): '01',
                     locale.nl_langinfo(locale.ABMON_2): '02',
                     locale.nl_langinfo(locale.ABMON_3): '03',
                     locale.nl_langinfo(locale.ABMON_4): '04',
                     locale.nl_langinfo(locale.ABMON_5): '05',
                     locale.nl_langinfo(locale.ABMON_6): '06',
                     locale.nl_langinfo(locale.ABMON_7): '07',
                     locale.nl_langinfo(locale.ABMON_8): '08',
                     locale.nl_langinfo(locale.ABMON_9): '09',
                     locale.nl_langinfo(locale.ABMON_10): '10',
                     locale.nl_langinfo(locale.ABMON_11): '11',
                     locale.nl_langinfo(locale.ABMON_12): '12'}

    except AttributeError:
        # Windows doesn't have nl_langinfo, so we use one that
        # only return English.
        # FIXME - need a better hack for this issue.
        month2num = {'nil': '00',
                     "Jan": '01',
                     "Feb": '02',
                     "Mar": '03',
                     "Apr": '04',
                     "May": '05',
                     "Jun": '06',
                     "Jul": '07',
                     "Aug": '08',
                     "Sep": '09',
                     "Oct": '10',
                     "Nov": '11',
                     "Dec": '12'}

    # This is not python 2.1 compatible (Nifty though)
    # num2month = dict(zip(month2num.itervalues(), month2num))
    global num2month
    num2month = {}
    for month_abbr, month_num in list(month2num.items()):
        num2month[month_num] = month_abbr
        num2month[int(month_num)] = month_abbr

    # all the valid month possibilities
    global MONTHS
    MONTHS = list(num2month.keys()) + list(month2num.keys())


def pwrap(s):
    """Wraps the text and prints it.
    """
    starter = ""
    linesep = os.linesep
    if s.startswith("- "):
        starter = "- "
        s = s[2:]
        linesep = os.linesep + "  "

    print(starter + linesep.join(textwrap.wrap(s, 72)))


def pwrap_error(s):
    """Wraps an error message and prints it to stderr.
    """
    starter = ""
    linesep = os.linesep
    if s.startswith("- "):
        starter = "- "
        s = s[2:]
        linesep = os.linesep + "  "

    sys.stderr.write(starter + linesep.join(textwrap.wrap(s, 72)) + "\n")


def deprecated_function(func):
    def _deprecated_function(*args, **kwargs):
        return func(*args, **kwargs)

    _deprecated_function.__doc__ = ("DEPRECATED.  Use %s instead." %
                                    func.__name__)
    _deprecated_function.__dict__.update(func.__dict__)
    return _deprecated_function


class ConfigSyntaxErrorException(Exception):
    """Thrown when ``convert_configini_values`` encounters a syntax
    error.
    """
    pass


def convert_configini_values(configini):
    """Takes a dict containing config.ini style keys and values, converts
    the values, and returns a new config dict.

    :param confini: dict containing the config.ini style keys and values

    :raises ConfigSyntaxErrorException: when there's a syntax error

    :returns: new config dict
    """
    def s_or_i(text):
        """
        Takes a string and if it begins with \" or \' and ends with
        \" or \', then it returns the string.  If it's an int, returns
        the int.  Otherwise it returns the text.
        """
        text = text.strip()
        if (((text.startswith('"') and not text.endswith('"'))
             or (not text.startswith('"') and text.endswith('"')))):
            raise ConfigSyntaxErrorException(
                "config syntax error: string '%s' missing start or end \"" %
                text)
        elif (((text.startswith("'") and not text.endswith("'"))
               or (not text.startswith("'") and text.endswith("'")))):
            raise ConfigSyntaxErrorException(
                "config syntax error: string '%s' missing start or end '" %
                text)
        elif text.startswith('"') and text.endswith('"'):
            return text[1:-1]
        elif text.startswith("'") and text.endswith("'"):
            return text[1:-1]
        elif text.isdigit():
            return int(text)
        return text

    config = {}
    for key, value in list(configini.items()):
        # in configini.items, we pick up a local_config which seems
        # to be a copy of what's in configini.items--puzzling.
        if isinstance(value, dict):
            continue

        value = value.strip()
        if (((value.startswith("[") and not value.endswith("]"))
             or (not value.startswith("[") and value.endswith("]")))):
            raise ConfigSyntaxErrorException(
                "config syntax error: list '%s' missing [ or ]" %
                value)
        elif value.startswith("[") and value.endswith("]"):
            value2 = value[1:-1].strip().split(",")
            if len(value2) == 1 and value2[0] == "":
                # handle the foo = [] case
                config[key] = []
            else:
                config[key] = [s_or_i(s.strip()) for s in value2]
        else:
            config[key] = s_or_i(value)

    return config


def escape_text(s):
    """Takes in a string and converts:

    * ``&`` to ``&amp;``
    * ``>`` to ``&gt;``
    * ``<`` to ``&lt;``
    * ``\"`` to ``&quot;``
    * ``'`` to ``&#x27;``
    * ``/`` to ``&#x2F;``

    Note: if ``s`` is ``None``, then we return ``None``.

    >>> escape_text(None)
    >>> escape_text("")
    ''
    >>> escape_text("a'b")
    'a&#x27;b'
    >>> escape_text('a"b')
    'a&quot;b'
    """
    if not s:
        return s

    for mem in (("&", "&amp;"), (">", "&gt;"), ("<", "&lt;"), ("\"", "&quot;"),
                ("'", "&#x27;"), ("/", "&#x2F;")):
        s = s.replace(mem[0], mem[1])
    return s


def urlencode_text(s):
    """Calls ``urllib.quote`` on the string ``s``.

    Note: if ``s`` is ``None``, then we return ``None``.

    >>> urlencode_text(None)
    >>> urlencode_text("")
    ''
    >>> urlencode_text("a c")
    'a%20c'
    >>> urlencode_text("a&c")
    'a%26c'
    >>> urlencode_text("a=c")
    'a%3Dc'

    """
    if not s:
        return s

    return urllib.parse.quote(s)

STANDARD_FILTERS = {"escape": lambda req, vd, s: escape_text(s),
                    "urlencode": lambda req, vd, s: urlencode_text(s)}


class Stripper(HTMLParser):
    """
    removes HTML formatting code.
    """
    def __init__(self):
        self.reset()
        super().__init__()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def feed(self, d):
        self.fed.append(d)
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

    def close(self):
        pass

    def gettext(self):
        return self.get_data()



def commasplit(s):
    """
    Splits a string that contains strings by comma.  This is
    more involved than just an ``s.split(",")`` because this handles
    commas in strings correctly.

    Note: commasplit doesn't remove extranneous spaces.

    >>> commasplit(None)
    []
    >>> commasplit("")
    ['']
    >>> commasplit("a")
    ['a']
    >>> commasplit("a, b, c")
    ['a', ' b', ' c']
    >>> commasplit("'a', 'b, c'")
    ["'a'", " 'b, c'"]
    >>> commasplit("'a', \\"b, c\\"")
    ["'a'", ' \"b, c\"']

    :param s: the string to split

    :returns: list of strings
    """
    if s is None:
        return []

    if not s:
        return [""]

    start_string = None
    t = []
    l = []

    for c in s:
        if c == start_string:
            start_string = None
            t.append(c)
        elif c == "'" or c == '"':
            start_string = c
            t.append(c)
        elif not start_string and c == ",":
            l.append("".join(t))
            t = []
        else:
            t.append(c)
    if t:
        l.append("".join(t))
    return l


class Replacer:
    """
    Class for replacing variables in a template

    This class is a utility class used to provide a bound method to the
    ``re.sub()`` function.  Originally from OPAGCGI.
    """
    def __init__(self, request, encoding, var_dict):
        """
        Its only duty is to populate itself with the replacement
        dictionary passed.

        :param request: the Request object
        :param encoding: the encoding to use.  ``utf-8`` is good.
        :param var_dict: the dict containing variable substitutions
        """
        self._request = request
        self._encoding = encoding
        self.var_dict = var_dict

    def replace(self, matchobj):
        """
        This is passed a match object by ``re.sub()`` which represents
        a template variable without the ``$``.  parse manipulates the
        variable and returns the expansion of that variable using the
        following rules:

        1. if the variable ``v`` is an identifier, but not in the
           variable dict, then we return the empty string, or

        2. if the variable ``v`` is an identifier in the variable
           dict, then we return ``var_dict[v]``, or

        3. if the variable ``v`` is a function call where the function
           is an identifier in the variable dict, then

           - if ``v`` has no passed arguments and the function takes
             no arguments we return ``var_dict[v]()`` (this is the old
             behavior

           - if ``v`` has no passed arguments and the function takes
             two arguments we return ``var_dict[v](request, vd)``

           - if ``v`` has passed arguments, we return
             ``var_dict[v](request, vd, *args)`` after some mild
             processing of the arguments

        Also, for backwards compatibility reasons, we convert things
        like::

            $id_escaped
            $id_urlencoded
            $(id_escaped)
            $(id_urlencoded)

        to::

            $escape(id)
            $urlencode(id)

        :param matchobj: the regular expression match object

        :returns: the substituted string
        """
        vd = self.var_dict
        request = self._request
        key = matchobj.group(1)

        # if the variable is using $(foo) syntax, then we strip the
        # outer parens here.
        if key.startswith("(") and key.endswith(")"):
            key = key[1:-1]

        # do this for backwards-compatibility reasons
        if key.endswith("_escaped"):
            key = "escape(%s)" % key[:-8]
        elif key.endswith("_urlencoded"):
            key = "urlencode(%s)" % key[:-11]

        if key.find("(") != -1 and key.rfind(")") > key.find("("):
            args = key[key.find("(")+1:key.rfind(")")]
            key = key[:key.find("(")]
        else:
            args = None

        if key not in vd:
            return ""

        r = vd[key]

        # if the value turns out to be a function, then we call it
        # with the args that we were passed.
        if callable(r):
            if args:
                def fix(s, vd=vd):
                    # if it's an int, return an int
                    if s.isdigit():
                        return int(s)
                    # if it's a string, return a string
                    if s.startswith("'") or s.startswith('"'):
                        return s[1:-1]
                    # otherwise it might be an identifier--check
                    # the vardict and return the value if it's in
                    # there
                    if s in vd:
                        return vd[s]
                    if s.startswith("$") and s[1:] in vd:
                        return vd[s[1:]]
                    return s
                args = [fix(arg.strip()) for arg in commasplit(args)]

                # stick the request and var_dict in as the first and
                # second arguments
                args.insert(0, vd)
                args.insert(0, request)

                r = r(*args)

            elif len(inspect.getargspec(r)[0]) == 2:
                r = r(request, vd)

            else:
                # this case is here for handling the old behavior
                # where functions took no arguments
                r = r()

        # convert non-strings to strings
        if not isinstance(r, str):
            if isinstance(r, str):
                r = r.encode(self._encoding)
            else:
                r = str(r)

        return r


def parse(request, var_dict, template):
    """
    This method parses the ``template`` passed in using ``Replacer``
    to expand template variables using values in the ``var_dict``.

    Originally based on OPAGCGI, but mostly re-written.

    :param request: the Request object
    :param var_dict: the dict holding name/value pair variable replacements
    :param template: the string template we're expanding variables in.

    :returns: the template string with template variables expanded.
    """
    encoding = request.config.get("blog_encoding", "utf-8")
    replacer = Replacer(request, encoding, var_dict)
    return _VAR_REGEXP.sub(replacer.replace, template)


def walk(request, root='.', recurse=0, pattern='', return_folders=0):
    """
    This function walks a directory tree starting at a specified root
    folder, and returns a list of all of the files (and optionally
    folders) that match our pattern(s). Taken from the online Python
    Cookbook and modified to own needs.

    It will look at the config "ignore_directories" for a list of
    directories to ignore.  It uses a regexp that joins all the things
    you list.  So the following::

       config.py["ignore_directories"] = ["CVS", "dev/pyblosxom"]

    turns into the regexp::

       .*?(CVS|dev/pyblosxom)$

    It will also skip all directories that start with a period.

    :param request: the Request object
    :param root: the root directory to walk
    :param recurse: the depth of recursion; defaults to 0 which goes all
                    the way down
    :param pattern: the regexp object for matching files; defaults to
                    '' which causes Pyblosxom to return files with
                    file extensions that match those the entryparsers
                    handle
    :param return_folders: True if you want only folders, False if you
                    want files AND folders

    :returns: a list of file paths.
    """
    # expand pattern
    if not pattern:
        ext = request.get_data()['extensions']
        pattern = re.compile(r'.*\.(' + '|'.join(list(ext.keys())) + r')$')

    ignore = request.get_configuration().get("ignore_directories", None)
    if isinstance(ignore, str):
        ignore = [ignore]

    if ignore:
        ignore = [re.escape(i) for i in ignore]
        ignorere = re.compile(r'.*?(' + '|'.join(ignore) + r')$')
    else:
        ignorere = None

    # must have at least root folder
    if not os.path.isdir(root):
        return []

    return _walk_internal(root, recurse, pattern, ignorere, return_folders)

# We do this for backwards compatibility reasons.
Walk = deprecated_function(walk)


def _walk_internal(root, recurse, pattern, ignorere, return_folders):
    """
    Note: This is an internal function--don't use it and don't expect
    it to stay the same between Pyblosxom releases.
    """
    # FIXME - we should either ditch this function and use os.walk or
    # something similar, or optimize this version by removing the
    # multiple stat calls that happen as a result of islink, isdir and
    # isfile.

    # initialize
    result = []

    try:
        names = os.listdir(root)
    except OSError:
        return []

    # check each file
    for name in names:
        fullname = os.path.normpath(os.path.join(root, name))

        # grab if it matches our pattern and entry type
        if pattern.match(name):
            if ((os.path.isfile(fullname) and not return_folders) or
                (return_folders and os.path.isdir(fullname) and
                 (not ignorere or not ignorere.match(fullname)))):
                result.append(fullname)

        # recursively scan other folders, appending results
        if (recurse == 0) or (recurse > 1):
            if name[0] != "." and os.path.isdir(fullname) and \
                    not os.path.islink(fullname) and \
                    (not ignorere or not ignorere.match(fullname)):
                result = result + \
                         _walk_internal(fullname,
                                        (recurse > 1 and [recurse - 1] or [0])[0],
                                        pattern, ignorere, return_folders)

    return result


def filestat(request, filename):
    """
    Returns the filestat on a given file.  We store the filestat in
    case we've already retrieved it during this Pyblosxom request.

    This returns the mtime of the file (same as returned by
    ``time.localtime()``) -- tuple of 9 ints.

    :param request: the Request object
    :param filename: the file name of the file to stat

    :returns: the filestat (tuple of 9 ints) on the given file
    """
    data = request.getData()
    filestat_cache = data.setdefault("filestat_cache", {})

    if filename in filestat_cache:
        return filestat_cache[filename]

    argdict = {"request": request,
               "filename": filename,
               "mtime": (0,) * 10}

    MT = stat.ST_MTIME

    argdict = run_callback("filestat",
                           argdict,
                           mappingfunc=lambda x, y: y,
                           donefunc=lambda x: x and x["mtime"][MT] != 0,
                           defaultfunc=lambda x: x)

    # no plugin handled cb_filestat; we default to asking the
    # filesystem
    if argdict["mtime"][MT] == 0:
        argdict["mtime"] = os.stat(filename)

    timetuple = time.localtime(argdict["mtime"][MT])
    filestat_cache[filename] = timetuple

    return timetuple


def what_ext(extensions, filepath):
    """
    Takes in a filepath and a list of extensions and tries them all
    until it finds the first extension that works.

    :param extensions: the list of extensions to test
    :param filepath: the complete file path (minus the extension) to
                     test and find the extension for

    :returns: the extension (string) of the file or ``None``.
    """
    for ext in extensions:
        if os.path.isfile(filepath + '.' + ext):
            return ext
    return None


def is_year(s):
    """
    Checks to see if the string is likely to be a year or not.  In
    order to be considered to be a year, it must pass the following
    criteria:

    1. four digits
    2. first two digits are either 19 or 20.

    :param s: the string to check for "year-hood"

    :returns: ``True`` if it is a year and ``False`` otherwise.
    """
    if not s:
        return False

    if len(s) == 4 and s.isdigit() and \
            (s.startswith("19") or s.startswith("20")):
        return True
    return False


def importname(module_name, name):
    """
    Safely imports modules for runtime importing.

    :param module_name: the package name of the module to import from
    :param name: the name of the module to import

    :returns: the module object or ``None`` if there were problems
              importing.
    """
    logger = getLogger()
    if not module_name:
        m = name
    else:
        m = "%s.%s" % (module_name, name)

    try:
        module = __import__(m)
        for c in m.split(".")[1:]:
            module = getattr(module, c)
        return module

    except ImportError as ie:
        logger.error("Module %s in package %s won't import: %s" % \
                     (repr(module_name), repr(name), ie))

    except Exception as e:
        logger.error("Module %s not in in package %s: %s" % \
                     (repr(module_name), repr(name), e))

    return None


def generate_rand_str(minlen=5, maxlen=10):
    """
    Generate a random string between ``minlen`` and ``maxlen``
    characters long.

    The generated string consists of letters and numbers.

    :param minlen: the minimum length of the generated random string
    :param maxlen: the maximum length of the generated random string

    :returns: generated string
    """
    import random, string
    chars = string.ascii_letters + string.digits
    randstr = []
    randstr_size = random.randint(minlen, maxlen)
    x = 0
    while x < randstr_size:
        randstr.append(random.choice(chars))
        x += 1
    return "".join(randstr)

generateRandStr = deprecated_function(generate_rand_str)


def run_callback(chain, input,
                 mappingfunc=lambda x, y: x,
                 donefunc=lambda x: 0,
                 defaultfunc=None):
    """
    Executes a callback chain on a given piece of data.  passed in is
    a dict of name/value pairs.  Consult the documentation for the
    specific callback chain you're executing.

    Callback chains should conform to their documented behavior.  This
    function allows us to do transforms on data, handling data, and
    also callbacks.

    The difference in behavior is affected by the mappingfunc passed
    in which converts the output of a given function in the chain to
    the input for the next function.

    If this is confusing, read through the code for this function.

    Returns the transformed input dict.

    :param chain: the name of the callback chain to run

    :param input: dict with name/value pairs that gets passed as the
                  args dict to all callback functions

    :param mappingfunc: the function that maps output arguments to
                        input arguments for the next iteration.  It
                        must take two arguments: the original dict and
                        the return from the previous function.  It
                        defaults to returning the original dict.

    :param donefunc: this function tests whether we're done doing what
                     we're doing.  This function takes as input the
                     output of the most recent iteration.  If this
                     function returns True then we'll drop out of the
                     loop.  For example, if you wanted a callback to
                     stop running when one of the registered functions
                     returned a 1, then you would pass in:
                     ``donefunc=lambda x: x`` .

    :param defaultfunc: if this is set and we finish going through all
                        the functions in the chain and none of them
                        have returned something that satisfies the
                        donefunc, then we'll execute the defaultfunc
                        with the latest version of the input dict.

    :returns: varies
    """
    chain = plugin_utils.get_callback_chain(chain)

    output = None

    for func in chain:
        # we call the function with the input dict it returns an
        # output.
        output = func(input)

        # we fun the output through our donefunc to see if we should
        # stop iterating through the loop.  if the donefunc returns
        # something true, then we're all done; otherwise we continue.
        if donefunc(output):
            break

        # we pass the input we just used and the output we just got
        # into the mappingfunc which will give us the input for the
        # next iteration.  in most cases, this consists of either
        # returning the old input or the old output--depending on
        # whether we're transforming the data through the chain or
        # not.
        input = mappingfunc(input, output)

    # if we have a defaultfunc and we haven't satisfied the donefunc
    # conditions, then we return whatever the defaultfunc returns when
    # given the current version of the input.
    if callable(defaultfunc) and not donefunc(output):
        return defaultfunc(input)

    # we didn't call the defaultfunc--so we return the most recent
    # output.
    return output


def addcr(text):
    """Adds a cr if it needs one.

    >>> addcr("foo")
    'foo\\n'
    >>> addcr("foo\\n")
    'foo\\n'

    :returns: string with \\n at the end
    """
    if not text.endswith("\n"):
        return text + "\n"
    return text


def create_entry(datadir, category, filename, mtime, title, metadata, body):
    """
    Creates a new entry in the blog.

    This is primarily used by the testing system, but it could be used
    by scripts and other tools.

    :param datadir: the datadir
    :param category: the category the entry should go in
    :param filename: the name of the blog entry (filename and
                     extension--no directory)
    :param mtime: the mtime (float) for the entry in seconds since the
                  epoch
    :param title: the title for the entry
    :param metadata: dict of key/value metadata pairs
    :param body: the body of the entry

    :raises IOError: if the datadir + category directory exists, but
                     isn't a directory
    """

    # format the metadata lines for the entry
    metadatalines = ["#%s %s" % (key, metadata[key])
                     for key in list(metadata.keys())]

    entry = addcr(title) + "\n".join(metadatalines) + body

    # create the category directories
    d = os.path.join(datadir, category)
    if not os.path.exists(d):
        os.makedirs(d)

    if not os.path.isdir(d):
        raise IOError("%s exists, but isn't a directory." % d)

    # create the filename
    fn = os.path.join(datadir, category, filename)

    # write the entry to disk
    f = open(fn, "w")
    f.write(entry)
    f.close()

    # set the mtime on the entry
    os.utime(fn, (mtime, mtime))


def get_cache(request):
    """
    Retrieves the cache from the request or fetches a new CacheDriver
    instance.

    :param request: the Request object

    :returns: a BlosxomCache object
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
    statically rendered entries without going through all the
    rigmarole.

    First we figure out whether this blog is set up for static
    rendering.  If not, then we return--no harm done.

    If we are, then we call ``render_url`` for each ``static_flavour``
    of the entry and then for each ``static_flavour`` of the index
    page.

    :param cdict: the config.py dict
    :param entry_filename: the url path of the entry to be updated;
                           example: ``/movies/xmen2``
    """
    static_dir = cdict.get("static_dir", "")

    if not static_dir:
        return

    static_flavours = cdict.get("static_flavours", ["html"])

    render_me = []
    for mem in static_flavours:
        render_me.append("/index" + "." + mem, "")
        render_me.append(entry_filename + "." + mem, "")

    for mem in render_me:
        render_url_statically(cdict, mem[0], mem[1])


def render_url_statically(cdict, url, querystring):
    """Renders a url and saves the rendered output to the
    filesystem.

    :param cdict: config dict
    :param url: url to render
    :param querystring: querystring of the url to render or ""
    """
    static_dir = cdict.get("static_dir", "")

    # if there is no static_dir, then they're not set up for static
    # rendering.
    if not static_dir:
        raise Exception("You must set static_dir in your config file.")

    response = render_url(cdict, url, querystring)
    response.seek(0)

    fn = os.path.normpath(static_dir + os.sep + url)
    if not os.path.isdir(os.path.dirname(fn)):
        os.makedirs(os.path.dirname(fn))

    # by using the response object the cheesy part of removing the
    # HTTP headers from the file is history.
    f = open(fn, "w")
    f.write(response.read())
    f.close()


def render_url(cdict, pathinfo, querystring=""):
    """
    Takes a url and a querystring and renders the page that
    corresponds with that by creating a Request and a Pyblosxom object
    and passing it through.  It then returns the resulting Response.

    :param cdict: the config.py dict
    :param pathinfo: the ``PATH_INFO`` string;
                     example: ``/dev/pyblosxom/firstpost.html``
    :param querystring: the querystring (if any); example: debug=yes

    :returns: a Pyblosxom ``Response`` object.
    """
    from .pyblosxom import Pyblosxom

    if querystring:
        request_uri = pathinfo + "?" + querystring
    else:
        request_uri = pathinfo

    env = {
        "HTTP_HOST": "localhost",
        "HTTP_REFERER": "",
        "HTTP_USER_AGENT": "static renderer",
        "PATH_INFO": pathinfo,
        "QUERY_STRING": querystring,
        "REMOTE_ADDR": "",
        "REQUEST_METHOD": "GET",
        "REQUEST_URI": request_uri,
        "SCRIPT_NAME": "",
        "wsgi.errors": sys.stderr,
        "wsgi.input": None
    }
    data = {"STATIC": 1}
    p = Pyblosxom(cdict, env, data)
    p.run(static=True)
    return p.get_response()


#******************************
# Logging
#******************************

import logging

# A dict to keep track of created log handlers.  Used to prevent
# multiple handlers from being added to the same logger.
_loghandler_registry = {}


class LogFilter(object):
    """
    Filters out messages from log-channels that are not listed in the
    log_filter config variable.
    """
    def __init__(self, names=None):
        """
        Initializes the filter to the list provided by the names
        argument (or ``[]`` if ``names`` is ``None``).

        :param names: list of strings to filter out
        """
        if names == None:
            names = []
        self.names = names

    def filter(self, record):
        if record.name in self.names:
            return 1
        return 0


def get_logger(log_file=None):
    """Creates and returns a log channel.

    If no log_file is given the system-wide logfile as defined in
    config.py is used. If a log_file is given that's where the created
    logger logs to.

    :param log_file: the file to log to.  defaults to None which
                     causes Pyblosxom to check for the ``log_file``
                     config.py property and if that's blank, then the
                     log_file is stderr

    :returns: a log channel (logger instance) which you can call
              ``error``, ``warning``, ``debug``, ``info``, ... on.
    """
    custom_log_file = False
    if log_file is None:
        log_file = _config.get('log_file', 'stderr')
        f = sys._getframe(1)
        filename = f.f_code.co_filename
        module = f.f_globals["__name__"]
        # by default use the root logger
        log_name = ""
        for path in _config.get('plugin_dirs', []):
            if filename.startswith(path):
                # if it's a plugin, use the module name as the log
                # channels name
                log_name = module
                break
        # default to log level WARNING if it's not defined in
        # config.py
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

    # setup the handler if it doesn't already exist.  only add one
    # handler per log channel.
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
            # add 'root' to the log_filter list to still allow
            # application level messages.
            log_filter = _config.get('log_filter', None)
            if log_filter:
                lfilter = LogFilter(log_filter)
                logger.addFilter(lfilter)

        # remember that we've seen this handler
        _loghandler_registry[key] = True

    return logger

getLogger = deprecated_function(get_logger)


def log_exception(log_file=None):
    """
    Logs an exception to the given file.  Uses the system-wide
    log_file as defined in config.py if none is given here.

    :param log_file: the file to log to.  defaults to None which
                     causes Pyblosxom to check for the ``log_file``
                     config.py property and if that's blank, then the
                     log_file is stderr
    """
    log = getLogger(log_file)
    log.exception("Exception occured:")


def log_caller(frame_num=1, log_file=None):
    """
    Logs some info about the calling function/method.  Useful for
    debugging.

    Usage:

    >>> import tools
    >>> tools.log_caller()     # logs frame 1
    >>> tools.log_caller(2)
    >>> tools.log_caller(3, log_file="/path/to/file")

    :param frame_num: the index of the frame to log; defaults to 1

    :param log_file: the file to log to.  defaults to None which
                     causes Pyblosxom to check for the ``log_file``
                     config.py property and if that's blank, then the
                     log_file is stderr
    """
    f = sys._getframe(frame_num)
    module = f.f_globals["__name__"]
    filename = f.f_code.co_filename
    line = f.f_lineno
    subr = f.f_code.co_name

    log = getLogger(log_file)
    log.info("\n  module: %s\n  filename: %s\n  line: %s\n  subroutine: %s",
             module, filename, line, subr)
