#######################################################################
# This is placed in the Public Domain.
#######################################################################

"""
Summary
=======

Generates a calendar along the lines of this one (with month and day names in
the configured locale)::

    <   January 2003   >
    Mo Tu We Th Fr Sa Su
           1  2  3  4  5
     6  7  8  9 10 11 12
    13 14 15 16 17 18 19
    20 21 22 23 24 25 26
    27 28 29 30 31

It walks through all your entries and marks the dates that have entries
so you can click on the date and see entries for that date.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.pycalendar`` to your ``load_plugins`` list in your
   ``config.py`` file.

2. Configure it as documented below.

3. Add the ``$(calendar)`` variable to your head and/or foot template.


Configuration
=============

You can set the start of the week using the ``calendar_firstweekday``
configuration setting, for example::

   py['calendar_firstweekday'] = 0

will make the week start on Monday (day '0'), instead of Sunday (day '6').

Pycalendar is locale-aware.  If you set the ``locale`` config property,
then month and day names will be displayed according to your locale.

It uses the following CSS classes:

* blosxomCalendar: for the calendar table
* blosxomCalendarHead: for the month year header (January 2003)
* blosxomCalendarWeekHeader: for the week header (Su, Mo, Tu, ...)
* blosxomCalendarEmpty: for filler days
* blosxomCalendarCell: for calendar days that aren't today
* blosxomCalendarBlogged: for calendar days that aren't today that
  have entries
* blosxomCalendarSpecificDay: for the specific day we're looking at
  (if we're looking at a specific day)
* blosxomCalendarToday: for today's calendar day

"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2011-10-23"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Displays a calendar on your blog."
__category__ = "date"
__license__ = "Public domain"
__registrytags__ = "1.4, 1.5, core"


import time
import calendar
import string

from Pyblosxom import tools
from Pyblosxom.memcache import memcache_decorator


def verify_installation(request):
    # there's no configuration needed for this plugin.
    return True


class PyblCalendar:
    def __init__(self, request):
        self._request = request
        self._cal = None

        self._today = None
        self._view = None
        self._specificday = None

        self._entries = {}

    @memcache_decorator('pycalendar', True)
    def __str__(self):
        """
        Returns the on-demand generated string.
        """
        if self._cal == None:
            self.generate_calendar()

        return self._cal

    def generate_calendar(self):
        """
        Generates the calendar.  We'd like to walk the archives
        for things that happen in this month and mark the dates
        accordingly.  After doing that we pass it to a formatting
        method which turns the thing into HTML.
        """
        config = self._request.get_configuration()
        data = self._request.get_data()
        entry_list = data["entry_list"]

        root = config["datadir"]
        baseurl = config.get("base_url", "")

        self._today = time.localtime()

        if len(entry_list) == 0:
            # if there are no entries, we shouldn't even try to
            # do something fancy.
            self._cal = ""
            return

        view = list(entry_list[0]["timetuple"])

        # this comes in as '', 2001, 2002, 2003, ...  so we can convert it
        # without an issue
        temp = data.get("pi_yr")
        if not temp:
            view[0] = int(self._today[0])
        else:
            view[0] = int(temp)

        # the month is a bit harder since it can come in as "08", "", or
        # "Aug" (in the example of August).
        temp = data.get("pi_mo")
        if temp and temp.isdigit():
            view[1] = int(temp)
        elif temp and temp in tools.month2num:
            view[1] = int(tools.month2num[temp])
        else:
            view[1] = int(self._today[1])

        self._view = view = tuple(view)

        # if we're looking at a specific day, we figure out what it is
        if data.get("pi_yr") and data.get("pi_mo") and data.get("pi_da"):
            if data["pi_mo"].isdigit():
                mon = data["pi_mo"]
            else:
                mon = tools.month2num[data["pi_mo"]]

            self._specificday = (int(data.get("pi_yr", self._today[0])),
                                 int(mon),
                                 int(data.get("pi_da", self._today[2])))

        archive_list = tools.walk(self._request, root)

        yearmonth = {}

        for mem in archive_list:
            timetuple = tools.filestat(self._request, mem)

            # if we already have an entry for this date, we skip to the
            # next one because we've already done this processing
            day = str(timetuple[2]).rjust(2)
            if day in self._entries:
                continue

            # add an entry for yyyymm so we can figure out next/previous
            year = str(timetuple[0])
            dayzfill = string.zfill(timetuple[1], 2)
            yearmonth[year + dayzfill] = time.strftime("%b", timetuple)

            # if the entry isn't in the year/month we're looking at with
            # the calendar, then we skip to the next one
            if timetuple[0:2] != view[0:2]:
                continue

            # mark the entry because it's one we want to show
            if config.get("static_monthnumbers"):
                datepiece = time.strftime("%Y/%m/%d", timetuple)
            else:
                datepiece = time.strftime("%Y/%b/%d", timetuple)
            self._entries[day] = (baseurl + "/" + datepiece, day)

        # Set the first day of the week (Sunday by default)
        first = config.get('calendar_firstweekday', 6)
        calendar.setfirstweekday(first)

        # create the calendar
        cal = calendar.monthcalendar(view[0], view[1])

        # insert the days of the week
        cal.insert(0, calendar.weekheader(2).split())

        # figure out next and previous links by taking the dict of
        # yyyymm strings we created, turning it into a list, sorting
        # them, and then finding "today"'s entry.  then the one before
        # it (index-1) is prev, and the one after (index+1) is next.
        keys = list(yearmonth.keys())
        keys.sort()
        thismonth = time.strftime("%Y%m", view)

        # do some quick adjustment to make sure we didn't pick a
        # yearmonth that's outside the yearmonths of the entries we
        # know about.
        if thismonth in keys:
            index = keys.index(thismonth)
        elif len(keys) == 0 or keys[0] > thismonth:
            index = 0
        else:
            index = len(keys) - 1

        # build the prev link
        if index == 0 or len(keys) == 0:
            prev = None
        else:
            prev = ("%s/%s/%s" % (baseurl, keys[index - 1][:4],
                                  yearmonth[keys[index - 1]]),
                    "&lt;")

        # build the next link
        if index == len(yearmonth) - 1 or len(keys) == 0:
            next = None
        else:
            next = ("%s/%s/%s" % (baseurl, keys[index + 1][:4],
                                  yearmonth[keys[index + 1]]),
                    "&gt;")

        # insert the month name and next/previous links
        cal.insert(0, [prev, time.strftime("%B %Y", view), next])

        self._cal = self.format_with_css(cal)

    def _fixlink(self, link):
        if link:
            return "<a href=\"%s\">%s</a>" % (link[0], link[1])
        else:
            return " "

    def _fixday(self, day):
        if day == 0:
            return "<td class=\"blosxomCalendarEmpty\">&nbsp;</td>"

        strday = str(day).rjust(2)
        if strday in self._entries:
            entry = self._entries[strday]
            link = "<a href=\"%s\">%s</a>" % (entry[0], entry[1])
        else:
            link = strday

        td_class_str = ""

        # if it's today
        if (self._view[0], self._view[1], day) == self._today[0:3]:
            td_class_str += "blosxomCalendarToday "

        if self._specificday:
        # if it's the day we're viewing
            if (self._view[0], self._view[1], day) == self._specificday:
                td_class_str += "blosxomCalendarSpecificDay "

        # if it's a day that's been blogged
        if strday in self._entries:
            td_class_str += "blosxomCalendarBlogged"

        if td_class_str != "":
            td_class_str = "<td class=\"" + td_class_str + "\">%s</td>" % link
        else:
            td_class_str = "<td class=\"blosxomCalendarCell\">%s</td>" % strday

        return td_class_str

    def _fixweek(self, item):
        return "<td class=\"blosxomCalendarWeekHeader\">%s</td>" % item

    def format_with_css(self, cal):
        """
        This formats the calendar using HTML table and CSS.  The output
        can be made to look prettier.
        """
        cal2 = ["<table class=\"blosxomCalendar\">"]
        cal2.append("<tr>")
        cal2.append("<td align=\"left\">" + self._fixlink(cal[0][0]) +
                    "</td>")
        cal2.append(
            '<td colspan="5" align="center" class="blosxomCalendarHead">' +
            cal[0][1] + '</td>')
        cal2.append("<td align=\"right\">" + self._fixlink(cal[0][2]) +
                    "</td>")
        cal2.append("</tr>")

        cal2.append("<tr>%s</tr>" %
                    "".join([self._fixweek(m) for m in cal[1]]))

        for mem in cal[2:]:
            mem = [self._fixday(m) for m in mem]
            cal2.append("<tr>" + "".join(mem) + "</tr>")

        cal2.append("</table>")

        return "\n".join(cal2)


def cb_prepare(args):
    request = args["request"]
    data = request.get_data()
    if data.get('entry_list', None):
        data["calendar"] = PyblCalendar(request)
