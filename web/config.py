py = {}

###############
# Start Below #
###############
# If your PyBlosxom installation is in a funky place, uncomment
# this next line and point it to your PyBlosxom installation
# directory.
#py["codebase"] = "/path/to/pyblosxom/installation"

# What's this blog's title?
py['blog_title'] = "Another pyblosxom blog"

# What's this blog's description (for outgoing RSS feed)?
py['blog_description'] = "blosxom with a touch of python"

# What's this blog's author name and email?
py['blog_author'] = "name email@blah.com"

# What's this blog's primary language (for outgoing RSS feed)?
py['blog_language'] = "en"

# Encoding for output. Default is iso-8859-1.
py['blog_encoding'] = "iso-8859-1"

# Where are this blog's entries kept?
py['datadir'] = "/path/to/blog"

# Should I stick only to the datadir for items or travel down the directory
# hierarchy looking for items?  If so, to what depth?
# 0 = infinite depth (aka grab everything), 1 = datadir only, n = n levels down
py['depth'] = 0

# How many entries should I show on the home page?
py['num_entries'] = 40


###########################
# Optional Configurations #
###########################

# What should this blog use as its base url?
# py['base_url'] = "http://www.some.host/weblog"

# Default parser/preformatter. Defaults to plain (does nothing)
#py['parser'] = 'plain'

# Using Caching? Caching speeds up rendering the page that is going to be
# shown. Even if you are not using pyblosxom special features, caching can
# improve rendering speed of certain flavours that can show a large number of
# files at one time. Choose a cache mechanism you'd like, see the
# Pyblosxom/cache/ directory, and read the source on how to enable caching with
# the particular cache driver, you need to set two variables:
#py['cacheDriver'] = 'xxxx'
#py['cacheConfig'] = ''

# Plugin directories:
# You can now specify where you plugins all lives, there are two types
# of plugindirectories, the standard pyblosxom plugins, and the xmlrpc
# plugins.  You can list out as many directories you want, but they
# should only contain the related plugins.
# Example: py['load_plugins'] = ['/opt', '/usr/bin']
#py['plugin_dirs'] = ['/path/to/my/plugins']

# There are two ways for PyBlosxom to load plugins.  The first is the
# default way which involves loading all the plugins in the lib/plugins
# directory in alphanumeric order.  The second is by specifying a
# "load_plugins" key here.  Doing so will cause us to load only the
# plugins you name and we will load them in the order you name them.
# The "load_plugins" key is a list of strings where each string is
# the name of a plugin module (i.e. the filename without the .py at
# the end).
# ex: py['load_plugins'] = ["pycalendar", "pyfortune", "pyarchives"]
#py['load_plugins'] = []


###########################
# Nothing to modify below #
###########################
__author__ = 'Wari Wahab <wari at wari dot per dot sg>'
__version__ = "CVS"
__date__ = "$Date$"
__revision__ = "$Revision$"
__copyright__ = "Copyright (c) 2003-2004 Wari Wahab"
__license__ = "MIT License"
py['pyblosxom_version'] = __version__
py['pyblosxom_name'] = 'pyblosxom'
