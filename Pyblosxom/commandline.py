#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003-2008 Wari Wahab
# Copyright (c) 2003-2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#######################################################################
"""
This module holds commandline related stuff.  Installation
verification, blog creation, commandline argument parsing, ...
"""

import os
import os.path
import sys
import textwrap
from optparse import OptionParser

from Pyblosxom.pyblosxom import VERSION_DATE, PyBlosxom
from Pyblosxom.tools import run_callback
from Pyblosxom import plugin_utils

USAGE = "%prog [options] [command] [command-options]"
VERSION = "%prog " + VERSION_DATE

def pwrap(s):
    """Wraps the text and prints it.
    """
    starter = ""
    linesep = os.linesep
    if s.startswith("- "):
        starter = "- "
        s = s[2:]
        linesep = os.linesep + "  "

    print starter + linesep.join(textwrap.wrap(s, 72))

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

def build_pyblosxom():
    """Imports config.py and builds an empty PyBlosxom object.
    """
    pwrap("Trying to import the config module....")
    try:
        from config import py as cfg
    except StandardError:
        h, t = os.path.split(sys.argv[0])
        scriptname = t or h

        pwrap_error("ERROR: Cannot find your config.py file.  Please execute "
                    "%s in the directory with the config.py file in it or use "
                    "the --config flag.\n\n"
                    "See \"%s --help\" for more details." % (scriptname,
                                                             scriptname))
        return None

    return PyBlosxom(cfg, {})

def build_parser(usage):
    parser = OptionParser(usage=usage, version=VERSION)
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="If the quiet flag is specified, then PyBlosxom "
                      "will run quietly.")
    parser.add_option("--config",
                      help="This specifies the directory that the config.py "
                      "for the blog you want to work with is in.  If the "
                      "config.py file is in the current directory, then "
                      "you don't need to specify this.  All commands except "
                      "the 'create' command need a config.py file.")

    return parser

def test_installation(command, argv):
    """
    This function gets called when someone starts up pyblosxom.cgi
    from the command line with no REQUEST_METHOD environment variable.
    It:

    1. verifies config.py file properties
    2. initializes all the plugins they have installed
    3. runs ``cb_verify_installation``--plugins can print out whether
       they are installed correctly (i.e. have valid config property
       settings and can read/write to data files)

    The goal is to be as useful and informative to the user as we can
    be without being overly verbose and confusing.

    This is designed to make it easier for a user to verify their
    PyBlosxom installation is working and also to install new plugins
    and verify that their configuration is correct.

    :Parameters:
       request : Request object
          the request object
    """
    parser = build_parser("%prog test [options]")
    parser.parse_args()

    p = build_pyblosxom()
    if not p:
        return 0

    request = p.get_request()
    config = request.config

    pwrap("System Information")
    pwrap("==================")
    pwrap("")

    pwrap("- pyblosxom:    %s" % VERSION_DATE)
    pwrap("- sys.version:  %s" % sys.version.replace("\n", " "))
    pwrap("- os.name:      %s" % os.name)
    codebase = os.path.dirname(os.path.dirname(__file__))
    pwrap("- codebase:     %s" % config.get("codebase", codebase))
    pwrap("")

    pwrap("Checking config.py file")
    pwrap("=======================")
    pwrap("- properties set: %s" % len(config))

    config_keys = config.keys()

    if "datadir" not in config_keys:
        pwrap_error("- ERROR: 'datadir' must be set.  Refer to installation "
              "documentation.")

    elif not os.path.isdir(config["datadir"]):
        pwrap_error("- ERROR: datadir '%s' does not exist."
                    "  You need to create your datadir and give it "
                    " appropriate permissions.")

    else:
        pwrap("- datadir '%s' exists." % config["datadir"])

    if (("blog_encoding" in config_keys 
         and config["blog_encoding"].lower() != "utf-8")):
        pwrap_error("- WARNING: 'blog_encoding' is set to something other "
                    "than 'utf-8'.  As of PyBlosxom 2.0, "
                    "this isn't a good idea unless you're absolutely certain "
                    "it's going to work for your blog.")
    pwrap("")

    pwrap("Checking plugin configuration")
    pwrap("=============================")

    import traceback

    no_verification_support = []

    if len(plugin_utils.plugins) == 0:
        pwrap("- There are no plugins installed.")
    else:
        pwrap("- This goes through your plugins and asks each of them to "
              "verify configuration and installation.")
        pwrap("")
        pwrap("----")
        for mem in plugin_utils.plugins:
            if hasattr(mem, "verify_installation"):
                pwrap("plugin:  %s" % mem.__name__)
                print "file:    %s" % mem.__file__
                print "version: %s" % (str(getattr(mem, "__version__")))

                try:
                    if mem.verify_installation(request) == 1:
                        pwrap("PASS")
                    else:
                        pwrap_error("FAIL")
                except StandardError:
                    pwrap_error("FAIL: Exception thrown:")
                    traceback.print_exc(file=sys.stdout)

                pwrap("----")
            else:
                mn = mem.__name__
                mf = mem.__file__
                no_verification_support.append( "'%s' (%s)" % (mn, mf))

        if len(no_verification_support) > 0:
            pwrap("")
            pwrap("The following plugins do not support installation "
                  "verification:")
            no_verification_support.sort()
            for mem in no_verification_support:
                print "- %s" % mem

    pwrap("")
    pwrap("Verification complete.  Correct any errors and warnings above.")

