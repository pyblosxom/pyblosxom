#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003-2008 Wari Wahab
# 
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#
# $Id: pyblosxom.py 1226 2008-03-22 04:01:05Z willhelm $
#######################################################################

import os
import os.path
import sys

from Pyblosxom.pyblosxom import VERSION_DATE, PyBlosxom

from optparse import OptionParser, OptionGroup



HELP = """Syntax: %(script)s [path-opts] [args]

PATH OPTIONS:

  -c, --config

     This specifies the location of the config.py file for the blog 
     you want to work with.  If the config.py file is in the current 
     directory, then you don't need to specify this.

     Note: %(script)s will use the "codebase" parameter in your config.py
     file to locate the version of PyBlosxom you're using if there
     is one.  If there isn't one, then %(script)s expects PyBlosxom to
     be installed as a Python package on your system.

ARGUMENTS:

  -v, --version

     Prints the PyBlosxom version and some other information.

  -h, --help

     Prints this help text

  -C, --create <dir>

     Creates a PyBlosxom "installation" by building the directory hierarchy
     and copying necessary files into it.  This is an easy way to create
     a new blog.

  -h, --headers

     When rendering a url, this will also render the HTTP headers.

  -r, --render <url>

     Renders a url of your blog.

        %(script)s -r http://www.joesblog.com/cgi-bin/pyblosxom.cgi/index.html

     will pull off the base_url from the front leaving "/index.html" and
     will render "/index.html" to stdout.

        %(script)s -c ~/cgi-bin/config.py -r /index.html

     will use the config.py file located in ~/cgi-bin/ and render
     "/index.html" from the PyBlosxom root.

  -s, --static [incremental]

     Statically renders your blog.  Use "incremental" to do an incremental 
     rendering.

  -t, --test

     Tests your installation.
     

EXAMPLES:


Additional flags and options may be available through plugins that
you have installed.  Refer to plugin documentation (usually found
at the top of the plugin file) for more information.
"""
     

