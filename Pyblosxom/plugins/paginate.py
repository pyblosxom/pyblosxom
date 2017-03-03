#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2004-2012 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

Plugin for paging long index pages.

Pyblosxom uses the ``num_entries`` configuration variable to prevent
more than ``num_entries`` being rendered by cutting the list down to
``num_entries`` entries.  So if your ``num_entries`` is set to 20, you
will only see the first 20 entries rendered.

The paginate plugin overrides this functionality and allows for
paging.

This plugin also needs the ``base_url`` variable to be set for static
rendering and fi using first_last to add links to the first and last page.

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

Optional:
3. Customize the links with the CSS class "paginate".


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

``paginate_first_last``

   Defaults to 0

   Set this to 1 to add links to the first and last page.


``paginate_first_text``

   Defaults to "&lt;&lt;&gt;".

   This is the text for the "first page" link.


``paginate_last_text``

   Defaults to "&gt;&gt;&gt;".

   This is the text for the "last page" link.


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

This plugin works fine with static rendering, but the urls look
different. Instead of adding a ``page=4`` kind of thing to the
querystring, this adds it to the url.

For example, say your front page was ``/index.html`` and you had 5
pages of entries. Then the urls would look like this::

    /index.html           first page
    /index_page2.html     second page
    /index_page3.html     third page
    ...

The links will break with static rendering if you blog is located at a url
that contains "_page".

"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2015-06-29"
__url__ = "http://pyblosxom.github.com/"
__description__ = (
    "Allows navigation by page for indexes that have too many entries.")
__category__ = "display"
__license__ = "MIT"
__registrytags__ = "1.5, core"


import os

from Pyblosxom.tools import pwrap_error, render_url_statically


def verify_installation(request):
    config = request.get_configuration()
    if config.get("num_entries", 0) == 0:
        pwrap_error(
            "Missing config property 'num_entries'.  paginate won't do "
            "anything without num_entries set.  Either set num_entries "
            "to a positive integer, or disable the paginate plugin."
            "See the documentation at the top of the paginate plugin "
            "code file for more details.")
        return False
    return True


class PageDisplay:
    def __init__(self, url_template, url_first_page, current_page, max_pages, count_from,
                 previous_text, next_text, linkstyle, first_last, first_text, last_text, request):
        self._url_template = url_template
        self._url_first_page = url_first_page
        self._current_page = current_page
        self._max_pages = max_pages
        self._count_from = count_from
        self._previous = previous_text
        self._next = next_text
        self._linkstyle = linkstyle
        self._first_last = first_last
        self._first = first_text
        self._last = last_text
        self._config = request.get_configuration()
        self._data = request.get_data()

    def __str__(self):
        output = []

        #first
        if (self._current_page != self._count_from
            and self._first_last == 1
            and self._data.get("STATIC")):
            first_url = self._url_first_page
            output.append('<a class="paginate" href="%s">%s</a>&nbsp;' %
                          (first_url, self._first))

        elif (self._current_page != self._count_from
              and self._first_last == 1):
            first_url = self._url_template % (self._count_from)
            output.append('<a class="paginate" href="%s">%s</a>&nbsp;' %
                          (first_url, self._first))
        
        # prev
        if (self._current_page == self._count_from + 1
            and self._data.get("STATIC")):
            prev_url = self._url_first_page
            output.append('<a class="paginate" href="%s">%s</a>&nbsp;' %
                          (prev_url, self._previous))

        elif self._current_page != self._count_from:
            prev_url = self._url_template % (self._current_page - 1)
            output.append('<a class="paginate" href="%s">%s</a>&nbsp;' %
                          (prev_url, self._previous))
            
        # pages
        if self._linkstyle == 0:
            for i in range(self._count_from, self._max_pages):
                if i == self._current_page:
                    output.append('[%d]' % i)
                elif (i == 1
                     and self._data.get("STATIC")):
                     page_url = self._url_first_page
                     output.append('<a class="paginate" href="%s">%d</a>' % (page_url, i))
                else:
                    page_url = self._url_template % i
                    output.append('<a class="paginate" href="%s">%d</a>' % (page_url, i))
        elif self._linkstyle == 1:
            output.append(' Page %s of %s ' %
                          (self._current_page, self._max_pages - 1))

        # next
        if self._current_page < self._max_pages - 1:
            next_url = self._url_template % (self._current_page + 1)
            output.append('&nbsp;<a class="paginate" href="%s">%s</a>' %
                          (next_url, self._next))

        
        #last
        if (self._current_page != self._max_pages -1
            and self._first_last == 1
            and self._data.get("STATIC")):
            last_url = self._url_template % (self._max_pages -1)
            output.append('<a class="paginate" href="%s">%s</a>&nbsp;' %
                          (last_url, self._last))

        elif (self._current_page != self._max_pages -1
              and self._first_last == 1):
            last_url = self._url_template (self._max_pages -1)
            output.append('<a class="paginate" href="%s">%s</a>&nbsp;' %
                          (last_url, self._last))

            
        return " ".join(output)


