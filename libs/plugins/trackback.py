import cgi, xmlrpc

class TrackBack:
	def __init__(self,properties):
		self.data = properties
		self.form = cgi.FieldStorage()

	def process(self):
		print "Content-type: text/plain\n\nHello world";
