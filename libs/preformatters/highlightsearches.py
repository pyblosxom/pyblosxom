# Courtesy from Abe Fettig
# http://fettig.net
from libs.preformatters.base import PreFormatterBase
import os
import urlparse
import urllib
import re

highlight = "<span style='background-color: #ffcc00'>\\1</span>"

class PreFormatter(PreFormatterBase):
    def __init__(self, text = ''):
        self.text = ''.join(text)

    def parse(self):
        result = self.text
        if os.environ.has_key('HTTP_REFERER'):
            referer = os.environ['HTTP_REFERER']
            googleSearchWords = getGoogleSearch(referer)
     
            if googleSearchWords:
                # don't match in tags
                tagChars = "A-Za-z \"\'=:/\."
                pattern = "(?!<[" + tagChars + "]*)"
                pattern = pattern + "("
                for word in urllib.unquote_plus(googleSearchWords).split():
                    for letter in word:
                        pattern = pattern + "[" + letter.lower() + letter.upper() + "]"
                    pattern = pattern + "|"
                pattern = pattern[:-1] + ")"
                pattern = pattern + "(?![" + tagChars + "]*>)"
                result = re.sub(pattern, highlight, result)
        return result

def getGoogleSearch(url):
    # taken from Mark's log parser tool
    search = ''
    argstr = urlparse.urlparse(url)[4]
    if argstr:
        argv = [arg.find('=')>-1 and arg.split('=', 1) or ('','') for arg in argstr.split('&')]
        search = [value for key, value in argv if key == 'q']
        if not search:
            # google.yahoo.com uses p=... instead of q=...
            search = [value for key, value in argv if key == 'p']
        if search:
            search = search[0].lower()
    return search
