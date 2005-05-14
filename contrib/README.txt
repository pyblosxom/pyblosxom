1. SUMMARY
==========

This document covers what you'll find in the contributed plugins pack
and also rules for developers who want to include their plugins in
the pack.


2. INCLUDED HERE
================

contrib/
  |-entryparsers/        -- holds entryparsers
  |-plugins/             -- holds pyblosxom plugins
  |   |-comments/        -- holds comments-related pieces
  |   |-lucene/          -- holds lucene pieces
  |   |-preformatters/   -- holds preformatters
  |
  |-xmlrpc_plugins/      -- holds xmlrpc plugins


With all of these files, refer to the top of the file for documentation
and information on installation, usage, and ownership.


2.1 Entryparsers
----------------
  py.py     - parses blog entries in python format
  rst.py    - parses blog entries in reST format
  txtl.py   - parses blog entries in Textile format

2.2 Plugins
-----------
  conditionalhttp.py         - kicks up a 304 if the page hasn't been modified
  firstdaydiv.py             - adds a variable to let you know if the story
                               being rendered is the first one or not
  logrequest.py              - logs requests
  logstats.py                - logs referrers
  pyarchives.py              - displays a list of archive urls
  pycalendar.py              - displays a calendar
  pycategories.py            - displays categories
  pyfilenametime.py          - allows you to set the mtime of an entry with
                               the file name
  standalonetrackbacktool.py - works with the standalone trackback tool
  w3cdate.py                 - builds w3c dates
  weblogsping.py             - pings weblogs.com and blo.gs with every
                               new entry

2.3 Comments
------------
  comments.py         - comments functionality
  trackback.py        - trackback functionality
  xmlrpc_pingback.py  - pingback (requires xmlrpc.py)

2.4 Lucene
----------
  lucene.py           - blog search engine

2.5 Preformatters
-----------------
  linebreaks.py       - changes CRLF to <br>
  moinmoin.py         - formats blog entries in moin format

2.6 XMLRPC plugins
------------------
  xmlrpc.py            - required plugin for any xmlrpc plugins
  xmlrpc_blogger.py    - implements the blogger xmlrpc interface
  xmlrpc_metaweblog.py - implements the metaweblog xmlrpc interface


REQUIREMENTS FOR PLUGINS
========================

All plugins must have the following items in order to be included
in the contributed package:

   1. a description of what the plugin does
   2. instructions on how to configure and install the plugin
   3. licensed under an appropriate license (GPL, MIT, or BSD)
   4. your name and contact information


Additionally, all plugins should have the following items:

   1. version information
   2. revision history
   3. examples of configuration and behavior
   4. url for a web-page that's related to the plugin or its development
   5. verify_installation code to help the user verify that the plugin
      is configured correctly


MUST HAVE REQUIREMENT DETAILS
=============================

1. Description of what the code does.

   The plugin must have a doc-string at the top of the plugin code file
   which clearly describes what the plugin does.

2. Instructions on how to configure and install the plugin

3. Licensed under an appropriate license (GPL, MIT, or BSD)

   The plugin must be under the GPL, MIT or BSD licenses and the license
   that the plugin is licensed under must be explicitly stated in the
   doc-string at the top of the plugin code file.  For example, you
   could toss the following text into the doc-string at the top of your
   plugin file (MIT license):


   Permission is hereby granted, free of charge, to any person
   obtaining a copy of this software and associated documentation
   files (the "Software"), to deal in the Software without restriction,
   including without limitation the rights to use, copy, modify,
   merge, publish, distribute, sublicense, and/or sell copies of the
   Software, and to permit persons to whom the Software is furnished
   to do so, subject to the following conditions:
   
   The above copyright notice and this permission notice shall be
   included in all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
   CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.


   Note, you can license your code under multiple licenses.  We can only
   distribute plugins that are licensed under the GPL, MIT, or BSD 
   licenses.


4. Your name and contact information

   After the doc-string at the top of your plugin, add the following line
   (and since it's Python code, it must be left-aligned):

   __author__ = "Your Name <your email address>"

   If you don't want people to contact you by email, then don't include
   your email address, but you must include some way for people to contact
   you somewhere in the doc-string at the top of the plugin code file.

   If there's no way to contact you, there's no way for us to notify you
   of issues.


SHOULD HAVE REQUIREMENT DETAILS
===============================

1. Version information

   Having version information in the file makes it a lot easier for us
   (and you) to track bugs since those bugs will exist in specific versions
   of the plugin and may be fixed over time.

   Include the following line:

   __version__ = "version #.# <date of release>"


2. Revision history

3. Examples of configuration and behavior

4. URL for a web-page that's related to the plugin or its development

5. verify_installation code to help the user verify that the plugin
   is configured correctly
