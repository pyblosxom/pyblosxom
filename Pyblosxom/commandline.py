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
"""
This module holds commandline related stuff.  Installation verification,
blog creation, commandline argument parsing, ...
"""

import os
import os.path
import sys
from optparse import OptionParser, OptionGroup

from Pyblosxom.pyblosxom import VERSION_DATE, PyBlosxom

def test_installation(request):
    """
    This function gets called when someone starts up pyblosxom.cgi
    from the command line with no REQUEST_METHOD environment variable.
    It:

    1. verifies config.py file properties
    2. initializes all the plugins they have installed
    3. runs ``cb_verify_installation``--plugins can print out whether
       they are installed correctly (i.e. have valid config property
       settings and can read/write to data files)

    The goal is to be as useful and informative to the user as we can be
    without being overly verbose and confusing.

    This is designed to make it easier for a user to verify their PyBlosxom
    installation is working and also to install new plugins and verify that
    their configuration is correct.

    :Parameters:
       request : Request object
          the request object
    """
    config = request.config

    print "== System information =="
    print "   pyblosxom:    %s" % VERSION_DATE
    print "   sys.version:  %s" % sys.version.replace("\n", " ")
    print "   os.name:      %s" % os.name
    print "   codebase:     %s" % config.get("codebase", 
                                  os.path.dirname(os.path.dirname(__file__)))

    print ""
    print "== Checking config.py file =="
    print "   properties set: %s" % len(config)

    config_keys = config.keys()

    if "datadir" not in config_keys:
        print "ERROR: 'datadir' must be set.  Refer to installation " + \
              "documentation."

    elif not os.path.isdir(config["datadir"]):
        print "ERROR: datadir '%s' does not exist.  You need to create your " + \
              "datadir and give it appropriate permissions."

    else:
        print "   datadir '%s' exists." % config["datadir"]

    if "blog_encoding" in config_keys and config["blog_encoding"].lower() != "utf-8":
        print "WARNING: 'blog_encoding' is set to something other than " + \
              "'utf-8'.  As of PyBlosxom 2.0, this isn't a good idea unless " + \
              "you're absolutely certain it's going to work for your blog."

    print ""
    print "== Checking plugin configuration =="
    print "   This goes through your plugins and asks each of them to verify " + \
          "configuration and installation."

    if "plugin_dirs" in config:
        from Pyblosxom import plugin_utils
        import traceback

        plugin_utils.initialize_plugins(config["plugin_dirs"],
                                        config.get("load_plugins", None))

        no_verification_support = []

        if len(plugin_utils.plugins) == 0:
            print "   There are no plugins installed."

        else:
            print ""
            for mem in plugin_utils.plugins:
                if hasattr(mem, "verify_installation"):
                    print "=== plugin: '%s'" % mem.__name__
                    print "    file: %s" % mem.__file__
                    print "    version: %s" % (str(getattr(mem, "__version__")))

                    try:
                        if mem.verify_installation(request) == 1:
                            print "    PASS"
                        else:
                            print "    FAIL"
                    except Exception, e:
                        print "    FAIL: Exception thrown:"
                        traceback.print_exc(file=sys.stdout)

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

    print ""
    print "Verification complete.  Correct any errors and warnings above."


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
    called from two different things: pyblosxom.cgi and pyblosxom-cmd.

    @param scriptname: the name of the script (ex. "pyblosxom-cmd")
    @type  scriptname: string

    @param argv: the arguments passed in
    @type  argv: list of strings

    @returns: the exit code
    """
    parser = OptionParser(usage="%prog [options] [command]",
                          version="%prog " + VERSION_DATE )
    
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="If the quiet flag is specified, then PyBlosxom will "
                           "run quietly.")
    parser.add_option("--config",
                      help="This specifies the directory that the config.py "
                           "for the blog you want to work with is in.  If the "
                           "config.py file is in the current directory, then "
                           "you don't need to specify this.")

    newbloggroup = OptionGroup(parser, "Commands for creating a new blog",
                               "Note: Blog creation commands don't require a "
                               "config.py file.")
    newbloggroup.add_option("--create",
                            dest="blogdir",
                            help="Creates the blog structure complete with "
                                 "config.py file, directories, flavour files and "
                                 "an initial blog post.")
    parser.add_option_group(newbloggroup)
    
    testgroup = OptionGroup(parser, "Commands for testing a blog")
    testgroup.add_option("--test",
                         action="store_true", dest="test", default=False,
                         help="Provides some verification of your config.py "
                              "and points out some common errors.")
    parser.add_option_group(testgroup)

    staticgroup = OptionGroup(parser, "Commands for static rendering")
    staticgroup.add_option("--static",
                           action="store_true", dest="static", default=False,
                           help="Command for 'compiling' your blog using "
                                "static rendering.  This allows you to use "
                                "PyBlosxom even if your web host doesn't allow "
                                "for CGI or other dynamic content scripts.")
    staticgroup.add_option("--incremental",
                           action="store_true", dest="incremental", default=False,
                           help="Option that causes static rendering to be "
                                "incremental.")
    parser.add_option_group(staticgroup)

    commandsgroup = OptionGroup(parser, "Other commands")
    commandsgroup.add_option("-r", "--render", dest="url",
                             help="Command to renders a single url of your blog.")
    commandsgroup.add_option("--headers",
                             action="store_true", dest="headers", default=False,
                             help="Option that causes headers to be displayed "
                                  "when rendering a single url.")
    parser.add_option_group(commandsgroup)

    def printq(s):
        print s

    (options, args) = parser.parse_args()

    if not options.verbose:
        printq = lambda s : s

    printq("%s version %s" % (scriptname, VERSION_DATE))

    if options.blogdir:
        return create_blog(options.blogdir, options.verbose)

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
            print \
"""
Error: Cannot find your config.py file.  Please execute %s in the
directory with the config.py file in it or use the --config flag.

See "%s --help" for more details.
""" % (scriptname, scriptname)
            return None

        return PyBlosxom(cfg, {})

    if options.test:
        p = get_p()
        if not p: 
            return 0
        return test_installation(p.getRequest())

    if options.static:
        p = get_p()
        if not p: return 0
        return p.runStaticRenderer(options.incremental, options.verbose)

    if options.url:
        url = options.url

        p = get_p()
        if not p:
            return 0
        
        base_url = p.getRequest().config.get("base_url", "")
        if url.startswith(base_url):
            url = url[len(base_url)]

        printq("Rendering '%s'\n" % url)
        return p.runRenderOne(url, options.headers)

    parser.print_help()
    return 0
