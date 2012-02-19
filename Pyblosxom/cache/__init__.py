#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Pyblosxom works by pulling data from the file system, passing it through
a series of filters and transformations, and then rendering it.  Some
of these steps are somewhat intensive and to alleviate this, we cache
things.

For example, the entries.base.BaseEntry class allows entries to be
cached after they've been pulled from the file system and passed
through a series of filters/formatters.

There are several cache mechanisms.  Read the documentation for each
to understand how they work and how to set them up.  Additional caching
mechanisms can be dropped in this directory and used by setting the
"cacheDriver" item in the config dict.
"""
pass
