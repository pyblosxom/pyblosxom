"""
This module tests the installation for pyblosxom for a given user.
It's a little basic at the moment.  It:

  1. tests properties in their config.py file
  2. verifies they have a datadir and that it exists
  3. initializes all the plugins they have installed
  4. runs "cb_verify_installation"--plugins can print out whether
     they are installed correctly (i.e. have valid config property
     settings and can read/write to data files)
  5. exits

The goal is to be as useful and informative to the user as we can be
without being overly verbose and confusing.

Modifications and additional tests are more than welcome.
"""
def test_installation(request):
    """
    This function gets called when someone starts up pyblosxom.cgi
    from the command line with no REQUEST_METHOD environment variable.

    It goes through and verifies that the configuration is correct,
    instantiates all the plugins, and then calls "verify_configuration"
    on each plugin allowing them to verify the configuration.

    It then prints out any errors that it sees as well as any other
    messages from the plugins.

    This is designed to make it much much much easier for a user to
    verify their PyBlosxom installation is working and also to install
    new plugins and verify that their configuration is correct.
    """
    import sys, os, os.path

    config = request.getConfiguration()

    # BASE STUFF
    print "Welcome to PyBlosxom's installation verification system."
    print "------"
    print "]] printing diagnostics [["
    print "sys.version: %s" % sys.version.replace("\n", " ")
    print "os.name:     %s" % os.name
    print "codebase:    %s" % config.get("codebase", "--default--")
    print "------"

    # CONFIG FILE
    print "]] checking config file [["
    print "config has %s properties set." % len(config)
    print ""
    required_config = ["datadir"]

    nice_to_have_config = ["blog_title", "blog_author", "blog_description",
                           "blog_language", "blog_encoding", 
                           "blosxom_custom_flavours", "base_url", "depth",
                           "num_entries", "renderer", "cacheDriver", 
                           "cacheConfig", "plugin_dirs", "load_plugins"]
    missing_properties = 0
    for mem in required_config:
        if not config.has_key(mem):
            print "   missing required property: '%s'" % mem
            missing_properties = 1

    for mem in nice_to_have_config:
        if not config.has_key(mem):
            print "   missing optional property: '%s'" % mem

    print ""
    print "Refer to the documentation for what properties are available"
    print "and what they do."

    if missing_properties:
        print ""
        print "Missing properties must be set in order for your blog to"
        print "work."
        print ""
        print "This must be done before we can go further.  Exiting."
        return

    print "PASS: config file is fine."

    print "------"
    print "]] checking datadir [["

    # DATADIR
    # FIXME - we should check permissions here?
    if not os.path.isdir(config["datadir"]):
        print "datadir '%s' does not exist." % config["datadir"]          
        print "You need to create your datadir and give it appropriate"
        print "permissions."
        print ""
        print "This must be done before we can go further.  Exiting."
        return

    print "PASS: datadir is fine."

    print "------"
    print "Now we're going to verify your plugin configuration."
    if config.has_key("load_plugins"):
        from Pyblosxom import plugin_utils
        plugin_utils.initialize_plugins(config.get("plugin_dirs", []),
                                        config.get("load_plugins", []))

        no_verification_support = []

        for mem in plugin_utils.plugins:
            if "verify_installation" in dir(mem):
                print "=== plugin: '%s'" % mem.__name__
                ret = mem.verify_installation(request)
                if ret == 1:
                    print "    PASS"
                else:
                    print "    FAIL!!!"
            else:
                no_verification_support.append(mem.__name__)

        if len(no_verification_support) > 0:
            print ""
            print "The following plugins do not support installation verification:"
            for mem in no_verification_support:
                print "   %s" % mem
    else:
        print "You have chosen not to load any plugins."


# vim: shiftwidth=4 tabstop=4 expandtab
