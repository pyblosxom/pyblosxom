from libs import tools
import time, os

def genLinearArchive(root, baseurl):
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
	return '\n'.join(result)

if __name__ == '__main__':
	print genLinearArchive('../../../blosxom', 'http://roughingit.subtlehints.net/p')