def test_installation(request):
    """
    This function gets called when someone starts up pyblosxom.cgi
    from the command line with no REQUEST_METHOD environment variable.
    It:

    1. tests properties in their config.py file
    2. verifies they have a datadir and that it exists
    3. initializes all the plugins they have installed
    4. runs "cb_verify_installation"--plugins can print out whether
       they are installed correctly (i.e. have valid config property
       settings and can read/write to data files)
    5. exits

    The goal is to be as useful and informative to the user as we can be
    without being overly verbose and confusing.

    This is designed to make it much much much easier for a user to
    verify their PyBlosxom installation is working and also to install
    new plugins and verify that their configuration is correct.

    :Parameters:
       request : Request object
          the request object
    """
    config = request.config

    # BASE STUFF
    print ""
    print "Welcome to PyBlosxom's installation verification system."
    print "------"
    print "]] printing diagnostics [["
    print "pyblosxom:   %s" % VERSION_DATE
    print "sys.version: %s" % sys.version.replace("\n", " ")
    print "os.name:     %s" % os.name
    print "codebase:    %s" % config.get("codebase", 
                              os.path.dirname(os.path.dirname(__file__)))
    print "------"

    # CONFIG FILE
    print "]] checking config file [["
    print "config has %s properties set." % len(config)
    print ""

    # these are required by the blog
    required_config = ["datadir"]

    # these are nice to have optional properties
    nice_to_have_config = ["blog_title", "blog_author", "blog_description",
                           "blog_language", "blog_encoding", "blog_icbm",
                           "base_url", "depth", "num_entries", "renderer", 
                           "plugin_dirs", "load_plugins", "blog_email", 
                           "blog_rights", "default_flavour", "flavourdir", 
                           "log_file", "log_level"]

    config_keys = config.keys()

    # remove keys that are auto-generated
    config_keys.remove("pyblosxom_version")
    config_keys.remove("pyblosxom_name")

    missing_required_props = []
    missing_optionsal_props = []

    missing_required_props = [ m for m in required_config if m not in config_keys ]

    missing_optional_props = [ m for m in nice_to_have_config if m not in config_keys ]

    all_keys = nice_to_have_config + required_config
    
    config_keys = [ m for m in config_keys if m not in all_keys ]

    def wrappify(ks):
        ks.sort()
        if len(ks) == 1:
            return "   %s" % ks[0]
        elif len(ks) == 2:
            return "   %s and %s" % (ks[0], ks[1])

        ks = ", ".join(ks[:-1]) + " and " + ks[-1]
        import textwrap
        return "   " + "\n   ".join( textwrap.wrap(ks, 72) )
    
    if missing_required_props:
        print ""
        print "Missing properties must be set in order for your blog to work."
        print ""
        print wrappify(missing_required_props)
        print ""
        print "This must be done before we can go further.  Exiting."
        return

    if missing_optional_props:
        print ""
        print "You're missing optional properties.  These are not required, but some of them"
        print "may interest you.  Refer to the documentation for more information."
        print ""
        print wrappify(missing_optional_props)

    if config_keys:
        print ""
        print "These are properties PyBlosxom doesn't know about.  They could be used by plugins" 
        print "or could be ones you've added.  Remove them if you know they're not used."
        print ""
        print wrappify(config_keys)
        print ""
        
    print "PASS: config file is fine."

    print "------"
    print "]] checking datadir [["
    print "Note: this does NOT check whether your webserver has permissions to view files therein."

    # DATADIR
    if not os.path.isdir(config["datadir"]):
        print "datadir '%s' does not exist." % config["datadir"]          
        print "You need to create your datadir and give it appropriate"
        print "permissions."
        print ""
        print "This must be done before we can go further.  Exiting."
        return

    print "PASS: datadir is there."

    print "------"
    print "]] checking plugins [["

    if "plugin_dirs" in config:
        plugin_utils.initialize_plugins(config["plugin_dirs"],
                                        config.get("load_plugins", None))

        no_verification_support = []

        if len(plugin_utils.plugins) == 0:
            print "There are no plugins installed."

        else:
            for mem in plugin_utils.plugins:
                if hasattr(mem, "verify_installation"):
                    print "=== plugin: '%s'" % mem.__name__
                    print "    file: %s" % mem.__file__
                    print "    version: %s" % (str(getattr(mem, "__version__")))

                    try:
                        if mem.verify_installation(request) == 1:
                            print "    PASS"
                        else:
                            print "    FAIL!!!"
                    except AssertionError, error_message:
                        print " FAIL!!! ", error_message

                else:
                    mn = mem.__name__
                    mf = mem.__file__
                    no_verification_support.append( "'%s' (%s)" % (mn, mf))

            if len(no_verification_support) > 0:
                print ""
                print "The following plugins do not support installation " + \
                      "verification:"
                for mem in no_verification_support:
                    print "   %s" % mem

    else:
        print "You have chosen not to load any plugins."


def create_blog(d, verbose):
    """
    Creates a blog in the specified directory.  Mostly this involves
    copying things over, but there are a few cases where we expand
    template variables.
    """
    if d == ".":
        d = "." + os.sep + "blog"

    d = os.path.abspath(d)
    
    if os.path.isfile(d) or os.path.isdir(d):
        if verbose: print "Cannot create '%s'--something is in the way." % d
        return 0

    def mkdir(d):
        if verbose: print "Creating '%s'..." % d
        os.makedirs(d)

    mkdir(d)
    mkdir(os.path.join(d, "entries"))
    mkdir(os.path.join(d, "plugins"))

    source = os.path.join(os.path.dirname(__file__), "flavours")

    for root, dirs, files in os.walk(source):
        if ".svn" in root:
            continue

        dest = os.path.join(d, "flavours", root[len(source)+1:])
        if not os.path.isdir(dest):
            if verbose: print "Creating '%s'..." % dest
            os.mkdir(dest)

        for mem in files:
            if verbose: print "Creating file '%s'..." % os.path.join(dest, mem)
            fpin = open(os.path.join(root, mem), "r")
            fpout = open(os.path.join(dest, mem), "w")

            fpout.write(fpin.read())

            fpout.close()
            fpin.close()
 
    def copyfile(frompath, topath, fn, fix=False):
        if verbose: print "Creating file '%s'..." % os.path.join(topath, fn)
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

    copyfile(source, d, "config.py", fix=True)
    copyfile(source, d, "blog.ini", fix=True)
    copyfile(source, d, "pyblosxom.cgi")

    datadir = os.path.join(d, "entries")
    firstpost = os.path.join(datadir, "firstpost.txt")
    if verbose: print "Creating file '%s'..." % firstpost
    fp = open(firstpost, "w")
    fp.write("""First post!
<p>
  This is your first post!  If you can see this with a web-browser,
  then it's likely that everything's working nicely!
</p>
""")
    fp.close()

    if verbose: print "Done!"
    return 0

