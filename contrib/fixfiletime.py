#!/usr/bin/env python2
"""
This is a quick script for fixing the atime/mtime for blog files.
It's often the case that I misspell something or want to add an
update, but because the timestamp for the blog entry comes from
the mtime of the file, I screw it up and cause it to cycle to the
top of my blog again.  Rrrrr....

Anyhow, this allows you to quickly fix that.
"""
import os, time, sys

__author__ = "Will Guaraldi   willg@bluesock.org"

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
