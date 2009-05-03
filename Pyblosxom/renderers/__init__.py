#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2003, 2004, 2005, 2006 Wari Wahab
#
# PyBlosxom is distributed under the MIT license.  See the file LICENSE
# for distribution details.
#######################################################################
"""
The end of the PyBlosxom request lifecycle involves rendering the
entries we've decided we want to render.  This is the job of the
renderers.  They handle pulling in templates, expanding variables,
formatting entries into stories, and then outputting it to stdout
(or wherever) for final output.

Creating a new renderer involves dropping a new module in this
directory and adjusting your config file to use your new module.
"""
pass
