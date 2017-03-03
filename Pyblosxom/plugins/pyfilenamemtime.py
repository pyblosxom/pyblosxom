#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2004, 2005 Tim Roberts
# Copyright (c) 2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

Allows you to specify the mtime for a file in the file name.

If a filename contains a timestamp in the form of
``YYYY-MM-DD-hh-mm``, change the mtime to be the timestamp instead of
the one kept by the filesystem.

For example, a valid filename would be ``foo-2002-04-01-00-00.txt``
for April fools day on the year 2002.  It is also possible to use
timestamps in the form of ``YYYY-MM-DD``.

http://www.probo.com/timr/blog/


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.pyfilenamemtime`` to the ``load_plugins``
   list of your ``config.py`` file.

2. Use date stamps in your entry filenames.

"""

__author__ = "Tim Roberts"
__email__ = ""
__version__ = "2011-10-23"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Allows you to codify the mtime in the filename."
__category__ = "date"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


import os
import re
import time

from Pyblosxom import tools
from Pyblosxom.memcache import memcache_decorator

DAYMATCH = re.compile(
    '([0-9]{4})-'
    '([0-1][0-9])-'
    '([0-3][0-9])'
    '(-([0-2][0-9])-([0-5][0-9]))?.[\w]+$')

@memcache_decorator('pyfilenamemtime')
def get_mtime(filename):
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
            mtime = time.mktime((year, mo, day, hr, minute, 0, 0, 0, -1))
        except Exception:
            # TODO: Some sort of debugging code here?
            pass
        return mtime
    return None


def cb_filestat(args):
    filename = args["filename"]
    stattuple = args["mtime"]
    
    mtime = get_mtime(filename)

    if mtime is not None:
        args["mtime"] = (
            tuple(list(stattuple[:8]) + [mtime] + list(stattuple[9:])))

    return args
