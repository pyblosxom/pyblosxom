"""
This is my fancy module to add a token which tells us whether we're
the first day being displayed or not.

To install:
 1. Copy this file into your pyblosxom/Pyblosxom/plugins directory.

 2. Create a file named date_head.html in your datadir containing::

    <div class="$dayDivClass">
    <span class="blosxomDate">$date</span>

 3. Edit your config.py and add the line::

    py['firstDayDiv'] = 'blosxomFirstDayDiv'

 4. That's it.  You're done.

Questions, comments, concerns?  Email bwinton at latte dot ca for help.


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

Copyright 2004, 2005 Blake Winton
"""
__author__ = "Blake Winton - bwinton@latte.ca"
__version__ = "$Id$"
__url__ = "http://pyblosxom.sourceforge.net/"
__description__ = "Adds a token which tells us whether we're the first day being displayed or not."

class PyFirstDate:
    """
    This class stores the state needed to determine whether we're
    supposed to return the first-day-div class or the
    not-the-first-day-div class.

    @type _dayDiv: string
    @ivar _dayDiv: The davDiv class to return.
    @type _count: int
    @ivar _count: The number of times we've been called (currently 0 or 1)
    """
    def __init__(self, request):
        """
        Initialize the PyFirstDate class.

        @type request: L{Pyblosxom.pyblosxom.Request} object
        @param request: A reference to the L{Pyblosxom.pyblosxom.Request} object.
        """
        config = request.getConfiguration()
        self._dayDiv = config.get("firstDayDiv", "blosxomDayDiv")
        self._count = 0

    def __str__(self):
        """
        Get a string representing the current state of this
        object.

        @rtype: string
        @return: the user-specified firstDayDiv if it's the first
                 time we're called, or "blosxomDayDiv" if it's not.
        """
        if self._count == 0:
            self._count = 1
        else:
            self._dayDiv = "blosxomDayDiv"
        return self._dayDiv

def cb_prepare(args):
    """
    Populate the L{Pyblosxom.pyblosxom.Request} with an instance of the
    L{PyFirstDate} class in the "dayDivClass" key.
    """
    request = args["request"]

    data = request.getData()
    data["dayDivClass"] = PyFirstDate(request)
