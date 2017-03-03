#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2009, 2010, 2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

This is a tags plugin.  It uses Pyblosxom's command line abilities to
split generation of tags index data from display of tags index data.

It creates a ``$(tagslist)`` variable for head and foot templates
which lists all the tags.

It creates a ``$(tags)`` variable for story templates which lists tags
for the story.

It creates a ``$(tagcloud)`` variable for the tag cloud.

It creates a ``$(feed_tags)`` variable for use in rss-feeds.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.tags`` to the ``load_plugins`` list in your
   ``config.py`` file.

2. Configure as documented below.


Configuration
=============

The following config properties define where the tags file is located,
how tag metadata is formatted, and how tag lists triggered.

``tags_separator``

    This defines the separator between tags in the metadata line.
    Defaults to ",".

    After splitting on the separator, each individual tag is stripped
    of whitespace before and after the text.

    For example::

       Weather in Boston
       #tags weather, boston
       <p>
         The weather in Boston today is pretty nice.
       </p>

    returns tags ``weather`` and ``boston``.

    If the ``tags_separator`` is::

       py["tags_separator"] = "::"

    then tags could be declared in the entries like this::

       Weather in Boston
       #tags weather::boston
       <p>
         The weather in Boston today is pretty nice.
       </p>

``tags_filename``

    This is the file that holds indexed tags data.  Defaults to
    datadir + os.pardir + ``tags.index``.

    This file needs to be readable by the process that runs your blog.
    This file needs to be writable by the process that creates the
    index.

``tags_trigger``

    This is the url trigger to indicate that the tags plugin should
    handle the file list based on the tag.  Defaults to ``tag``.

``truncate_tags``

    If this is True, then tags index listings will get passed through
    the truncate callback.  If this is False, then the tags index
    listing will not be truncated.

    If you're using a paging plugin, then setting this to True will
    allow your tags index to be paged.

    Example::

        py["truncate_tags"] = True

    Defaults to True.


In the head and foot templates, you can list all the tags with the
``$(tagslist)`` variable.  The templates for this listing use the
following three config properties:

``tags_list_start``

    Printed before the list.  Defaults to ``<p>``.

``tags_list_item``

    Used for each tag in the list.  There are a bunch of variables you can
    use:

    * ``base_url`` - the baseurl for your blog
    * ``flavour`` - the default flavour or flavour currently showing
    * ``tag`` - the tag name
    * ``count`` - the number of items that are tagged with this tag
    * ``tagurl`` - url composed of baseurl, trigger, and tag

    Defaults to ``<a href="%(tagurl)s">%(tag)s</a>``.

``tags_list_finish``

    Printed after the list.  Defaults to ``</p>``.


In the head and foot templates, you can also add a tag cloud with the
``$(tagcloud)`` variable.  The templates for the cloud use the
following three config properties:

``tags_cloud_start``

    Printed before the cloud.  Defaults to ``<p>``.

``tags_cloud_item``

    Used for each tag in the cloud list.  There are a bunch of
    variables you can use:

    * ``base_url`` - the baseurl for your blog
    * ``flavour`` - the default flavour or flavour currently showing
    * ``tag`` - the tag name
    * ``count`` - the number of items that are tagged with this tag
    * ``class`` - biggestTag, bigTag, mediumTag, smallTag or smallestTag--the
      css class for this tag representing the frequency the tag is used
    * ``tagurl`` - url composed of baseurl, trigger, and tag

    Defaults to ``<a href="%(tagurl)s">%(tag)s</a>``.

``tags_cloud_finish``

    Printed after the cloud.  Defaults to ``</p>``.

You'll also want to add CSS classes for the size classes to your CSS.
For example, you could add this::

   .biggestTag { font-size: 16pt; }
   .bigTag { font-size: 14pt }
   .mediumTag { font-size: 12pt }
   .smallTag { font-size: 10pt ]
   .smallestTag { font-size: 8pt ]


You can list the tags for a given entry in the story template with the
``$(tags)`` variable.  The tag items in the story are formatted with one
configuration property:

``tags_item``

    This is the template for a single tag for an entry.  It can use the
    following bits:

    * ``base_url`` - the baseurl for this blog
    * ``flavour`` - the default flavour or flavour currently being viewed
    * ``tag`` - the tag
    * ``tagurl`` - url composed of baseurl, trigger and tag

    Defaults to ``<a href="%(tagurl)s">%(tag)s</a>``.

    Tags are joined together with ``,``.

``tags_feed_item``

    This is the template for a single tag for a rss-feed.  It can use the
    following bits:

    * ``base_url`` - the baseurl for this blog
    * ``flavour`` - the default flavour or flavour currently being viewed
    * ``tag`` - the tag
    * ``tagurl`` - url composed of baseurl, trigger and tag

    Defaults to ``<category domain="%(base_url)s">%(tag)s</category>``

    Tags are joined together with ``\n`` (newline).


Creating the tags index file
============================

Run::

    pyblosxom-cmd buildtags

from the directory your ``config.py`` is in or::

    pyblosxom-cmd buildtags --config=/path/to/config/file

from anywhere.

This builds the tags index file that the tags plugin requires to
generate tags-based bits for the request.

Until you rebuild the tags index file, the entry will not have its
tags indexed.  Thus you should either rebuild the tags file after writing
or updating an entry or you should rebuild the tags file as a cron job.

.. Note::

   If you're using static rendering, you need to build the tags
   index before you statically render your blog.


Converting from categories to tags
==================================

This plugin has a command that goes through your entries and adds tag
metadata based on the category.  There are some caveats:

1. it assumes entries are in the blosxom format of title, then
   metadata, then the body.

2. it only operates on entries in the datadir.

It maintains the atime and mtime of the file.  My suggestion is to
back up your files (use tar or something that maintains file stats),
then try it out and see how well it works, and figure out if that
works or not.

To run the command do::

    pyblosxom-cmd categorytotags

from the directory your ``config.py`` is in or::

    pyblosxom-cmd categorytotags --config=/path/to/config/file

