import locale
import os
import sys
import time
from Pyblosxom import tools
from Pyblosxom.entries.fileentry import FileEntry


def blosxom_handler(request):
    """This is the default blosxom handler.

    It calls the renderer callback to get a renderer.  If there is no
    renderer, it uses the blosxom renderer.

    It calls the pathinfo callback to process the path_info http
    variable.

    It calls the filelist callback to build a list of entries to
    display.

    It calls the prepare callback to do any additional preparation
    before rendering the entries.

    Then it tells the renderer to render the entries.

    :param request: the request object.
    """
    config = request.get_configuration()
    data = request.get_data()

    # go through the renderer callback to see if anyone else wants to
    # render.  this renderer gets stored in the data dict for
    # downstream processing.
    rend = tools.run_callback('renderer',
                              {'request': request},
                              donefunc=lambda x: x is not None,
                              defaultfunc=lambda x: None)

    if not rend:
        # get the renderer we want to use
        rend = config.get("renderer", "blosxom")

        # import the renderer
        rend = tools.importname("Pyblosxom.renderers", rend)

        # get the renderer object
        rend = rend.Renderer(request, config.get("stdoutput", sys.stdout))

    data['renderer'] = rend

    # generate the timezone variable
    data["timezone"] = time.tzname[time.localtime()[8]]

    # process the path info to determine what kind of blog entry(ies)
    # this is
    tools.run_callback("pathinfo",
                       {"request": request},
                       donefunc=lambda x: x is not None,
                       defaultfunc=blosxom_process_path_info)

    # call the filelist callback to generate a list of entries
    data["entry_list"] = tools.run_callback(
        "filelist",
        {"request": request},
        donefunc=lambda x: x is not None,
        defaultfunc=blosxom_file_list_handler)

    # figure out the blog-level mtime which is the mtime of the head
    # of the entry_list
    entry_list = data["entry_list"]
    if isinstance(entry_list, list) and len(entry_list) > 0:
        mtime = entry_list[0].get("mtime", time.time())
    else:
        mtime = time.time()
    mtime_tuple = time.localtime(mtime)
    mtime_gmtuple = time.gmtime(mtime)

    data["latest_date"] = time.strftime('%a, %d %b %Y', mtime_tuple)

    # Make sure we get proper 'English' dates when using standards
    loc = locale.getlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, 'C')

    data["latest_w3cdate"] = time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                           mtime_gmtuple)
    data['latest_rfc822date'] = time.strftime('%a, %d %b %Y %H:%M GMT',
                                              mtime_gmtuple)

    # set the locale back
    locale.setlocale(locale.LC_ALL, loc)

    # we pass the request with the entry_list through the prepare
    # callback giving everyone a chance to transform the data.  the
    # request is modified in place.
    tools.run_callback("prepare", {"request": request})

    # now we pass the entry_list through the renderer
    entry_list = data["entry_list"]
    renderer = data['renderer']

    if renderer and not renderer.rendered:
        if entry_list:
            renderer.set_content(entry_list)
            # Log it as success
            tools.run_callback("logrequest",
                               {'filename': config.get('logfile', ''),
                                'return_code': '200',
                                'request': request})
        else:
            renderer.add_header('Status', '404 Not Found')
            renderer.set_content(
                {'title': 'The page you are looking for is not available',
                 'body': 'Somehow I cannot find the page you want. ' +
                         'Go Back to <a href="%s">%s</a>?'
                         % (config["base_url"], config["blog_title"])})
            # Log it as failure
            tools.run_callback("logrequest",
                               {'filename': config.get('logfile', ''),
                                'return_code': '404',
                                'request': request})
        renderer.render()

    elif not renderer:
        output = config.get('stdoutput', sys.stdout)
        output.write("Content-Type: text/plain\n\n" +
                     "There is something wrong with your setup.\n" +
                     "Check your config files and verify that your " +
                     "configuration is correct.\n")

    cache = tools.get_cache(request)
    if cache:
        cache.close()