def page(request, num_entries, entry_list):
    http = request.get_http()
    config = request.get_configuration()
    data = request.get_data()

    first_text = config.get("paginate_first_text", "&lt;&lt;&lt;")
    previous_text = config.get("paginate_previous_text", "&lt;&lt;")
    next_text = config.get("paginate_next_text", "&gt;&gt;")
    last_text = config.get("paginate_last_text", "&gt;&gt;&gt;")

    first_last = config.get("paginate_first_last", 0)
    if first_last > 1:
        first_last = 1

    link_style = config.get("paginate_linkstyle", 1)
    if link_style > 1:
        link_style = 1

    entries_per_page = num_entries
    count_from = config.get("paginate_count_from", 0)

    if isinstance(entry_list, list) and 0 < entries_per_page < len(entry_list):

        page = count_from
        url = http.get("REQUEST_URI", http.get("HTTP_REQUEST_URI", ""))
        url_template = url
        if not data.get("STATIC"):
            form = request.get_form()

            if form:
                try:
                    page = int(form.getvalue("page"))
                except (TypeError, ValueError):
                    page = count_from

            # Restructure the querystring so that page= is at the end
            # where we can fill in the next/previous pages.
            if url_template.find("?") != -1:
                query = url_template[url_template.find("?") + 1:]
                url_template = url_template[:url_template.find("?")]

                query = query.split("&")
                query = [m for m in query if not m.startswith("page=")]
                if len(query) == 0:
                    url_template = url_template + "?" + "page=%d"
                else:
                    # Note: We're using &amp; here because it needs to
                    # be url_templateencoded.
                    url_template = (url_template + "?" + "&amp;".join(query) +
                                    "&amp;page=%d")
            else:
                url_template += "?page=%d"

        else:
            try:
                page = data["paginate_page"]
            except KeyError:
                page = count_from

            # The REQUEST_URI isn't the full url here--it's only the
            # path and so we need to add the base_url.
            base_url = config["base_url"].rstrip("/")
            url_template = base_url + url_template

            url_template = url_template.split("/")
            ret = url_template[-1].rsplit("_", 1)
            if len(ret) == 1:
                fn, ext = os.path.splitext(ret[0])
                pageno = "_page%d"
            else:
                fn, pageno = ret
                pageno, ext = os.path.splitext(pageno)
                pageno = "_page%d"
            url_template[-1] = fn + pageno + ext
            url_template = "/".join(url_template)
            url_first_page = url_template.split("_page")
            url_first_page = url_first_page[0] + ext

        begin = (page - count_from) * entries_per_page
        end = (page + 1 - count_from) * entries_per_page
        if end > len(entry_list):
            end = len(entry_list)

        max_pages = ((len(entry_list) - 1) / entries_per_page) + 1 + count_from

        data["entry_list"] = entry_list[begin:end]

        data["page_navigation"] = PageDisplay(
            url_template, url_first_page, page, max_pages, count_from, previous_text,
            next_text, link_style, first_last, first_text, last_text, request)

        # If we're static rendering and there wasn't a page specified
        # and this is one of the flavours to statically render, then
        # this is the first page and we need to render all the rest of
        # the pages, so we do that here.
        static_flavours = config.get("static_flavours", ["html"])
        if ((data.get("STATIC") and page == count_from
             and data.get("flavour") in static_flavours)):
            # Turn http://example.com/index.html into
            # http://example.com/index_page5.html for each page.
            url = url.split('/')
            fn = url[-1]
            fn, ext = os.path.splitext(fn)
            template = '/'.join(url[:-1]) + '/' + fn + '_page%d'
            if ext:
                template = template + ext

            for i in range(count_from + 1, max_pages):
                print("   rendering page %s ..." % (template % i))
                render_url_statically(dict(config), template % i, '')


def cb_truncatelist(args):
    request = args["request"]
    entry_list = args["entry_list"]

    page(request, request.config.get("num_entries", 10), entry_list)
    return request.data.get("entry_list", entry_list)


def cb_pathinfo(args):
    request = args["request"]
    data = request.get_data()

    # This only kicks in during static rendering.
    if not data.get("STATIC"):
        return

    http = request.get_http()
    pathinfo = http.get("PATH_INFO", "").split("/")

    # Handle the http://example.com/index_page5.html case. If we see
    # that, put the page information in the data dict under
    # "paginate_page" and "fix" the pathinfo.
    if pathinfo and "_page" in pathinfo[-1]:
        fn, pageno = pathinfo[-1].rsplit("_")
        pageno, ext = os.path.splitext(pageno)
        try:
            pageno = int(pageno[4:])
        except (ValueError, TypeError):
            # If it's not a valid page number, then we shouldn't be
            # doing anything here.
            return

        pathinfo[-1] = fn
        pathinfo = "/".join(pathinfo)
        if ext:
            pathinfo += ext

        http["PATH_INFO"] = pathinfo
        data["paginate_page"] = pageno
