# vim: tabstop=4 shiftwidth=4
"""
Generates a calendar along the lines of this one:

    January 2003
Mo Tu We Th Fr Sa Su
       1  2  3  4  5
 6  7  8  9 10 11 12
13 14 15 16 17 18 19
20 21 22 23 24 25 26
27 28 29 30 31

It walks through all your entries and marks the dates that have entries
so you can click on the date and see entries for that date.

It uses a "calendarstyle" entry in the pyblosxom.ini file under the 
pyblosxom section:

   calendarstyle = pre | css

with default for pre.  In css mode, it has the following CSS things:

   calendarhead

(Should we add more?)
"""
__author__ = "Will Guaraldi - willg@bluesock.org"
__version__ = "$id$"

from libs import tools
import time, os, calendar, sys, string

class PyblCalendar:
	def __init__(self, py):
		self._py = py
		self._cal = None

	def __str__(self):
		"""
		Returns the on-demand generated string.
		"""
		if self._cal == None:
			self.generateCalendar()

		return self._cal

	def generateCalendar(self):
		"""
		Generates the calendar.  We'd like to walk the archives
		for things that happen in this month and mark the dates
		accordingly.  And possibly turn this into a table with
		CSS markup and such.
		"""
		root = self._py["datadir"]
		baseurl = self._py.get("base_url", "")
		markup = self._py.get("calendarstyle", "pre")

		today = time.localtime()


		# this ocmes in as 2001, 2002, 2003, ...  so we can convert it
		# without an issue
		temp = self._py["pi_yr"]
		if temp:
			# today = (int(temp),) + today[1:]
			today = tuple([int(temp)] + list(today)[1:])

		# this comes in as Jan, Feb, ...  so we convert it with a quick
		# lookup for today in there as well
		lookup = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
					"May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
					"Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
					"": today[1]}

		temp = self._py["pi_mo"]
		today = tuple([today[0]] + [lookup[temp]] + list(today)[2:])

		archiveList = tools.Walk(root)

		highlight = {}
		yearmonth = {}

		for mem in archiveList:
			timetuple = time.localtime(os.stat(mem)[8])

			# we keep track of all the ones we got so we can figure
			# out what the previous and next months are
			yearmonth[str(timetuple[0]) + string.zfill(timetuple[1], 2)] = time.strftime("%b", timetuple)

			if timetuple[0] != today[0] or timetuple[1] != today[1]:
				continue

			day = str(timetuple[2]).rjust(2)
			
			if highlight.has_key(day):
				continue

			datepiece = time.strftime("%Y/%b/%d", timetuple)
			highlight[day] = (baseurl + "/" + datepiece, day)


		# create the calendar
		calendar.setfirstweekday(calendar.SUNDAY)
		cal = calendar.monthcalendar(today[0], today[1])
		
		# insert the days of the week
		cal.insert(0, ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"])

		# figure out next and previous links by taking the dict of yyyymm
		# strings we created, turning it into a list, sorting them,
		# and then finding "today"'s entry.  then the one before it 
		# (index-1) is prev, and the one after (index+1) is next.
		keys = yearmonth.keys()
		keys.sort()
		thismonth = time.strftime("%Y%m", today)

		index = keys.index(thismonth)
		if index == 0:
			prev = None
		else:
			prev = (baseurl + "/" + keys[index-1][:4] + "/" + yearmonth[keys[index-1]], "<")

		if index == len(yearmonth)-1:
			next = None
		else:
			next = (baseurl + "/" + keys[index+1][:4] + "/" + yearmonth[keys[index+1]], ">")

		# insert the month name and next/previous links
		cal.insert(0, [prev, time.strftime("%B %Y", today), next])

		if markup == "pre":
			self._cal = self.formatWithPre(highlight, cal)
		elif markup == "css":
			self._cal = self.formatWithCSS(highlight, cal)
		else:
			self._cal = "Invalid calendarstyle '%s'" % markup


	def formatWithCSS(self, highlight, cal):
		"""
		This formats the calendar using HTML table and CSS.  The output
		can be made to look prettier.
		"""
		def fixl(link):
			if link:
				return "<a href=\"%s\">%s</a>" % (link[0], link[1])
			else:
				return " "

		cal2 = ["<table border=\"0\" cellspacing=\"4\" cellpadding=\"0\">"]
		cal2.append("<tr>")
		cal2.append("<td align=\"left\">" + fixl(cal[0][0]) + "</td>")
		cal2.append("<td colspan=\"5\" align=\"center\"><span class=\"calendarhead\">" + cal[0][1] + "</span></td>")
		cal2.append("<td align=\"right\">" + fixl(cal[0][2]) + "</td>")
		cal2.append("</tr>")
		cal2.append("<tr><td>" + "</td><td>".join(cal[1]) + "</td></tr>")

		def fixday(highlight, day):
			if day == 0: return "  "
			day = str(day).rjust(2)
			if highlight.has_key(day):
				return "<a href=\"%s\">%s</a>" % (highlight[day][0], highlight[day][1])
			return day

		for mem in cal[2:]:
			mem = [fixday(highlight, m) for m in mem]
			cal2.append("<tr><td align=\"center\">" + "</td><td align=\"center\">".join(mem) + "</td></tr>")

		cal2.append("</table>")

		return "\n".join(cal2)


	def formatWithPre(self, highlight, cal):
		"""
		This formats the calendar using <pre>...</pre> tags.  The
		output isn't exceptionally pretty, but it sure gets the job
		done.
		"""
		def fixl(link):
			if link:
				return "<a href=\"%s\">%s</a>" % (link[0], link[1])
			else:
				return " "

		cal2 = fixl(cal[0][0]) + cal[0][1].center(18) + fixl(cal[0][2]) + "\n" \
					+ " ".join(cal[1]) + "\n"

		def fixday(highlight, day):
			if day == 0: return "  "
			day = str(day).rjust(2)
			if highlight.has_key(day):
				return "<a href=\"%s\">%s</a>" % (highlight[day][0], highlight[day][1])
			return day

		for mem in cal[2:]:
			mem = [fixday(highlight, m) for m in mem]
			cal2 += " ".join(mem) + "\n"

		return "<pre>%s</pre>" % cal2


def load(py, entryList):
	py["calendar"] = PyblCalendar(py)
