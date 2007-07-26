#!/usr/bin/env python

# -u turns off character translation to allow transmission
# of gzip compressed content on Windows and OS/2
#!/path/to/python -u

# Uncomment this if something goes wrong (for debugging)
#import cgitb; cgitb.enable()


# You shouldn't have to adjust anything below this line.
# ------------------------------------------------------

import os, sys

# this allows for a config.py override
script = os.environ.get('SCRIPT_FILENAME', None)
if script is not None:
    script = script[0:script.rfind("/")]
    sys.path.insert(0, script)

# this allows for grabbing the config based on the DocumentRoot
# setting if you're using apache
root = os.environ.get('DOCUMENT_ROOT', None)
if root is not None:
    sys.path.insert(0, root)

# Settings are now in config.py, you should disable access to it by htaccess
# (make it executable or deny access)
from config import py as cfg

# If the user defined a "codebase" property in their config file,
# then we insert that into our sys.path because that's where the
# PyBlosxom installation is.
if cfg.has_key("codebase"):
    sys.path.insert(0, cfg["codebase"])

from Pyblosxom.pyblosxom import run_pyblosxom

if __name__ == '__main__':
    run_pyblosxom()
