#!/usr/bin/env python

#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003 - 2007 Wari Wahab
# 
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#
# $Id: pyblosxom.py 913 2006-08-08 20:29:42Z willhelm $
#######################################################################

import os, sys

# this allows for a config.py override
script = os.environ.get('SCRIPT_FILENAME', None)
if script is not None:
    sys.path.insert(0, os.path.dirname(script))
sys.path.insert(0, os.getcwd())

from Pyblosxom.commandline import command_line_handler

if __name__ == '__main__':
    sys.exit(command_line_handler("pyblcmd", sys.argv))
