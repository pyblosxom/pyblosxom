#!/usr/bin/env python
# vim: shiftwidth=4 tabstop=4 expandtab
"""
This utility can be used to update a file entry while keeping the
timestamp intact. This is very useful for blog entries that are time
critical and you do not wish the time to get updated in any way.

Since this utility works like a wrapper for you favourite editor,
replace the EDITOR line below to reflect the command to your favourite
editor, be it nano, pico or bbedit, etc. Tested on un*x only.


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

Copyright 2004, 2005 Wari Wahab
"""
__version__ = "$Id$"

EDITOR='vim -c "set tabstop=4 shiftwidth=4 expandtab"'
from os import environ
EDITOR=environ.get('VISUAL')

from os import stat, path, spawnl, utime, P_WAIT
import sys, time

if len(sys.argv) > 1:
   filename = sys.argv[1]
   print "Editing file %s" % filename
else:
   filename = raw_input("filename? ")

if not filename:
   print "No filename given.  Quitting."
   sys.exit(1)

try:
   filestats = stat(filename)
except:
   print "File not found.  Quitting."
   sys.exit(1)

atime, mtime = filestats[7:9]

spawnl(P_WAIT, EDITOR, EDITOR, filename)

print "Setting back the time"
try:
   utime(filename, (atime, mtime))
except Exception, e:
   print "Failed to set the new time.", e
   print "Quitting."
   sys.exit(1)
