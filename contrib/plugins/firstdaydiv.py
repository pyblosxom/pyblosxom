"""
This is my fancy module to add a token which tells us whether we're the first
day being displayed or not. Displays the first date header with a different
class from the rest, using CSS.

To install:
1) Copy this file into your pyblosxom/libs/plugins directory.
2) Create a file named date_head.html in your datadir containing:
   ------------------------
   <div class="$dayDivClass">
   <span class="blosxomDate">$date</span>
   ------------------------
   (without the leading spaces, or the lines of dashs).
3) Edit your config.py and add the line:
   py['firstDayDiv'] = 'blosxomFirstDayDiv'
4) That's it.  You're done.

For example of what this plugin can do, view the source of
http://www.latte.ca/weblog/

Questions, comments, concerns?  Email bwinton@latte.ca for help.
"""
class PyFirstDate:
    def __init__(self, py):
        self._py = py
        self._dayDiv = self._py.get("firstDayDiv", "blosxomDayDiv");
        self._count = 0

    def __str__(self):
        if self._count == 0:
            self._count = 1;
        else:
            self._dayDiv = "blosxomDayDiv"
        return self._dayDiv

def load(py, entryList):
    py["dayDivClass"] = PyFirstDate(py)

if __name__ == '__main__':
    pass
