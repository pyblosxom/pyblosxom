# Interface for PreFormatters
# This one prints <br /> tags for every line
import re
from libs.preformatters.base import PreFormatterBase
class PreFormatter(PreFormatterBase):
    def parse(self):
        result = ''
        for line in self.text:
            result += re.sub('\n','<br />',line)
        return result
