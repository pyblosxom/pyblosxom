from MoinMoin.parser.wiki import Parser
from MoinMoin.formatter.text_html import Formatter
from MoinMoin.request import Request
from MoinMoin.Page import Page
from MoinMoin.user import User
from cStringIO import StringIO
import sys
from libs.preformatters.base import PreFormatterBase

class PreFormatter(PreFormatterBase):
	def __init__(self, text = ''):
		self.text = ''.join(text)

	def parse(self):
		s = StringIO()
		oldstdout = sys.stdout
		form = None
		page = Page(None)
		page.hilite_re = None
		request = Request()
		request.user = User()
		formatter = Formatter(request)
		formatter.setPage(page)
		sys.stdout = s
		Parser(self.text, request).format(formatter, form)
		sys.stdout = oldstdout
		result = s.getvalue()
		s.close()
		return result

if __name__ == '__main__':
	text = """Hello, and welcome to MoinMoin, Refer to HelpOnFormatting for Formatting guidelines"""
	wiki = WikiText(text)
	print wiki.Wikify()
