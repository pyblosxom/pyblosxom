#######################################################################
# This file is part of PyBlosxom.
#
# Copyright (c) 2010 Will Kahn-Greene
#
# PyBlosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
Summary
=======

This plugin marks abbreviations and acronyms based on an
acronyms/abbreviations files.

To install, do the following:

1. Add ``acronyms`` to the ``load_plugins`` list variable in your
   config.py file::

       py["load_plugins"] = [... "acronyms"]

2. Create an acronyms file with acronyms and abbreviations in it.

   See below for the syntax.

3. Specify the location of the file with the ``acronyms_file``
   variable in your config.py file.

   The default is ``acronyms.txt`` in the parent directory to your
   datadir.


Usage
=====

When writing a blog entry, just write the acronyms and abbreviations
and they'll be marked up by the plugin in the story callback.

If you're writing an entry that you don't want to have marked up, add
this to the metadata for the entry::

    #noacronyms 1


Building the acronyms file
==========================

The file should be a text file with one acronym or abbreviation
followed by an = followed by the explanation.  The
acronym/abbreviation is a regular expression and can contain regular
expression bits.

An acronym is upper or lower case letters that is NOT followed by a
period.  If it's followed by a period, then you need to explicitly
state it's an acronym.

    <acronym> = explanation
    <acronym> = acronym|explanation

Examples::

    ASCII = American Standard Code for Information Interchange
    CGI = Common Gateway Interface; Computer Generated Imagery
    CSS = Cascading Stylesheets
    HTML = Hypertext Markup Language
    HTTP = Hypertext Transport Protocol
    RDF = Resource Description Framework
    RSS = Really Simple Sindication
    URL = Uniform Resource Locator
    URI = Uniform Resource Indicator
    WSGI = Web Server Gateway Interface
    XHTML = Extensible Hypertext Markup Language
    XML = Extensible Markup Language

This one is explicitly labeled an acronym::

    X.M.L. = acronym|Extensible Markup Language

This one uses regular expression to match both ``UTF-8`` and
``UTF8``::

    UTF\-?8 = 8-bit UCS/Unicode Transformation Format

An abbreviation is a series of characters followed by a period.  If
it's not followed by a period, then you need to explicitly state that
it's an abbreviation.

    <abbreviation> = explanation
    <abbreviation> = abbr|explanation

Examples::

    dr. = doctor

This one is explicitly labeled an abbreviation::

    dr = abbr|doctor

.. Note::

   If the first part is an improperly formed regular expression, then
   it will be skipped.

   You can verify that your file is properly formed by running
   ``pyblosxom-cmd test``.


Styling
=======

Might want to add something like this to your CSS::

    acronym {
        bordor-bottom: 1px dashed #aaa;
        cursor: help;
    }

    abbr {
        bordor-bottom: 1px dashed #aaa;
        cursor: help;
    }


Origins
=======

Based on the Blosxom acronyms plugin by Axel Beckert at
http://noone.org/blosxom/acronyms .
"""
__author__ = "Will Kahn-Greene - willg at bluesock dot org"
__version__ = "2010-05-07"
__url__ = "http://pyblosxom.sourceforge.net/"
__description__ = "Marks acronyms and abbreviations in blog entries."

import os
import re

from Pyblosxom import tools

def get_acronym_file(cfg):
    datadir = cfg["datadir"]
    filename = cfg.get("acronym_file",
                       os.path.join(datadir, os.pardir, "acronyms.txt"))
    return filename

def verify_installation(request):    
    config = request.get_configuration()
    filename = get_acronym_file(config)
    if not os.path.exists(filename):
        print "There is no acronym file at %s." % filename
        print "You should create one.  Refer to documentation for examples."
        return 0

    try:
        fp = open(filename, "r")
    except IOError:
        print "Your acronyms file %s cannot be opened for reading." % filename
        print "Please adjust the permissions."
        return 0

    malformed = False

    # FIXME - this is a repeat of build_acronyms
    for line in fp.readlines():
        line = line.strip()
        firstpart = line.split("=", 1)[0]
        firstpart = "(\\b" + firstpart.strip() + "\\b)"
        try:
            firstpartre = re.compile(firstpart)
        except re.error, s:
            print "- '%s' is not a properly formed regexp.  (%s)" % (line, s)
            malformed = True
    fp.close()
    if malformed:
        return 0
    return 1

def build_acronyms(lines):
    acronyms = []
    for line in lines:
        line = line.split("=", 1)
        firstpart = line[0].strip()

        try:
            firstpartre = re.compile("(\\b" + firstpart + "\\b)")
        except re.error:
            logger = tools.get_logger()
            logger.error("acronyms: '%s' is not a regular expression",
                         firstpart)
            continue

        secondpart = line[1].strip()
        secondpart = secondpart.replace("\"", "&quot;")

        if (secondpart.startswith("abbr|") or firstpart.endswith(".")):
            if secondpart.startswith("abbr|"):
                secondpart = secondpart[5:]
            repl = "<abbr title=\"%s\">\\1</abbr>" % secondpart
        else:
            if secondpart.startswith("acronym|"):
                secondpart = secondpart[8:]
            repl = "<acronym title=\"%s\">\\1</acronym>" % secondpart

        acronyms.append((firstpartre, repl))
    return acronyms

def cb_start(args):
    request = args["request"]
    config = request.get_configuration()
    filename = get_acronym_file(config)

    try:
        fp = open(filename, "r")
    except IOError:
        return

    lines = fp.readlines()
    fp.close()

    request.get_data()["acronyms"] = build_acronyms(lines)

TAG_RE = re.compile("<\D.*?>")
TAG_DIGIT_RE = re.compile("<\d+?>")

def cb_story(args):
    request = args["request"]
    acrolist = request.get_data()["acronyms"]
    entry = args["entry"]

    if entry.get("noacronyms"):
        return args
    
    body = entry.get("body", "")

    tags = {}
    def matchrepl(matchobj):
        ret = "<%d>" % len(tags)
        tags[ret] = matchobj.group(0)
        return ret

    body = TAG_RE.sub(matchrepl, body)

    for reob, repl in acrolist:
        body = reob.sub(repl, body)

    def matchrepl(matchobj):
        return tags[matchobj.group(0)]

    body = TAG_DIGIT_RE.sub(matchrepl, body)

    entry["body"] = body
    return args
