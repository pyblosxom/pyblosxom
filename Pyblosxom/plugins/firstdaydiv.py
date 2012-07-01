#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2004, 2005 Blake Winton
# Copyright (c) 2010, 2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

Adds a token which allows you to differentiate between the first day
of entries in a series of entries to be displayed from the other days.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. In your ``config.py`` file, add ``Pyblosxom.plugins.firstdaydiv``
   to the ``load_plugins`` list.

2. (optional) Set the ``firstDayDiv`` config variable.  This defaults
   to ``blosxomFirstDayDiv``.

   Example::

      py['firstDayDiv'] = 'blosxomFirstDayDiv'


Usage
=====

This denotes the first day with the css class set in the
``firstDayDiv`` config variable.  This is available in the
``$(dayDivClass)`` template variable.  You probably want to put this
in your ``date_head`` template in a ``<div...>`` tag.

For example, in your ``date_head``, you could have::

   <div class="$dayDivClass">
   <span class="blosxomDate">$date</span>

and in your ``date_foot``, you'd want to close that ``<div>`` off::

   </div>

Feel free to use this in other ways.
"""

__author__ = "Blake Winton"
__email__ = "bwinton@latte.ca"
__version__ = "2011-10-22"
__url__ = "http://pyblosxom.github.com/"
__description__ = ("Adds a token which tells us whether "
                   "we're the first day being displayed or not.")
__category__ = "date"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


class PyFirstDate:
    """
    This class stores the state needed to determine whether we're
    supposed to return the first-day-div class or the
    not-the-first-day-div class.

    """
    def __init__(self, request):
        config = request.get_configuration()
        self._day_div = config.get("firstDayDiv", "blosxomFirstDayDiv")
        self._count = 0

    def __str__(self):
        if self._count == 0:
            self._count = 1
        else:
            self._day_div = "blosxomDayDiv"
        return self._day_div


def cb_prepare(args):
    """
    Populate the ``Pyblosxom.pyblosxom.Request`` with an instance of
    the ``PyFirstDate`` class in the ``dayDivClass`` key.

    """
    request = args["request"]

    data = request.get_data()
    data["dayDivClass"] = PyFirstDate(request)
