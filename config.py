py = {}
# What's this blog's title?
py['blog_title'] = "Another pyblosxom blog"

# What's this blog's description (for outgoing RSS feed)?
py['blog_description'] = "blosxom with a touch of python"

# What's this blog's primary language (for outgoing RSS feed)?
py['blog_language'] = "en"

# Where are this blog's entries kept?
py['datadir'] = "/path/to/blog"

# Should I stick only to the datadir for items or travel down the directory
# hierarchy looking for items?  If so, to what depth?
# 0 = infinite depth (aka grab everything), 1 = datadir only, n = n levels down
py['depth'] = 0

# How many entries should I show on the home page?
py['num_entries'] = 40

# Trackback data directory (If you install Standalone Trackback Tool)
#py['tb_data'] = '/path/to/tb_data/directory'

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


# XML-RPC data
xmlrpc = {}
# Username to access this server
xmlrpc['username'] = 'someusername'
# Password to access this server
xmlrpc['password'] = 'somepassword'

__author__ = 'Wari Wahab <wari@wari.per.sg>'
__version__ = "CVS"
__date__ = "$Date$"
__revision__ = "$Revision$"
__copyright__ = "Copyright (c) 2003 Wari Wahab"
__license__ = "Python"
py['pyblosxom_version'] = __version__
py['pyblosxom_name'] = 'pyblosxom'