def blosxom_entry_parser(filename, request):
    """Open up a ``.txt`` file and read its contents.  The first line
    becomes the title of the entry.  The other lines are the body of
    the entry.

    :param filename: a filename to extract data and metadata from
    :param request: a standard request object

    :returns: dict containing parsed data and meta data with the
              particular file (and plugin)
    """
    config = request.get_configuration()

    entry_data = {}

    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    # the file has nothing in it...  so we're going to return a blank
    # entry data object.
    if len(lines) == 0:
        return {"title": "", "body": ""}

    # the first line is the title
    entry_data["title"] = lines.pop(0).strip()

    # absorb meta data lines which begin with a #
    while lines and lines[0].startswith("#"):
        meta = lines.pop(0)
        # remove the hash
        meta = meta[1:].strip()
        meta = meta.split(" ", 1)
        # if there's no value, we append a 1
        if len(meta) == 1:
            meta.append("1")
        entry_data[meta[0].strip()] = meta[1].strip()

    # call the preformat function
    args = {'parser': entry_data.get('parser', config.get('parser', 'plain')),
            'story': lines,
            'request': request}
    entry_data["body"] = tools.run_callback(
        'preformat',
        args,
        donefunc=lambda x: x is not None,
        defaultfunc=lambda x: ''.join(x['story']))

    # call the postformat callbacks
    tools.run_callback('postformat',
                       {'request': request,
                        'entry_data': entry_data})

    return entry_data


def blosxom_file_list_handler(args):
    """This is the default handler for getting entries.  It takes the
    request object in and figures out which entries based on the
    default behavior that we want to show and generates a list of
    EntryBase subclass objects which it returns.

    :param args: dict containing the incoming Request object

    :returns: the content we want to render
    """
    request = args["request"]

    data = request.get_data()
    config = request.get_configuration()

    if data['bl_type'] == 'dir':
        file_list = tools.walk(request,
                               data['root_datadir'],
                               int(config.get("depth", "0")))
    elif data['bl_type'] == 'file':
        file_list = [data['root_datadir']]
    else:
        file_list = []

    entry_list = [FileEntry(request, e, data["root_datadir"]) for e in file_list]

    # if we're looking at a set of archives, remove all the entries
    # that aren't in the archive
    if data.get("pi_yr", ""):
        tmp_pi_mo = data.get("pi_mo", "")
        date_str = "%s%s%s" % (data.get("pi_yr", ""),
                               tools.month2num.get(tmp_pi_mo, tmp_pi_mo),
                               data.get("pi_da", ""))
        entry_list = [x for x in entry_list
                      if time.strftime("%Y%m%d%H%M%S", x["timetuple"]).startswith(date_str)]

    args = {"request": request, "entry_list": entry_list}
    entry_list = tools.run_callback("sortlist",
                                    args,
                                    donefunc=lambda x: x != None,
                                    defaultfunc=blosxom_sort_list_handler)

    args = {"request": request, "entry_list": entry_list}
    entry_list = tools.run_callback("truncatelist",
                                    args,
                                    donefunc=lambda x: x != None,
                                    defaultfunc=blosxom_truncate_list_handler)

    return entry_list


def blosxom_sort_list_handler(args):
    """Sorts the list based on ``_mtime`` attribute such that
    most recently written entries are at the beginning of the list
    and oldest entries are at the end.

    :param args: args dict with ``request`` object and ``entry_list``
                 list of entries

    :returns: the sorted ``entry_list``
    """
    entry_list = args["entry_list"]

    entry_list = [(e._mtime, e) for e in entry_list]
    entry_list.sort()
    entry_list.reverse()
    entry_list = [e[1] for e in entry_list]

    return entry_list