def command_line_handler(scriptname, argv):
    """
    Handles calling PyBlosxom from the command line.  This can be
    called from two different things: pyblosxom.cgi and pyblcmd.

    @param scriptname: the name of the script (ex. "pyblcmd")
    @type  scriptname: string

    @param argv: the arguments passed in
    @type  argv: list of strings

    @returns: the exit code
    """
    parser = OptionParser(version="%prog " + VERSION_DATE )
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="If the quiet flag is specified, then PyBlosxom will "
                           "run quietly.")
    parser.add_option("--config",
                      help="This specifies the location of the config.py file "
                           "for the blog you want to work with.  If the "
                           "config.py file is in the current directory, then "
                           "you don't need to specify this.")

    startgroup = OptionGroup(parser, "Starting out")
    startgroup.add_option("--create",
                          help="Creates the blog structure complete with "
                               "config.py file, directories, flavour files and "
                               "an initial blog post.")
    startgroup.add_option("--test",
                          action="store_true", dest="test", default=False,
                          help="Verifies your config.py file and blog.")
    parser.add_option_group(startgroup)

    staticgroup = OptionGroup(parser, "Static rendering")
    staticgroup.add_option("--static",
                           action="store_true", dest="static", default=False,
                           help="Statically renders your blog.")
    staticgroup.add_option("--incremental",
                           action="store_true", dest="incremental", default=False,
                           help="Causes static rendering to be incremental.")
    parser.add_option_group(staticgroup)

    commandsgroup = OptionGroup(parser, "Other commands")
    commandsgroup.add_option("-r", "--render",
                             help="Renders a single url of your blog.")
    commandsgroup.add_option("--headers",
                             action="store_true", dest="headers", default=False,
                             help="Causes headers to be displayed when rendering "
                                  "a single url.")
    parser.add_option_group(commandsgroup)

    def printq(s):
        print s

    (options, args) = parser.parse_args()

    if not options.verbose:
        printq = lambda s : s

    printq("%s version %s" % (scriptname, VERSION_DATE))

    if options.create:
        return create_blog(options.create, options.verbose)

    if options.config:
        m = options.config
        if m.endswith("config.py"):
            m = m[0:-9]
        printq("Appending %s to sys.path for importing config.py." % m)
        sys.path.append(m)

    # after this point, we need a config.py dict to do things

    def get_p():
        printq("Trying to import the config module....")
        try:
            from config import py as cfg
        except:
            print "Error: Cannot find your config.py file.  Please execute %s in" % scriptname
            print "the directory with your config.py file in it or use the --config"
            print "flag.  See \"%s --help\" for more details." % scriptname
            return None

        return PyBlosxom(cfg, {})

    if options.test:
        p = get_p()
        if not p: return 0
        return p.testInstallation()

    if options.static:
        p = get_p()
        if not p: return 0
        return p.runStaticRenderer(options.incremental, options.verbose)

    if options.render:
        url = mem[1]
        if url.startswith(cfg.get("base_url", "")):
            url = url[len(cfg.get("base_url", "")):]

        printq("Rendering '%s'" % url)

        p = get_p()
        if not p: return 0
        return p.runRenderOne(url, options.headers)

    parser.print_help()
    return 0
