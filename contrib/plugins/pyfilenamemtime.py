# vim: tabstop=4 shiftwidth=4
"""
If a filename contains a timestamp in the form of YYYY-MM-DD-hh-mm,
change the mtime to be the timestamp instead of the one kept by the
filesystem.  For example, a valid filename would be
foo-2002-04-01-00-00.txt for April fools day on the year 2002
"""
import os, re, time

__author__ = 'Tim Roberts http://www.probo.com/timr/blog/'
__version__ = '$Id$'

DAYMATCH = re.compile('([0-9]{4})-([0-1][0-9])-([0-3][0-9])-([0-2][0-9])-([0-5][0-9])')

def cb_prepare(args):
    request = args["request"]
    data = request.getData()

    entries = data["entry_list"]

    adj = 0

    for mem in entries:
        if mem.has_key("fn"):
            mtch = DAYMATCH.search(mem["fn"])
            mtime = 0
            if mtch:
                try:
                    year = int(mtch.groups()[0])
                    mo = int(mtch.groups()[1])
                    day = int(mtch.groups()[2])
                    hr = int(mtch.groups()[3])
                    minute = int(mtch.groups()[4]) 
                    mtime = time.mktime((year,mo,day,hr,minute,0,0,0,-1))
                except:
                    # TODO: Some sort of debugging code here?
                    pass

            if mtime and hasattr(mem, "setTime"):
                mem.setTime(time.localtime(mtime))
                adj = 1
                mem["adjusted_mtime"] = "1"

    if adj == 1:
        entrylist = [ (m._mtime, m) for m in entries ]
        entrylist.sort()
        entrylist.reverse()
        entrylist = [x[1] for x in entrylist]
        data["entry_list"] = entrylist
        
