# vim: tabstop=4 shiftwidth=4
"""
Walks through your blog root figuring out all the categories you have
and how many entries are in each category.  It generates html with
this information and stores it in the $categorylinks variable which
you can use in your head or foot templates.

You can format the output by setting the "category_begin", "category_item", and
"category_end" properties.

Categories exist in a hierarchy.  The "category_begin" property begins a 
category group and the "category_end" property ends a category group.  The
"category_item" property is the template for each category item.

For example, the following properties will use <ul> to open a category, </ul>
to close a category and <li> for each item:

py["category_begin"] = "<ul>"
py["category_item"] = r'<li><a href="%(base_url)s/%(category)sindex">%(category)s</a></li>'
py["category_end"] = "</ul>"


Another example, the following properties don't have a begin or an end but
instead use indentation for links and displays the number of entries in that
category:

py["category_begin"] = ""
py["category_item"] = r'%(indent)s<a href="%(base_url)s/%(category)sindex">%(category)s</a> (%(count)d)<br />'
py["category_end"] = ""

There are no variables available in the category_begin or category_end templates.

Available variables in the category_item template:

  base_url      (this is set in your config.py file)   string
  fullcategory  'dev/pyblosxom/status/'                string
  category      'status/'                              string
  flavour       'html'                                 string
  count         70                                     int
  indent        '&nbsp;&nbsp;&nbsp;&nbsp;'             string
"""
__author__ = "Will Guaraldi - willg at bluesock dot org"
__version__ = "$Id$"

from Pyblosxom import tools
import re, os

DEFAULT_BEGIN = r'<ul class="categorygroup">'
DEFAULT_ITEM = r'<li><a href="%(base_url)s/%(fullcategory)sindex.%(flavour)s">%(category)s</a> (%(count)d)</li>'
DEFAULT_END = "</ul>"

def verify_installation(request):
    config = request.getConfiguration()
    if not config.has_key("category_template"):
        print "missing optional config property 'category_template' which allows "
        print "you to specify how the category hierarchy is rendered.  see"
        print "the documentation at the top of the pycategories plugin code "
        print "file for more details."
    return 1

class PyblCategories:
    def __init__(self, request):
        self._request = request
        self._categories = None
        self.genCategories()

    def __str__(self):
        if self._categories == None:
            self.genCategories()
        return self._categories

    def genCategories(self):
        config = self._request.getConfiguration()
        root = config["datadir"]

        begin_t = config.get("category_begin", DEFAULT_BEGIN)
        item_t = config.get("category_item", DEFAULT_ITEM)
        end_t = config.get("category_end", DEFAULT_END)

        self._baseurl = config.get("base_url", "")

        form = self._request.getForm()
        flavour = (form.has_key('flav') and form['flav'].value or 
            config.get('default_flavour', 'html'))

        # build the list of all entries in the datadir
        elist = tools.Walk(self._request, root)

        # peel off the root dir from the list of entries
        elist = [mem[len(root)+1:] for mem in elist]

        # go through the list of entries and build a map that
        # maintains a count of how many entries are in each 
        # category
        elistmap = {}
        for mem in elist:
            mem = os.path.dirname(mem)
            elistmap[mem] = 1 + elistmap.get(mem, 0)
        self._elistmap = elistmap

        # go through the elistmap keys (which is the list of
        # categories) and for each piece in the key (i.e. the key
        # could be "dev/pyblosxom/releases" and the pieces would
        # be "dev", "pyblosxom", and "releases") we build keys
        # for the category list map (i.e. "dev", "dev/pyblosxom",
        # "dev/pyblosxom/releases")
        clistmap = {}
        for mem in elistmap.keys():
            mem = mem.split(os.sep)
            for index in range(len(mem)+1):
                p = os.sep.join(mem[0:index])
                clistmap[p] = 0

        # then we take the category list from the clistmap and
        # sort it alphabetically
        clist = clistmap.keys()
        clist.sort()

        output = []
        indent = 0

        # then we generate each item in the list
        for item in clist:
            itemlist = item.split(os.sep)

            num = 0
            for key in self._elistmap.keys():
                if key.endswith(item) or key.endswith(item + os.sep):
                    num = num + self._elistmap[key]

            if not item:
                tab = ""
            else:
                tab = len(itemlist) * "&nbsp;&nbsp;"

            if indent > len(itemlist):
                for i in range(indent - len(itemlist)):
                    output.append(end_t)

            elif indent < len(itemlist):
                for i in range(len(itemlist) - indent):
                    output.append(begin_t)

            # now we build the dict with the values for substitution
            d = { "base_url":     self._baseurl, 
                  "fullcategory": item + "/", 
                  "category":     itemlist[-1] + "/", 
                  "flavour":      flavour,
                  "count":        num,
                  "indent":       tab }

            # and we toss it in the thing
            output.append(item_t % d)

            indent = len(itemlist)

        output.append(end_t)

        # then we join the list and that's the final string
        self._categories = "\n".join(output)

def cb_prepare(args):
    request = args["request"]
    data = request.getData()
    data["categorylinks"] = PyblCategories(request)
