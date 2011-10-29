#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2004-2011 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

Plugin for paging long index pages.

PyBlosxom uses the num_entries configuration variable to prevent more
than ``num_entries`` being rendered by cutting the list down to
``num_entries`` entries.  So if your ``num_entries`` is set to 20, you
will only see the first 20 entries rendered.

The paginate overrides this functionality and allows for paging.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.paginate`` to your ``load_plugins`` list
   variable in your ``config.py`` file.

   Make sure it's the first plugin in the ``load_plugins`` list so
   that it has a chance to operate on the entry list before other
   plugins.

2. add the ``$(page_navigation)`` variable to your head or foot (or
   both) templates.  this is where the page navigation HTML will
   appear.


Here are some additional configuration variables to adjust the
behavior::

``paginate_count_from``

   Defaults to 0.

   This is the number to start counting from.  Some folks like their
   pages to start at 0 and others like it to start at 1.  This enables
   you to set it as you like.

   Example::

      py["paginate_count_from"] = 1


``paginate_previous_text``

   Defaults to "&lt;&lt;".

   This is the text for the "previous page" link.


``paginate_next_text``

   Defaults to "&gt;&gt;".

   This is the text for the "next page" link.


``paginate_linkstyle``

   Defaults to 1.

   This allows you to change the link style of the paging.

   Style 0::

       [1] 2 3 4 5 6 7 8 9 ... >>

   Style 1::

      Page 1 of 4 >>

   If you want a style different than that, you'll have to copy the
   plugin and implement your own style.


Note about static rendering
===========================

This plugin doesn't work with static rendering.  The problem is that
it relies on the querystring to figure out which page to show and when
you're static rendering, only the first page is rendered.  At some
point, someone will fix this.

"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2011-10-22"
__url__ = "http://pyblosxom.bluesock.org/"
__description__ = (
    "Allows navigation by page for indexes that have too many entries.")
__category__ = "display"
__license__ = "MIT"
__registrytags__ = "1.5, core"


def verify_installation(request):
    config = request.get_configuration()
    if config.get("num_entries", 0) == 0:
        print "Missing config property 'num_entries'.  paginate won't do "
        print "anything without num_entries set.  Either set num_entries "
        print "to a positive integer, or disable the paginate plugin."
        print "See the documentation at the top of the paginate plugin "
        print "code file for more details."
        return 0
    return 1


class PageDisplay:
    def __init__(self, url, current_page, max_pages, count_from,
                 previous_text, next_text, linkstyle):
        self._url = url
        self._current_page = current_page
        self._max_pages = max_pages
        self._count_from = count_from
        self._previous = previous_text
        self._next = next_text
        self._linkstyle = linkstyle

    def __str__(self):
        output = []
        # prev
        if self._current_page != self._count_from:
            output.append('<a href="%s%d">%s</a>&nbsp;' %
                          (self._url, self._current_page - 1, self._previous))

        # pages
        if self._linkstyle == 0:
            for i in range(self._count_from, self._max_pages):
                if i == self._current_page:
                    output.append('[%d]' % i)
                else:
                    output.append('<a href="%s%d">%d</a>' %
                                  (self._url, i, i))
        elif self._linkstyle == 1:
            output.append(' Page %s of %s ' %
                          (self._current_page, self._max_pages - 1))

        # next
        if self._current_page < self._max_pages - 1:
            output.append('&nbsp;<a href="%s%d">%s</a>' %
                          (self._url, self._current_page + 1, self._next))

        return " ".join(output)


def page(request, num_entries, entry_list):
    http = request.get_http()
    config = request.get_configuration()
    data = request.get_data()

    previous_text = config.get("paginate_previous_text", "&lt;&lt;")
    next_text = config.get("paginate_next_text", "&gt;&gt;")

    linkstyle = config.get("paginate_linkstyle", 1)
    if linkstyle > 1:
        linkstyle = 1

    max = num_entries
    count_from = config.get("paginate_count_from", 0)

    if max > 0 and isinstance(entry_list, list) and len(entry_list) > max:
        form = request.get_form()

        page = count_from
        if form:
            try:
                page = int(form.getvalue("page"))
            except:
                page = count_from

        begin = (page - count_from) * max
        end = (page + 1 - count_from) * max
        if end > len(entry_list):
            end = len(entry_list)

        maxpages = ((len(entry_list) - 1) / max) + 1 + count_from

        url = http.get("REQUEST_URI", http.get("HTTP_REQUEST_URI", ""))
        if url.find("?") != -1:
            query = url[url.find("?") + 1:]
            url = url[:url.find("?")]

            query = query.split("&")
            query = [m for m in query if not m.startswith("page=")]
            if len(query) == 0:
                url = url + "?" + "page="
            else:
                url = url + "?" + "&amp;".join(query) + "&amp;page="
        else:
            url = url + "?page="

        data["entry_list"] = entry_list[begin:end]

        data["page_navigation"] = PageDisplay(
            url, page, maxpages, count_from, previous_text, next_text,
            linkstyle)

    else:
        data["page_navigation"] = ""


def cb_truncatelist(args):
    request = args["request"]
    entry_list = args["entry_list"]

    page(request, request.config.get("num_entries", 10), entry_list)
    return request.data.get("entry_list", entry_list)
