#!/usr/bin/env python2
"""
This is a script for backdating mtime for blog files.  It allows you to
write an entry today and backdate it to yesterday.


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

Copyright 2004, 2005 Will Guaraldi
"""
import os, time, sys

__author__ = "Will Guaraldi - willg at bluesock dot org"
__version__ = "$Id$"
__url__ = "http://pyblosxom.sourceforge.net/"
__description__ = "Allows you to backdate entries."

if len(sys.argv) > 1:
   filename = sys.argv[1]
else:
   filename = raw_input("filename? ")

if not filename:
   print "No filename given.  Quitting."
   sys.exit(1)

try:
   filestats = os.stat(filename)
except:
   print "File not found.  Quitting."
   sys.exit(1)


print "We take a timeadjustment in seconds.  So if you want the file "
print "to go back 7 days, say \"7 days\"."
timeadj = raw_input("time adjustment? ")
if not timeadj:
   print "No time adjustment given.  Quitting."

timeadj = timeadj.split()

quantity = 0
offset = 0
multiplier = 1
for mem in timeadj:
   if mem.isdigit():
      quantity = int(mem)
   else:
      if mem in ["w", "week", "weeks"]:
         multiplier = 60 * 60 * 24 * 7
      elif mem in ["d", "day", "days"]:
         multiplier = 60 * 60 * 24
      elif mem in ["h", "hour", "hours"]:
         multiplier = 60 * 60
      elif mem in ["m", "min", "mins", "minute", "minutes"]:
         multiplier = 60
      else:
         print "Unrecognized label '%s'.  Quitting."
         sys.exit(1)
      offset = offset + (quantity * multiplier)
      quantity = 0
      multiplier = 1

print "Time adjustment is: %d seconds" % offset

filestats = os.stat(filename)
atime, mtime = filestats[7:9]
print "Old mtime: ", time.asctime(time.localtime(mtime))

mtime = mtime - offset
try:
   os.utime(filename, (atime, mtime))
except Exception, e:
   print "Failed to set the new time.", e
   print "Quitting."
   sys.exit(1)

print "New mtime: ", time.asctime(time.localtime(mtime))
print "Success!"