def create_blog(command, argv):
    """
    Creates a blog in the specified directory.  Mostly this involves
    copying things over, but there are a few cases where we expand
    template variables.
    """
    parser = build_parser("%prog create [options] <dir>")
    (options, args) = parser.parse_args()

    if args:
        d = args[0]
    else:
        d = "."

    if d == ".":
        d = "." + os.sep + "blog"

    d = os.path.abspath(d)

    verbose = options.verbose

    if os.path.isfile(d) or os.path.isdir(d):
        pwrap_error("ERROR: Cannot create '%s'--something is in the way." % d)
        return 0

    def _mkdir(d):
        if verbose:
            print "Creating '%s'..." % d
        os.makedirs(d)

    _mkdir(d)
    _mkdir(os.path.join(d, "entries"))
    _mkdir(os.path.join(d, "plugins"))

    source = os.path.join(os.path.dirname(__file__), "flavours")

    for root, dirs, files in os.walk(source):
        if ".svn" in root:
            continue

        dest = os.path.join(d, "flavours", root[len(source)+1:])
        if not os.path.isdir(dest):
            if verbose:
                print "Creating '%s'..." % dest
            os.mkdir(dest)

        for mem in files:
            if verbose:
                print "Creating file '%s'..." % os.path.join(dest, mem)
            fpin = open(os.path.join(root, mem), "r")
            fpout = open(os.path.join(dest, mem), "w")

            fpout.write(fpin.read())

            fpout.close()
            fpin.close()

    def _copyfile(frompath, topath, fn, fix=False):
        if verbose:
            print "Creating file '%s'..." % os.path.join(topath, fn)
        fp = open(os.path.join(frompath, fn), "r")
        filedata = fp.readlines()
        fp.close()

        if fix:
            basedir = topath
            if not basedir.endswith(os.sep):
                basedir = basedir + os.sep
            if os.sep == "\\":
                basedir = basedir.replace(os.sep, os.sep + os.sep)
            datamap = { "basedir": basedir,
                        "codedir": os.path.dirname(os.path.dirname(__file__)) }
            filedata = [line % datamap for line in filedata]

        fp = open(os.path.join(topath, fn), "w")
        fp.write("".join(filedata))
        fp.close()

    source = os.path.join(os.path.dirname(__file__), "data")

    _copyfile(source, d, "config.py", fix=True)
    _copyfile(source, d, "blog.ini", fix=True)
    _copyfile(source, d, "pyblosxom.cgi", fix=True)

    datadir = os.path.join(d, "entries")
    firstpost = os.path.join(datadir, "firstpost.txt")
    if verbose:
        print "Creating file '%s'..." % firstpost
    fp = open(firstpost, "w")
    fp.write("""First post!
<p>
  This is your first post!  If you can see this with a web-browser,
  then it's likely that everything's working nicely!
</p>
""")
    fp.close()

    if verbose:
        print "Done!"
    return 0

