#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008, 2009, 2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

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
"""
__author__ = "Will Kahn-Greene - willg at bluesock dot org"
__version__ = "2010-05-08"
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
        archive_list = tools.walk(self._request, root)
        items = []

        for mem in archive_list:
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

    # Use current (or default) flavour for permalinks
    # note: for date URLs, data["flavor"] is not set in the pyblosxom handler
    # if it is passed as an extension.
    # If we find a valid date URL, we will therefore set data["flavour"] accordingly
    # a few lines down.
    try:
        flavour = data["flavour"]
    except KeyError:
        flavour = config.get("default_flavour", "html")


    # if a flavor is appended drop it for the date calculation
    # and save it, so we can set the rendering flavour.
    if os.path.basename(year).find('.') != -1:
        year, flavour = year.rsplit('.',1)
    if year.startswith("/"):
        year = year[1:]
    if year.endswith("/"):
        year = year[:-1]
    if not year.isdigit() or not len(year) == 4:
        return

    data["flavour"] = flavour
    
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
         "/%(file_path)s." + flavour + "\">%(title)s</a><br>")
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
            request, mem[3], config['datadir'])
        day.append(l % entry)

    if day:
        month.append(e % (d, "\n".join(day)))
    if month:
        entrylist.append(new_entry(request, m, "\n".join(month)))

    return entrylist
