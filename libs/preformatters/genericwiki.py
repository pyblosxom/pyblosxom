# Generic wiki markup PreFormatter 2002-11-18, for pyblosxom
# CHANGE wikibaseurl to point to your wiki, & wikinamepattern to yours
# Bug reports, comments, presents, etc. to John Abbe at johnca@ourpla.net
# ToDo: Lists; code/<pre>; InterWiki links; other wikinamepatterns
import re
from libs.preformatters.base import PreFormatterBase

class PreFormatter(PreFormatterBase):
    def __init__(self, text = ''):
        self.text = text

    def parse(self):
        # url of your wiki up to page name
        wikibaseurl = "http://ourpla.net/cgi/pikie?"
        # WikiName pattern used in your wiki
        wikinamepattern = r'\b(([A-Z]+[a-z]+){2,})\b' # original
        mailurlpattern = r'mailto\:[\"\-\_\.\w]+\@[\-\_\.\w]+\w'
        newsurlpattern = r'news\:(?:\w+\.){1,}\w+'
        fileurlpattern = r'(?:http|https|file|ftp)\:' +
                '[\/\-\_\.\w]+[\/\w][\?\&\+\=\%\w\/\-\_\.]*'
        result = ''
        for line in self.text:
            result += line

        # Turn '[xxx:address label]' into labeled link
        result = re.sub(r'\[(' +
                 fileurlpattern + '|' +
                 mailurlpattern + '|' +
                 newsurlpattern + ')\ (.+?)\]',
                 r'<a href="\1">\2</a>', result)

        # Convert naked URLs into links -- skip ones with a " before
        result = re.sub(r'(?<!")(' +
                 fileurlpattern + '|' +
                 mailurlpattern + '|' +
                 newsurlpattern + ')',
                 r'<a href="\1">\1</a>', result)

        # Convert WikiNames into links
        result = re.sub(r'(?<![\?\/\=])' +
                 wikinamepattern, '<a href="' +
                 wikibaseurl + r'\1">\1</a>', result)

        # '' for emphasis, ''' for strong, ---- for a horizontal rule
        result = re.sub(r"'''(.*?)'''", r"<strong>\1</strong>", result)
        result = re.sub(r"''(.*?)''", r"<em>\1</em>", result)
        result = re.sub(r"\n(-{4,})\n", "<hr>", result)

        # Convert two or more newlines into <p>
        result = re.sub(r'\n{2,}', r'</p>\n<p>', result)

        return "<p>" + result + "</p>"