def render_url(command, argv):
    """Renders a single url.
    """
    parser = build_parser("%prog renderurl [options] <url> [<url>...]")

    parser.add_option("--headers",
                      action="store_true", dest="headers", default=False,
                      help="Option that causes headers to be displayed "
                      "when rendering a single url.")

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        return 0

    for url in args:
        p = build_pyblosxom()

        base_url = p.get_request().config.get("base_url", "")
        if url.startswith(base_url):
            url = url[len(base_url):]
        p.run_render_one(url, options.headers)

    return 0

def run_static_renderer(command, argv):
    parser = build_parser("%prog staticrender [options]")
    parser.add_option("--incremental",
                      action="store_true", dest="incremental", default=False,
                      help="Option that causes static rendering to be "
                      "incremental.")

    (options, args) = parser.parse_args()

    p = build_pyblosxom()
    if not p:
        return 0

    return p.run_static_renderer(options.incremental)

DEFAULT_HANDLERS = (
    ("create", create_blog, "Creates directory structure for a new blog."),
    ("test", test_installation, 
     "Tests installation and configuration for a blog."),
    ("staticrender", run_static_renderer, 
     "Statically renders your blog into an HTML site."),
    ("renderurl", render_url, "Renders a single url of your blog.")
    )

def get_handlers():
    try:
        from config import py as cfg
        plugin_utils.initialize_plugins(cfg.get("plugin_dirs", []),
                                        cfg.get("load_plugins", None))
    except ImportError:
        pass

    handlers_dict = dict([(v[0], (v[1], v[2])) for v in DEFAULT_HANDLERS])
    handlers_dict = run_callback("commandline", handlers_dict,
                                 mappingfunc=lambda x, y: y,
                                 defaultfunc=lambda x: x)

    # test the handlers, drop any that aren't the right return type,
    # and print a warning.
    handlers = []
    for k, v in handlers_dict.items():
        if not len(v) == 2 or not callable(v[0]) or not isinstance(v[1], str):
            print "Plugin returned '%s' for commandline." % ((k, v),)
            continue
        handlers.append((k, v[0], v[1]))

    return handlers

def command_line_handler(scriptname, argv):
    if "--silent" in argv:
        sys.stdout = open(os.devnull, "w")
        argv.remove("--silent")

    print "%s version %s" % (scriptname, VERSION_DATE)

    # slurp off the config file setting and add it to sys.path.
    # this needs to be first to pick up plugin-based command handlers.
    configdir = None
    for i, mem in enumerate(argv):
        if mem.startswith("--config"):
            if "=" in mem:
                _, configdir = mem.split("=")
                break
            else:
                try:
                    configdir = argv[i+1]
                    break
                except IndexError:
                    pwrap_error("Error: no config file argument specified.")
                    pwrap_error("Exiting.")
                    return 1

    if configdir is not None:
        if configdir.endswith("config.py"):
            configdir = configdir[0:-9]

        if not os.path.exists(configdir):
            pwrap_error("ERROR: '%s' does not exist--cannot find config.py "
                        "file." % configdir)
            pwrap_error("Exiting.")
            return 1

        if not "config.py" in os.listdir(configdir):
            pwrap_error("Error: config.py not in '%s'.  "
                        "Cannot find config.py file." % configdir)
            pwrap_error("Exiting.")
            return 1

        sys.path.append(configdir)
        print "Adding %s to sys.path...." % configdir

    handlers = get_handlers()

    if len(argv) == 1 or (len(argv) == 2 and argv[1] in ("-h", "--help")):
        parser = build_parser("[command]")
        parser.print_help()
        print ""
        print "Commands:"
        for command_str, _, command_help in handlers:
            print "    %-14s %s" % (command_str, command_help)
        return 0

    if argv[1] == "--version":
        return 0

    # then we execute the named command with options, or print help
    if argv[1].startswith("-"):
        pwrap_error ( "Command '%s' does not exist." % argv[1])
        pwrap_error ('')
        pwrap_error ( "Commands:")
        for command_str, _, command_help in handlers:
            pwrap_error ( "    %-14s %s" % (command_str, command_help))
        return 1

    command = argv.pop(1)
    for (c, f, h) in handlers:
        if c == command:
            return f(command, argv)

    pwrap_error ( "Command '%s' does not exist." % command)
    for command_str, command_func, command_help in handlers:
        pwrap_error ( "    %-14s %s" % (command_str, command_help))
    return 1