def blosxom_process_path_info(args):
    """Process HTTP ``PATH_INFO`` for URI according to path
    specifications, fill in data dict accordingly.

    The paths specification looks like this:

    - ``/foo.html`` and ``/cat/foo.html`` - file foo.* in / and /cat
    - ``/cat`` - category
    - ``/2002`` - category
    - ``/2002`` - year
    - ``/2002/Feb`` and ``/2002/02`` - Year and Month
    - ``/cat/2002/Feb/31`` and ``/cat/2002/02/31``- year and month day
      in category.

    :param args: dict containing the incoming Request object
    """
    request = args['request']
    config = request.get_configuration()
    data = request.get_data()
    py_http = request.get_http()

    form = request.get_form()

    # figure out which flavour to use.  the flavour is determined by
    # looking at the "flav" post-data variable, the "flav" query
    # string variable, the "default_flavour" setting in the config.py
    # file, or "html"
    flav = config.get("default_flavour", "html")
    if "flav" in form:
        flav = form["flav"].value

    data['flavour'] = flav

    data['pi_yr'] = ''
    data['pi_mo'] = ''
    data['pi_da'] = ''

    path_info = py_http.get("PATH_INFO", "")

    data['root_datadir'] = config['datadir']

    data["pi_bl"] = path_info

    # first we check to see if this is a request for an index and we
    # can pluck the extension (which is certainly a flavour) right
    # off.
    new_path, ext = os.path.splitext(path_info)
    if new_path.endswith("/index") and ext:
        # there is a flavour-like thing, so that's our new flavour and
        # we adjust the path_info to the new filename
        data["flavour"] = ext[1:]
        path_info = new_path

    while path_info and path_info.startswith("/"):
        path_info = path_info[1:]

    absolute_path = os.path.join(config["datadir"], path_info)

    path_info = path_info.split("/")

    if os.path.isdir(absolute_path):

        # this is an absolute path

        data['root_datadir'] = absolute_path
        data['bl_type'] = 'dir'

    elif absolute_path.endswith("/index") and \
            os.path.isdir(absolute_path[:-6]):

        # this is an absolute path with /index at the end of it

        data['root_datadir'] = absolute_path[:-6]
        data['bl_type'] = 'dir'

    else:
        # this is either a file or a date

        ext = tools.what_ext(list(data["extensions"].keys()), absolute_path)
        if not ext:
            # it's possible we didn't find the file because it's got a
            # flavour thing at the end--so try removing it and
            # checking again.
            new_path, flav = os.path.splitext(absolute_path)
            if flav:
                ext = tools.what_ext(list(data["extensions"].keys()), new_path)
                if ext:
                    # there is a flavour-like thing, so that's our new
                    # flavour and we adjust the absolute_path and
                    # path_info to the new filename
                    data["flavour"] = flav[1:]
                    absolute_path = new_path
                    path_info, flav = os.path.splitext("/".join(path_info))
                    path_info = path_info.split("/")

        if ext:
            # this is a file
            data["bl_type"] = "file"
            data["root_datadir"] = absolute_path + "." + ext

        else:
            data["bl_type"] = "dir"

            # it's possible to have category/category/year/month/day
            # (or something like that) so we pluck off the categories
            # here.
            pi_bl = ""
            while len(path_info) > 0 and \
                    not (len(path_info[0]) == 4 and path_info[0].isdigit()):
                pi_bl = os.path.join(pi_bl, path_info.pop(0))

            # handle the case where we do in fact have a category
            # preceding the date.
            if pi_bl:
                pi_bl = pi_bl.replace("\\", "/")
                data["pi_bl"] = pi_bl
                data["root_datadir"] = os.path.join(config["datadir"], pi_bl)

            if len(path_info) > 0:
                item = path_info.pop(0)
                # handle a year token
                if len(item) == 4 and item.isdigit():
                    data['pi_yr'] = item
                    item = ""

                    if len(path_info) > 0:
                        item = path_info.pop(0)
                        # handle a month token
                        if item in tools.MONTHS:
                            data['pi_mo'] = item
                            item = ""

                            if len(path_info) > 0:
                                item = path_info.pop(0)
                                # handle a day token
                                if len(item) == 2 and item.isdigit():
                                    data["pi_da"] = item
                                    item = ""

                                    if len(path_info) > 0:
                                        item = path_info.pop(0)

                # if the last item we picked up was "index", then we
                # just ditch it because we don't need it.
                if item == "index":
                    item = ""

                # if we picked off an item we don't recognize and/or
                # there is still stuff in path_info to pluck out, then
                # it's likely this wasn't a date.
                if item or len(path_info) > 0:
                    data["bl_type"] = "dir"
                    data["root_datadir"] = absolute_path

    # construct our final URL
    url = config['base_url']
    if data['pi_bl'].startswith("/") and url.endswith("/"):
        url = url[:-1] + data['pi_bl']
    elif data['pi_bl'].startswith("/") or url.endswith("/"):
        url = url + data["pi_bl"]
    else:
        url = url + "/" + data['pi_bl']
    data['url'] = url

    # set path_info to our latest path_info
    data['path_info'] = path_info

    if data.get("pi_yr"):
        data["truncate"] = config.get("truncate_date", False)
    elif data.get("bl_type") == "dir":
        if data["path_info"] == [''] or data["path_info"] == ['index']:
            data["truncate"] = config.get("truncate_frontpage", True)
        else:
            data["truncate"] = config.get("truncate_category", True)
    else:
        data["truncate"] = False


def blosxom_truncate_list_handler(args):
    """If ``config["num_entries"]`` is not 0 and ``data["truncate"]``
    is not 0, then this truncates ``args["entry_list"]`` by
    ``config["num_entries"]``.

    :param args: args dict with ``request`` object and ``entry_list``
                 list of entries

    :returns: the truncated ``entry_list``.
    """
    request = args["request"]
    entry_list = args["entry_list"]

    data = request.data
    config = request.config

    num_entries = config.get("num_entries", 5)
    truncate = data.get("truncate", 0)
    if num_entries and truncate:
        entry_list = entry_list[:num_entries]
    return entry_list
