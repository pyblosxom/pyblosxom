# vim: tabstop=4 shiftwidth=4
from libs import api
import os, re, time

DAYMATCH = re.compile('([0-9]{4})-([0-1][0-9])-([0-3][0-9])-([0-2][0-9])-([0-5][0-9]).txt')

def filestat(args):
    filename = args["filename"]
    stattuple = args["mtime"]
    
    mtime = 0
    mtch = DAYMATCH.match(os.path.basename(filename))
    if mtch:
        try:
            timetuple = time.strptime("-".join(mtch.groups()), "%Y-%m-%d-%H-%M")
            mtime = time.mktime(timetuple)
        except:
            pass

    if mtime: 
        args["mtime"] = tuple(list(stattuple[:8]) + [mtime] + list(stattuple[9:]))

    return args

def initialize():
    api.filestat.register(filestat, api.LAST)
