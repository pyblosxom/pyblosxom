# vim: tabstop=4 shiftwidth=4
import os
import cPickle as pickle
from libs import tools
from xml.marshal import wddx as marshal

class FeedBack:
	def __init__(self, blog, dataFile):
		self.blog = blog
		self.dataFile = dataFile
		self.feedback = []
		self.commentFile = self.blog + '.feedback'
		if os.path.isfile(self.blog):
			if (os.path.isfile(self.dataFile) and 
					os.stat(self.dataFile)[8] >= os.stat(self.commentFile)[8]):
				cached = 1
				try:
					fp = file(dataFile, 'rb')
					entryData = pickle.load(fp)
					self.feedback = entryData.get('feedback',[])
					fp.close()
				except:
					cached = 0
			else:
				cached = 0

			if not cached and os.path.isfile(self.commentFile):
				try:
					self.feedback = marshal.loads(file(self.commentFile).read())
				except:
					pass
	
	def saveFeedback(self, type, data):
		self.feedback.append({'type':type, 'data':data})
		self.saveFeedbackToFile()
	
	def saveFeedbackToFile(self):
		file(self.commentFile, 'w').write(marshal.dumps(self.feedback))

	def show(self, commentTemplate = '', trackbackTemplate = '', pingbackTemplate = ''):
		_show_pingback(pingbackTemplate)
		_show_trackback(trackbackTemplate)
		_show_comments(commentTemplate)
		
	def _show_pingback(self, template):
		for ping in self.feedback.get('pings', []):
			tools.parse(ping, template)
			
	def _show_pingback(self, template):
		for ping in self.feedback.get('tracks', []):
			tools.parse(ping, template)

	def _show_pingback(self, template):
		for ping in self.feedback.get('comments', []):
			tools.parse(ping, template)
	
