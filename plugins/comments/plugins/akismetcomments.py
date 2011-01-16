# Copyright (C) 2006 Benjamin Mako Hill <mako@atdot.cc>
#                    Blake Winton <bwinton+blog@latte.ca>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
# USA

"""
Run comments and trackbacks through Akismet (http://akismet.com/ ) to see
whether to reject them or not.

To use this plugin, you must also install akismet.py in your python path (in
the PyBlosxom plugin directory is fine):
http://www.voidspace.org.uk/python/modules.shtml#akismet

Additionally, you will need to get a Wordpress.com API key::

   http://faq.wordpress.com/2005/10/19/api-key/

Then, use this key to put put the following line into your
config.py file::

   py['akismet_api_key'] = 'MYKEYID'

Additionally, if you haven't set it already, you will need to set::

   py['base_url'] = 'mybaseurl'

If a comment is rejected, a message explaining this will saved in a
variable. You can place this into your template using the standard
``$(comment_message)`` variable.

This plugin merges the work done on the akismetComments.py Plugin by
Blake Winton with the the akismet.py plugin by Benjamin Mako Hill.
"""
__author__      = "Benjamin Mako Hill"
__version__     = "0.2"
__url__         = "http://mako.cc/projects/pyblosxom"
__description__ = "Run comments through Akismet."

import sys
import time

def verify_installation(request):
    try:
        from akismet import Akismet
    except ImportError:
        print >>sys.stderr, "Missing module 'akismet'.",
      	return False

    config = request.get_configuration()
 
    # try to check to se make sure that the config file has a key
    if not config.has_key("akismet_api_key"):
        print >>sys.stderr, "Missing required configuration value 'akismet_key'",
        return False

    try:
        from akismet import Akismet
        a = Akismet(config['akismet_api_key'], config['base_url'],
                    agent='PyBlosxom/1.3')
        if not a.verify_key():
            print >>sys.stderr, "Could not verify akismet API key.",
            return False
    except ImportError:
        print "Unknown error loading Akismet module!",
        return False

    return True

def cb_comment_reject(args):
    from akismet import Akismet, AkismetError

    request = args['request']
    comment = args['comment']
    config = request.get_configuration()

    reqdata = request.get_data()
    http = request.get_http()

    fields = {'comment': 'description',
              'comment_author_email': 'email',
              'comment_author': 'author',
              'comment_author_url': 'link',
              'comment_type': 'type',
              }
    data = {}
    for field in fields:
        if comment.has_key(fields[field]):
            data[field] = ""
            for char in list(comment[fields[field]]):
                try:
                    char.encode('ascii')
                # FIXME - bare except--bad!
                except:
                    data[field] = data[field] + "&#" + str(ord(char)) + ";"
                else:
                    data[field] = data[field] + char

    if not data.get('comment'):
        print >>sys.stderr, "Comment info not enough.",
        return False
    body = data['comment']

    if 'ipaddress' in comment:
        data['user_ip'] = comment['ipaddress']
    data['user_agent'] = http.get('HTTP_USER_AGENT','')
    data['referrer'] = http.get('HTTP_REFERER','')

    api_key = config.get('akismet_api_key')
    base_url = config.get('base_url')

    # initialize the api
    api = Akismet(api_key, base_url, agent='PyBlosxom/1.3')

    if not api.verify_key():
        print >>sys.stderr, "Could not verify akismet API key. Comments accepted.",
        return False

    # false is ham, true is spam
    try:
        if api.comment_check(body, data):
            print >>sys.stderr, "Rejecting comment",
            return (True, 'I\'m sorry, but your comment was rejected by the <a href="http://akismet.com/">Akismet</a> spam filtering system.')

        else:
            return False
    except AkismetError:
        print >>sys.stderr, "Rejecting comment (AkismetError)",
        return (True, "Missing essential data (e.g., a UserAgent string).")

# akismet can handle trackback spam too
cb_trackback_reject = cb_comment_reject