from anywhere.
"""

__author__ = "Will Kahn-Greene"
__email__ = "willg at bluesock dot org"
__version__ = "2015-06-14"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Tags plugin"
__category__ = "tags"
__license__ = "MIT"
__registrytags__ = "1.5, core"


import os
import pickle as pickle
import shutil

from Pyblosxom.memcache import memcache_decorator


def savefile(path, tagdata):
    """Saves tagdata to file at path."""
    fp = open(path + ".new", "w")
    pickle.dump(tagdata, fp)
    fp.close()

    shutil.move(path + ".new", path)


@memcache_decorator('tags')
def loadfile(path):
    """Loads tagdata from file at path."""
    fp = open(path, "r")
    tagdata = pickle.load(fp)
    fp.close()
    return tagdata


def get_tagsfile(cfg):
    """Generates tagdata filename."""
    datadir = cfg["datadir"]
    tagsfile = cfg.get("tags_filename",
                       os.path.join(datadir, os.pardir, "tags.index"))
    return tagsfile


def buildtags(command, argv):
    """Command for building the tags index."""
    import config

    datadir = config.py.get("datadir")
    if not datadir:
        raise ValueError("config.py has no datadir property.")

    sep = config.py.get("tags_separator", ",")
    tagsfile = get_tagsfile(config.py)

    from Pyblosxom.pyblosxom import Pyblosxom
    from Pyblosxom import tools
    from Pyblosxom.entries import fileentry

    # build a Pyblosxom object, initialize it, and run the start
    # callback.  this gives entry parsing related plugins a chance to
    # get their stuff together so that they work correctly.
    p = Pyblosxom(config.py, {})
    p.initialize()
    req = p.get_request()
    tools.run_callback("start", {"request": req})

    # grab all the entries in the datadir
    filelist = tools.walk(req, datadir)
    entrylist = [fileentry.FileEntry(req, e, datadir) for e in filelist]

    tags_to_files = {}
    for mem in entrylist:
        tagsline = mem["tags"]
        if not tagsline:
            continue
        tagsline = [t.strip() for t in tagsline.split(sep)]
        for t in tagsline:
            tags_to_files.setdefault(t, []).append(mem["filename"])

    savefile(tagsfile, tags_to_files)
    return 0


def category_to_tags(command, argv):
    """Goes through all entries and converts the category to tags
    metadata.

    It adds the tags line as the second line.

    It maintains the mtime for the file.
    """
    import config

    datadir = config.py.get("datadir")
    if not datadir:
        raise ValueError("config.py has no datadir property.")

    sep = config.py.get("tags_separator", ",")

    from Pyblosxom.pyblosxom import Request
    from Pyblosxom.blosxom import blosxom_entry_parser
    from Pyblosxom import tools

    data = {}

    # register entryparsers so that we parse all possible file types.
    data["extensions"] = tools.run_callback("entryparser",
                                            {"txt": blosxom_entry_parser},
                                            mappingfunc=lambda x, y: y,
                                            defaultfunc=lambda x: x)

    req = Request(config.py, {}, data)

    # grab all the entries in the datadir
    filelist = tools.walk(req, datadir)

    if not datadir.endswith(os.sep):
        datadir = datadir + os.sep

    for mem in filelist:
        print("working on %s..." % mem)

        category = os.path.dirname(mem)[len(datadir):]
        tags = category.split(os.sep)
        print("   adding tags %s" % tags)
        tags = "#tags %s\n" % (sep.join(tags))

        atime, mtime = os.stat(mem)[7:9]

        fp = open(mem, "r")
        data = fp.readlines()
        fp.close()

        data.insert(1, tags)

        fp = open(mem, "w")
        fp.write("".join(data))
        fp.close()

        os.utime(mem, (atime, mtime))

    return 0


def cb_commandline(args):
    args["buildtags"] = (buildtags, "builds the tags index")
    args["categorytotags"] = (
        category_to_tags,
        "builds tag metadata from categories for entries")
    return args


def cb_start(args):
    request = args["request"]
    data = request.get_data()
    tagsfile = get_tagsfile(request.get_configuration())
    if os.path.exists(tagsfile):
        try:
            tagsdata = loadfile(tagsfile)
        except IOError:
            tagsdata = {}
    else:
        tagsdata = {}
    data["tagsdata"] = tagsdata


def cb_filelist(args):
    from Pyblosxom.blosxom import blosxom_truncate_list_handler
    from Pyblosxom import tools

    # handles /trigger/tag to show all the entries tagged that
    # way
    req = args["request"]

    pyhttp = req.get_http()
    data = req.get_data()
    config = req.get_configuration()

    trigger = "/" + config.get("tags_trigger", "tag")
    if not pyhttp["PATH_INFO"].startswith(trigger):
        return

    datadir = config["datadir"]
    tagsfile = get_tagsfile(config)
    tagsdata = loadfile(tagsfile)

    tag = pyhttp["PATH_INFO"][len(trigger) + 1:]
    filelist = tagsdata.get(tag, [])
    if not filelist:
        tag, ext = os.path.splitext(tag)
        filelist = tagsdata.get(tag, [])
        if filelist:
            data["flavour"] = ext[1:]

    from Pyblosxom.entries import fileentry
    entrylist = [fileentry.FileEntry(req, e, datadir) for e in filelist]

    # sort the list by mtime
    entrylist = [(e._mtime, e) for e in entrylist]
    entrylist.sort()
    entrylist.reverse()
    entrylist = [e[1] for e in entrylist]

    data["truncate"] = config.get("truncate_tags", True)

    args = {"request": req, "entry_list": entrylist}
    entrylist = tools.run_callback("truncatelist",
                                   args,
                                   donefunc=lambda x: x != None,
                                   defaultfunc=blosxom_truncate_list_handler)

    return entrylist


def cb_story(args):
    # adds tags to the entry properties
    request = args["request"]
    entry = args["entry"]
    config = request.get_configuration()

    sep = config.get("tags_separator", ",")
    tags = [t.strip() for t in entry.get("tags", "").split(sep)]
    feed_tags = [t.strip() for t in entry.get("tags", "").split(sep)]
    tags.sort()
    entry["tags_raw"] = tags

    form = request.get_form()
    try:
        flavour = form["flav"].value
    except KeyError:
        flavour = config.get("default_flavour", "html")
    baseurl = config.get("base_url", "")
    trigger = config.get("tags_trigger", "tag")
    template = config.get("tags_item", '<a href="%(tagurl)s">%(tag)s</a>')
    feed_template = config.get("tags_feed_item", '<category domain="%(base_url)s">%(tag)s</category>')

    tags = [template % {"base_url": baseurl,
                        "flavour": flavour,
                        "tag": tag,
                        "tagurl": "/".join([baseurl, trigger, tag])}
            for tag in tags]
    entry["tags"] = ", ".join(tags)

    feed_tags = [feed_template % {"base_url": baseurl,
                        "flavour": flavour,
                        "tag": tag,
                        "baseurl": "/".join([baseurl, trigger, tag])}
            for tag in feed_tags]
    entry["feed_tags"] = "\n ".join(feed_tags)
    return args


def cb_head(args):
    # adds a taglist to header/footer
    request = args["request"]
    entry = args["entry"]
    data = request.get_data()
    config = request.get_configuration()
    tagsdata = data.get("tagsdata", {})

    # first, build the tags list
    tags = list(tagsdata.keys())
    tags.sort()

    start_t = config.get("tags_list_start", '<p>')
    item_t = config.get("tags_list_item", ' <a href="%(tagurl)s">%(tag)s</a> ')
    finish_t = config.get("tags_list_finish", '</p>')

    output = []

    form = request.get_form()
    try:
        flavour = form["flav"].value
    except KeyError:
        flavour = config.get("default_flavour", "html")
    baseurl = config.get("base_url", "")
    trigger = config.get("tags_trigger", "tag")

    output.append(start_t)
    for item in tags:
        d = {"base_url": baseurl,
             "flavour": flavour,
             "tag": item,
             "count": len(tagsdata[item]),
             "tagurl": "/".join([baseurl, trigger, item])}
        output.append(item_t % d)
    output.append(finish_t)

    entry["tagslist"] = "\n".join(output)

    # second, build the tags cloud
    tags_by_file = list(tagsdata.items())

    start_t = config.get("tags_cloud_start", "<p>")
    item_t = config.get("tags_cloud_item",
                        '<a class="%(class)s" href="%(tagurl)s">%(tag)s</a>')
    finish_t = config.get("tags_cloud_finish", "</p>")

    tagcloud = [start_t]

    if len(tags_by_file) > 0:
        tags_by_file.sort(key=lambda x: len(x[1]))
        # the most popular tag is at the end--grab the number of files
        # that have that tag
        max_count = len(tags_by_file[-1][1])
        min_count = len(tags_by_file[0])

        # figure out the bin size for the tag size classes
        b = (max_count - min_count) / 5

        range_and_class = (
            (min_count + (b * 4), "biggestTag"),
            (min_count + (b * 3), "bigTag"),
            (min_count + (b * 2), "mediumTag"),
            (min_count + b, "smallTag"),
            (0, "smallestTag")
            )

        # sorts it alphabetically
        tags_by_file.sort()

        for tag, files in tags_by_file:
            len_files = len(files)
            for tag_range, tag_size_class in range_and_class:
                if len_files > tag_range:
                    tag_class = tag_size_class
                    break

            d = {"base_url": baseurl,
                 "flavour": flavour,
                 "class": tag_class,
                 "tag": tag,
                 "count": len(tagsdata[tag]),
                 "tagurl": "/".join([baseurl, trigger, tag])}

            tagcloud.append(item_t % d)

    tagcloud.append(finish_t)
    entry["tagcloud"] = "\n".join(tagcloud)

    return args


cb_foot = cb_head


def cb_staticrender_filelist(args):
    req = args["request"]

    # We call our own cb_start() here because we need to initialize
    # the tagsdata.
    cb_start({"request": req})

    config = req.get_configuration()
    filelist = args["filelist"]

    tagsdata = req.get_data()["tagsdata"]
    index_flavours = config.get("static_index_flavours", ["html"])
    trigger = "/" + config.get("tags_trigger", "tag")

    # Go through and add an index.flav for each index_flavour
    # for each tag.
    for tag in list(tagsdata.keys()):
        for flavour in index_flavours:
            filelist.append((trigger + "/" + tag + "." + flavour, ""))
