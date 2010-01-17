# vim: tabstop=4 shiftwidth=4
"""
If a filename contains a timestamp in the form of YYYY-MM-DD-hh-mm,
change the mtime to be the timestamp instead of the one kept by the
filesystem.  For example, a valid filename would be
foo-2002-04-01-00-00.txt for April fools day on the year 2002.
It is also possible to use timestamps in the form of YYYY-MM-DD

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

Copyright 2004, 2005 Tim Roberts
"""
import os, re, time

__author__ = 'Tim Roberts http://www.probo.com/timr/blog/'
__version__ = '$Id$'

DAYMATCH = re.compile('([0-9]{4})-([0-1][0-9])-([0-3][0-9])(-([0-2][0-9])-([0-5][0-9]))?.[\w]+$')

def cb_filestat(args):
    filename = args["filename"]
    stattuple = args["mtime"]
    
    mtime = 0
    mtch = DAYMATCH.search(os.path.basename(filename))
    if mtch:
        try:
            year = int(mtch.group(1))
            mo = int(mtch.group(2))
            day = int(mtch.group(3))
            if mtch.group(4) is None:
                hr = 0
                minute = 0
            else:
                hr = int(mtch.group(5))
                minute = int(mtch.group(6)) 
            mtime = time.mktime((year,mo,day,hr,minute,0,0,0,-1))
        except StandardError:
            # TODO: Some sort of debugging code here?
            pass

    if mtime: 
        args["mtime"] = tuple(list(stattuple[:8]) + [mtime] + list(stattuple[9:]))

    return args
