# vim: tabstop=4 shiftwidth=4
"""
Quickly walks your blog entries and figures out the hierarchy of directories
and generates a list of categories much like the archives which you
can retrieve with $categorylinks.
"""
__author__ = "Will Guaraldi - willg@bluesock.org"
__version__ = "$Id$"

from libs import tools

class PyblCategories:
	def __init__(self, py):
		self._py = py
		self._categories = None

	def __str__(self):
		if self._categories == None:
			self.genCategories()
		return self._categories

	def genCategories(self):
		root = self._py["datadir"]
		baseurl = self._py.get("base_url", "")
		clist = tools.Walk(root, pattern=None, return_folders=1)
		clist = [mem[len(root)+1:] for mem in clist]
		clist = ["<a href=\"%s/%s\">%s</a>" % (baseurl, mem, mem) for mem in clist]
		clist.sort()
		self._categories = "<br>".join(clist)

def load(py, entryList):
	py["categorylinks"] = PyblCategories(py)
