"""Interface for preformatters
"""
# Plain preformatter
# This one does nothing except to join strings
from libs.preformatters.base import PreFormatterBase
class PreFormatter(PreFormatterBase):
	def __init__(self, text = ''):
		"""Text is a list of strings"""
		self.text = text

	def parse(self):
		"""Override this method to modify the text, return a string"""
		return ''.join(self.text)
