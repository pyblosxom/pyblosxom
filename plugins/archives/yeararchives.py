"""
Summary
=======

Walks through your blog root figuring out all the available years for
the archives list.  It stores the years with links to year summaries
in the variable ``$archivelinks``.  You should put this variable in either
your head or foot template.


Usage
=====

When the user clicks on one of the year links (i.e. http://base_url/2004/), 
then yeararchives will display a summary page for that year.  The summary is 
generated using the ``yearsummarystory.html`` template for each month in the
year.  Mine is::

   <div class="blosxomEntry">
   <span class="blosxomTitle">$title</span>
   <div class="blosxomBody">
   <table>
   $body
   </table>
   </div>
   </div>


I don't have anything configurable in ``config.py``--so you'll have to 
edit the html stuff directly in the plugin.  If you dislike this, please 
take some time to fix it and send me a diff and I'll make the adjustments.


----

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright 2004-2010 Will Guaraldi

Revisions:
2010-01-07 - updated to yeararchives, updated for PyBlosxom 1.5.
2008-01-01 - fixed a problem between wbgarchives and comments and also
             fixed the ordering of months displayed.
2007-07-07 - converted documentation to reST.
2005-11-11 - Pulled into new VCS.
1.4 - (26 October, 2005) pulled into new VCS
1.3 - (14 March, 2005) added categories
1.2 - (09 December, 2004) fixed date_head issue
1.1 - (22 August, 2004) fixed a bug involving four-letter category names
                        (thanks Ludvig)
1.0 - (15 August, 2004) initial writing
"""
__author__ = "Will Guaraldi - willg at bluesock dot org"
__version__ = "$Date: 2009-06-13 03:18:19 +0000 (Sat, 13 Jun 2009) $"
__url__ = "http://pyblosxom.sourceforge.net/"
__description__ = "Year-based archives handler."

from Pyblosxom import tools, entries
import time, os

def verify_installation(request):
    return 1

class YearArchives:
    def __init__(self, request):
        self._request = request
        self._archives = None
        self._items = None

    def __str__(self):
        if self._archives == None:
            self.gen_linear_archive()
        return self._archives

    def gen_linear_archive(self):
        config = self._request.get_configuration()
        data = self._request.get_data()
        root = config["datadir"]
        baseurl = config.get("base_url", "")

        archives = {}
        archiveList = tools.walk(self._request, root)
        items = []

        for mem in archiveList:
            timetuple = tools.filestat(self._request, mem)

            y = time.strftime("%Y", timetuple)
            m = time.strftime("%m", timetuple)
            d = time.strftime("%d", timetuple)
            l = "<a href=\"%s/%s/\">%s</a><br>" % (baseurl, y, y)

            if not archives.has_key(y):
                archives[y] = l
            items.append(["%s-%s" % (y, m), "%s-%s-%s" % (y, m, d),
                          time.mktime(timetuple), mem])

        arc_keys = archives.keys()
        arc_keys.sort()
        arc_keys.reverse()

        result = []
        for key in arc_keys:
            result.append(archives[key])
        self._archives = '\n'.join(result)
        self._items = items

def new_entry(request, yearmonth, body):
    """
    Takes a bunch of variables and generates an entry out of it.  It
    creates a timestamp so that conditionalhttp can handle it without
    getting all fussy.
    """
    entry = entries.base.EntryBase(request)

    entry['title'] = yearmonth
    entry['filename'] = yearmonth + "/summary"
    entry['file_path'] = yearmonth
    entry._id = yearmonth + "::summary"

    entry["template_name"] = "yearsummarystory"
    entry["nocomments"] = "yes"

    entry["absolute_path"] = ""
    entry["fn"] = ""

    entry.set_time(time.strptime(yearmonth, "%Y-%m"))
    entry.set_data(body)

    return entry

INIT_KEY = "yeararchives_initiated"

def cb_prepare(args):
    request = args["request"]
    data = request.get_data()
    data["archivelinks"] = YearArchives(request)

def cb_date_head(args):
    request = args["request"]
    data = request.get_data()

    if data.has_key(INIT_KEY):
        args["template"] = ""
    return args

def cb_filelist(args):
    request = args["request"]
    pyhttp = request.get_http()
    data = request.get_data()
    config = request.get_configuration()
    baseurl = config.get("base_url", "")

    year = pyhttp["PATH_INFO"]

    if not year:
        return

    if year.startswith("/"):
        year = year[1:]
    if year.endswith("/"):
        year = year[:-1]
    if not year.isdigit() or not len(year) == 4:
        return

    data[INIT_KEY] = 1

    # get all the entries
    wa = YearArchives(request)
    wa.gen_linear_archive()
    items = wa._items

    # peel off the items for this year
    items = [m for m in items if m[0].startswith(year)]

    items.sort()
    items.reverse()
    
    l = ("(%(path)s) <a href=\"" + baseurl +
         "/%(file_path)s.html\">%(title)s</a><br>")
    e = "<tr>\n<td valign=\"top\" align=\"left\">%s</td>\n<td>%s</td></tr>\n"
    d = ""
    m = ""

    day = []
    month = []
    entrylist = []

    for mem in items:
        if not m:
            m = mem[0]
        if not d:
            d = mem[1]

        if m != mem[0]:
            month.append(e % (d, "\n".join(day)))
            entrylist.append(new_entry(request, m, "\n".join(month)))
            m = mem[0]
            d = mem[1]
            day = []
            month = []

        elif d != mem[1]:
            month.append(e % (d, "\n".join(day)))
            d = mem[1]
            day = []
        entry = entries.fileentry.FileEntry(
            request, mem[3], data['root_datadir'])
        day.append(l % entry)

    if day:
        month.append(e % (d, "\n".join(day)))
    if month:
        entrylist.append(new_entry(request, m, "\n".join(month)))

    return entrylist
