# vim: tabstop=4 shiftwidth=4
from libs import tools
import time, os

class PyblArchives:
	def __init__(self, py):
		self._py = py
		self._archives = None

	def __str__(self):
		if self._archives == None:
			self.genLinearArchive()
		return self._archives

	def genLinearArchive(self):
		root = self._py["datadir"]
		baseurl = self._py.get("base_url", "")
		archives = {}
		archiveList = tools.Walk(root)
		for file in archiveList:
			mtime = os.stat(file)[8]
			timetuple = time.localtime(mtime)
			mo = time.strftime('%b',timetuple)
			mo_num = time.strftime('%m',timetuple)
			da = time.strftime('%d',timetuple)
			yr = time.strftime('%Y',timetuple)
			if not archives.has_key(yr + mo_num):
				archives[yr + mo_num] = ('<a href="%s/%s/%s">%s-%s</a><br />' % 
										(baseurl, yr, mo, yr, mo))
		arcKeys = archives.keys()
		arcKeys.sort()
		arcKeys.reverse()
		result = []
		for key in arcKeys:
			result.append(archives[key])
		self._archives = '\n'.join(result)

def load(py, entryList):
	py["archivelinks"] = PyblArchives(py)

if __name__ == '__main__':
	# print genLinearArchive('../../../blosxom', 'http://roughingit.subtlehints.net/p')
	pass
