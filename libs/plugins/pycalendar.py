# vim: tabstop=4 shiftwidth=4
"""
Generates a calendar like this one:

    January 2003
Mo Tu We Th Fr Sa Su
       1  2  3  4  5
 6  7  8  9 10 11 12
13 14 15 16 17 18 19
20 21 22 23 24 25 26
27 28 29 30 31

Then it makes little urls over the dates that have entries for this
month.

todo:
 - need to change it from <pre>...</pre> to table markup with css
"""
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
		if archiveList:
			for mem in archiveList:
				timetuple = time.localtime(os.stat(mem)[8])
				if timetuple[0] != today[0] or timetuple[1] != today[1]:
					continue

				day = str(timetuple[2]).rjust(2)
				
				if highlight.has_key(day):
					continue

				datepiece  = time.strftime("%Y/%b/%d", timetuple)
				highlight[day] = "<b><a href=\"%s/%s\">%s</a></b>" % (baseurl, datepiece, day)

		calendar.setfirstweekday(calendar.SUNDAY)
		cal = calendar.monthcalendar(today[0], today[1])
		
		def fixday(highlight, day):
			if day == 0: return "  "
			if day < 10:
				day = " " + str(day)
			else:
				day = str(day)

			return highlight.get(day, day)

		for i in range(len(cal)):
			cal[i] = " ".join([fixday(highlight, mem) for mem in cal[i]])

		# insert the days of the week
		cal.insert(0, "Su Mo Tu We Th Fr Sa")

		# insert the month name
		cal.insert(0, time.strftime("%B %Y", today).center(20))

		# join the whole thing together
		cal = "<pre>" + "\n".join(cal) + "</pre>"
		self._cal = cal

def load(py, list):
	py["calendar"] = PyblCalendar(py)
