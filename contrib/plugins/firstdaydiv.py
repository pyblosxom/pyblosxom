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

Questions, comments, concerns?  Email bwinton@latte.ca for help.
"""
__author__ = "Blake Winton - bwinton@latte.ca"
__version__ = "$Id$"


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
