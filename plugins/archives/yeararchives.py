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


The ``$(archivelinks)`` link can be configured with the
``archive_template`` config variable.  It uses the Python string
formatting syntax.

Example::

    py['archive_template'] = '<a href="%(base_url)s/%(Y)s/index.%(f)s">%(Y)s</a><br />'

The vars available with typical example values are::

    Y      4-digit year   ex: '1978'
    y      2-digit year   ex: '78'
    f      the flavour    ex: 'html'

"""
__author__ = "Will Kahn-Greene - willg at bluesock dot org"
__version__ = "2010-05-08"
__url__ = "http://pyblosxom.sourceforge.net/"
__description__ = "Year-based archives handler."

from Pyblosxom import tools, entries
import time, os

def verify_installation(request):
    config = request.get_configuration()
    if not config.has_key("archive_template"):
        print "missing optional config property 'archive_template' which "
        print "allows you to specify how the archive links are created.  "
        print "refer to yeararchives plugin documentation for more details."
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

        fulldict = {}
        fulldict.update(config)
        fulldict.update(data)

        flavour = data.get(
            "flavour", config.get("default_flavour", "html"))

        template = config.get(
            'archive_template',
            '<a href="%(base_url)s/%(Y)s/index.%(f)s">%(Y)s</a><br />')

        for mem in archive_list:
            timetuple = tools.filestat(self._request, mem)

            timedict = {}
            for x in ["m", "Y", "y", "d"]:
                timedict[x] = time.strftime("%" + x, timetuple)

            fulldict.update(timedict)
            fulldict["f"] = flavour
            year = fulldict["Y"]

            if not archives.has_key(year):
                archives[year] = template % fulldict
            items.append(
                ["%(Y)s-%(m)s" % fulldict,
                 "%(Y)s-%(m)s-%(d)s" % fulldict,
                 time.mktime(timetuple),
                 mem])

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

def parse_path_info(path):
    """Returns None or (year, flav) tuple.

    Handles urls of this type:

    - /2003
    - /2003/
    - /2003/index
    - /2003/index.flav
    """
    path = path.split("/")
    path = [m for m in path if m]
    if not path:
        return

    year = path[0]
    if not year.isdigit() or not len(year) == 4:
        return

    if len(path) == 1:
        return (year, None)

    if len(path) == 2 and path[1].startswith("index"):
        flav = None
        if "." in path[1]:
            flav = path[1].split(".", 1)[1]
        return (year, flav)

    return

def cb_filelist(args):
    request = args["request"]
    pyhttp = request.get_http()
    data = request.get_data()
    config = request.get_configuration()
    baseurl = config.get("base_url", "")

    path = pyhttp["PATH_INFO"]

    ret = parse_path_info(path)
    if ret == None:
        return

    # note: returned flavour is None if there is no .flav appendix
    year, flavour = ret

    data[INIT_KEY] = 1

    # get all the entries
    wa = YearArchives(request)
    wa.gen_linear_archive()
    items = wa._items

    # peel off the items for this year
    items = [m for m in items if m[0].startswith(year)]

    items.sort()
    items.reverse()

    # Set and use current (or default) flavour for permalinks
    if not flavour:
        flavour = data.get(
            "flavour", config.get("default_flavour", "html"))

    data["flavour"] = flavour

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
