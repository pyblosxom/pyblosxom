py = {}
# What's this blog's title?
py['blog_title'] = "Another pyblosxom blog"

# What's this blog's description (for outgoing RSS feed)?
py['blog_description'] = "blosxom with a touch of python"

# What's this blog's primary language (for outgoing RSS feed)?
py['blog_language'] = "en"

# Where are this blog's entries kept?
py['datadir'] = "/path/to/blog"

# What should this blog use as its base url?
# py['base_url'] = "http://www.some.host/weblog"

# Should I stick only to the datadir for items or travel down the directory
# hierarchy looking for items?  If so, to what depth?
# 0 = infinite depth (aka grab everything), 1 = datadir only, n = n levels down
py['depth'] = 0

# How many entries should I show on the home page?
py['num_entries'] = 40

# Default parser/preformatter. Defaults to plain (does nothing)
#py['parser'] = 'plain'

# Using Caching? Caching speeds up rendering the page that is going to be
# shown. Even if you are not using pyblosxom special features, caching can
# improve rendering speed of certain flavours that can show a large number of
# files at one time. Choose a cache mechanism you'd like, see the libs/cache/
# directory, and read the source on how to enable caching with the particular
# cache driver, you need to set two variables:
#py['cacheDriver'] = 'xxxx'
#py['cacheConfig'] = ''

# There are two ways for PyBlosxom to load plugins.  The first is the
# default way which involves loading all the plugins in the lib/plugins
# directory in alphanumeric order.  The second is by specifying a
# "load_plugins" key here.  Doing so will cause us to load only the
# plugins you name and we will load them in the order you name them.
# The "load_plugins" key is a list of strings where each string is
# the name of a plugin module (i.e. the filename without the .py at
# the end).
# ex: py['load_plugins'] = ["pycalendar", "pyfortune", "pyarchives"]
# py['load_plugins'] = []

# XML-RPC data
xmlrpc = {}
# Username and password to access this server, you can define one or more
#xmlrpc['usernames'] = {'someuser': 'somepassword'}

__author__ = 'Wari Wahab <wari@wari.per.sg>'
__version__ = "CVS"
__date__ = "$Date$"
__revision__ = "$Revision$"
__copyright__ = "Copyright (c) 2003 Wari Wahab"
__license__ = "Python"
py['pyblosxom_version'] = __version__
py['pyblosxom_name'] = 'pyblosxom'
