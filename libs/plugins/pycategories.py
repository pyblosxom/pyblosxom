# vim: tabstop=4 shiftwidth=4
"""
Walks through your blog root figuring out all the categories you have
and how many entries are in each category.  It generates html with
this information and stores it in the $categorylinks variable which
you can use in your head or foot templates.

Additionally, you can specify the flavour for the link by creating an 
entry in the config.py file or the ini file with the name 
"category_flavour" and the value of the flavour you want to use.

ini-file example (in the pyblosxom section):

   category_flavour = index

config.py example:

   py["category_flavour"] = "index"
"""
__author__ = "Will Guaraldi - willg@bluesock.org"
__version__ = "$Id$"

from libs import tools
import re, os

class PyblCategories:
	def __init__(self, py):
		self._py = py
		self._categories = None

	def __str__(self):
		if self._categories == None:
			self.genCategories()
		return self._categories

	def genitem(self, item):
		itemlist = item.split("/")

		num = 0
		for key in self._elistmap:
			if key.find(item) == 0:
				num = num + self._elistmap[key]
		num = " (%d)" % num

		return (((len(itemlist)-1) * "&nbsp;&nbsp;") + 
				"<a href=\"%s/%s%s\">%s</a>%s" % (self._baseurl, item, self._flavour, itemlist[-1] +"/", num))

	def genCategories(self):
		root = self._py["datadir"]
		if self._py.get("category_flavour", "") == "":
			self._flavour = ""
		else:
			self._flavour = "?flav=" + self._py["category_flavour"]

		self._baseurl = self._py.get("base_url", "")

		# build the list of directories (categories)
		clist = tools.Walk(root, pattern=re.compile('.*'), return_folders=1)
		clist = [mem[len(root)+1:] for mem in clist]
		clist.sort()
		clist.insert(0, "")

		# build the list of entries
		elist = tools.Walk(root)
		elist = [mem[len(root)+1:] for mem in elist]

		elistmap = {}
		for mem in elist:
			mem = os.path.dirname(mem)
			elistmap[mem] = 1 + elistmap.get(mem, 0)
		self._elistmap = elistmap

		clist = map(self.genitem, clist)
		self._categories = "<br>".join(clist)

def load(py, entryList):
	py["categorylinks"] = PyblCategories(py)
