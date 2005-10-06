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

# What's this blog's author name?
py['blog_author'] = "name"

# What's the blog author's email address?
py["blog_email"] = "email@blah.com"

# What's this blog's primary language (for outgoing RSS feed)?
py['blog_language'] = "en"

# Encoding for output. Default is iso-8859-1.
py['blog_encoding'] = "iso-8859-1"

# These are the rights you give to others in regards to the content
# on your blog.  Generally, this is the copyright information.
# This is used in the Atom feeds.  Leaving this blank or not filling
# it in correctly could result in a feed that doesn't validate.
py["blog_rights"] = "Copyright 2005 Joe Bobb"

# Where are this blog's entries kept?
py['datadir'] = "/path/to/blog"

# Where should PyBlosxom log files be kept?
py['logdir'] = "/path/to/logdir"

# Where should the application log to?
# If set to "NONE" log messages are silently ignored.
# Falls back to sys.stderr if the file can't be opened for writing.
py['log_file'] = "/path/to/pyblosxom.log"

# At what level should we log to log_file?
# One of: critical, error, warning, info, debug
# For production 'warning' or 'error' is recommended.
py['log_level'] = "warning"

# Let's you specify which channels should be logged.
# If specified, only messages from the listed channels are logged.
# Each plugin logs to it's own channel, therefor channelname == pluginname.
# Application level messages are logged to a channel named 'root'.
# If you use log_filter and ommit the 'root' channel here, app level messages 
# are not logged! log_filter is mainly interesting to debug a specific plugin.
#py['log_filter'] = ['root', 'plugin1', 'plugin2']

# List of strings with directories that should be ignored (e.g. "CVS")
# ex: py['ignore_directories'] = ["CVS", "temp"]
py['ignore_directories'] = []

# Should I stick only to the datadir for items or travel down the directory
# hierarchy looking for items?  If so, to what depth?
# 0 = infinite depth (aka grab everything), 1 = datadir only, n = n levels down
py['depth'] = 0

# How many entries should I show on the home page?
py['num_entries'] = 40

# What should the default flavour you want used be?
py['default_flavour'] = "html"


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
# Example: py['plugin_dirs'] = ['/opt', '/usr/bin']
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


# Doing static rendering?  Static rendering essentially "compiles" your
# blog into a series of static html pages.  For more details, read:
# http://wiki.subtlehints.net/moin/PyBlosxom_2fStaticRendering
# 
# What directory do you want your static html pages to go into?
#py["static_dir"] = "/path/to/static/dir"

# What flavours shouldt get generated?
#py["static_flavours"] = ["html"]

# What other paths should we statically render?
# This is for additional urls handled by other plugins like the booklist
# and plugin_info plugins.  If there are multiple flavours you want
# to capture, specify each:
# ex: py["static_urls"] = ["/booklist.rss", "/booklist.html"]
#py["static_urls"] = ["/path/to/url1", "/path/to/url2"]

# Whether (1) or not (0) you want to create date indexes using month
# names?  (ex. /2004/Apr/01)  Defaults to 1 (yes).
#py["static_monthnames"] = 1
# Whether (1) or not (0) you want to create date indexes using month
# numbers?  (ex. /2004/04/01)  Defaults to 0 (no).
#py["static_monthnumbers"] = 0
