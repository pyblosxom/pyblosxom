"""Interface for preformatters
"""
# Basic Interface for PreFormatters
# This one does nothing except to join strings
class PreFormatterBase:
    def __init__(self, text = ''):
        """Text is a list of strings"""
        self.text = text

    def parse(self):
        """Override this method to modify the text, return a string"""
        return ''.join(self.text)

class PreFormatter(PreFormatterBase):
    pass
