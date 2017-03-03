#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2004-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

Walks through your blog root figuring out all the categories you have
and how many entries are in each category.  It generates html with
this information and stores it in the ``$(categorylinks)`` variable
which you can use in your head or foot templates.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.pycategories`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Add ``$(categorylinks)`` to your head and/or foot templates.


Configuration
=============

You can format the output by setting ``category_begin``,
``category_item``, and ``category_end`` properties.

Categories exist in a hierarchy.  ``category_start`` starts the
category listing and is only used at the very beginning.  The
``category_begin`` property begins a new category group and the
``category_end`` property ends that category group.  The
``category_item`` property is the template for each category item.
Then after all the categories are printed, ``category_finish`` ends
the category listing.

For example, the following properties will use ``<ul>`` to open a
category, ``</ul>`` to close a category and ``<li>`` for each item::

    py["category_start"] = "<ul>"
    py["category_begin"] = "<ul>"
    py["category_item"] = (
        r'<li><a href="%(base_url)s/%(category_urlencoded)sindex">'
        r'%(category)s</a></li>')
    py["category_end"] = "</ul>"
    py["category_finish"] = "</ul>"


Another example, the following properties don't have a begin or an end
but instead use indentation for links and displays the number of
entries in that category::

    py["category_start"] = ""
    py["category_begin"] = ""
    py["category_item"] = (
        r'%(indent)s<a href="%(base_url)s/%(category_urlencoded)sindex">'
        r'%(category)s</a> (%(count)d)<br />')
    py["category_end"] = ""
    py["category_finish"] = ""

There are no variables available in the ``category_begin`` or
``category_end`` templates.

Available variables in the category_item template:

=======================  ==========================  ====================
variable                 example                     datatype
=======================  ==========================  ====================
base_url                 http://joe.com/blog/        string
fullcategory_urlencoded  'dev/pyblosxom/status/'     string
fullcategory             'dev/pyblosxom/status/'     string (urlencoded)
category                 'status/'                   string
category_urlencoded      'status/'                   string (urlencoed)
flavour                  'html'                      string
count                    70                          int
indent                   '&nbsp;&nbsp;&nbsp;&nbsp;'  string
=======================  ==========================  ====================
"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "$Id$"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Builds a list of categories."
__category__ = "category"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


from Pyblosxom import tools
from Pyblosxom.memcache import memcache_decorator
from Pyblosxom.tools import pwrap
import os


DEFAULT_START = r'<ul class="categorygroup">'
DEFAULT_BEGIN = r'<li><ul class="categorygroup">'
DEFAULT_ITEM = (
    r'<li><a href="%(base_url)s/%(fullcategory_urlencoded)sindex.%(flavour)s">'
    r'%(category)s</a> (%(count)d)</li>')
DEFAULT_END = "</ul></li>"
DEFAULT_FINISH = "</ul>"


def verify_installation(request):
    config = request.get_configuration()
    if not "category_item" in config:
        pwrap(
            "missing optional config property 'category_item' which allows "
            "you to specify how the category hierarchy is rendered.  see"
            "the documentation at the top of the pycategories plugin code "
            "file for more details.")
    return True


class PyblCategories:
    def __init__(self, request):
        self._request = request
        self._categories = None

    @memcache_decorator('pycategories', True)
    def __str__(self):
        if self._categories is None:
            self.gen_categories()
        return self._categories

    def gen_categories(self):
        config = self._request.get_configuration()
        root = config["datadir"]

        start_t = config.get("category_start", DEFAULT_START)
        begin_t = config.get("category_begin", DEFAULT_BEGIN)
        item_t = config.get("category_item", DEFAULT_ITEM)
        end_t = config.get("category_end", DEFAULT_END)
        finish_t = config.get("category_finish", DEFAULT_FINISH)

        self._baseurl = config.get("base_url", "")

        form = self._request.get_form()

        if 'flav' in form:
            flavour = form['flav'].value
        else:
            flavour = config.get('default_flavour', 'html')

        # build the list of all entries in the datadir
        elist = tools.walk(self._request, root)

        # peel off the root dir from the list of entries
        elist = [mem[len(root) + 1:] for mem in elist]

        # go through the list of entries and build a map that
        # maintains a count of how many entries are in each category
        elistmap = {}
        for mem in elist:
            mem = os.path.dirname(mem)
            elistmap[mem] = 1 + elistmap.get(mem, 0)
        self._elistmap = elistmap

        # go through the elistmap keys (which is the list of
        # categories) and for each piece in the key (i.e. the key
        # could be "dev/pyblosxom/releases" and the pieces would be
        # "dev", "pyblosxom", and "releases") we build keys for the
        # category list map (i.e. "dev", "dev/pyblosxom",
        # "dev/pyblosxom/releases")
        clistmap = {}
        for mem in list(elistmap.keys()):
            mem = mem.split(os.sep)
            for index in range(len(mem) + 1):
                p = os.sep.join(mem[0:index])
                clistmap[p] = 0

        # then we take the category list from the clistmap and sort it
        # alphabetically
        clist = list(clistmap.keys())
        clist.sort()

        output = []
        indent = 0

        output.append(start_t)
        # then we generate each item in the list
        for item in clist:
            itemlist = item.split(os.sep)

            num = 0
            for key in list(self._elistmap.keys()):
                if item == '' or key == item or key.startswith(item + os.sep):
                    num = num + self._elistmap[key]

            if not item:
                tab = ""
            else:
                tab = len(itemlist) * "&nbsp;&nbsp;"

            if itemlist != ['']:
                if indent > len(itemlist):
                    for i in range(indent - len(itemlist)):
                        output.append(end_t)

                elif indent < len(itemlist):
                    for i in range(len(itemlist) - indent):
                        output.append(begin_t)

            # now we build the dict with the values for substitution
            d = {"base_url": self._baseurl,
                 "fullcategory": item + "/",
                 "category": itemlist[-1] + "/",
                 "flavour": flavour,
                 "count": num,
                 "indent": tab}

            # this prevents a double / in the root category url
            if item == "":
                d["fullcategory"] = item

            # this adds urlencoded versions
            d["fullcategory_urlencoded"] = (
                tools.urlencode_text(d["fullcategory"]))
            d["category_urlencoded"] = tools.urlencode_text(d["category"])

            # and we toss it in the thing
            output.append(item_t % d)

            if itemlist != ['']:
                indent = len(itemlist)

        output.append(end_t * indent)
        output.append(finish_t)

        # then we join the list and that's the final string
        self._categories = "\n".join(output)


def cb_prepare(args):
    request = args["request"]
    data = request.get_data()
    data["categorylinks"] = PyblCategories(request)
