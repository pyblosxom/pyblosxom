#!/usr/bin/python

#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
This script generates documentation for plugins from the plugin docstrings.
"""

import os
import ast
import sys


# skip these because they're not plugins
SKIP = ("akismet.py", "__init__.py")


HELP = """extract_docs_from_plugins

This goes through the plugins in ../Pyblosxom/plugins/, extracts the
docstrings, and generates docs files for each one.  It puts them all in
a plugins/ directory here.

Docstrings for plugins should be formatted in restructured text.
"""

TEMPLATE = """
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

%(line)s
%(title)s
%(line)s

%(body)s


License
=======

Plugin is distributed under license: %(license)s
"""

def get_info(node, info_name):
    # FIXME - this is inefficient since it'll traverse the entire ast
    # but we only really need to look at the top level.
    for mem in ast.walk(node):
        if not isinstance(mem, ast.Assign):
            continue

        for target in mem.targets:
            if not isinstance(target, ast.Name):
                continue

            if target.id == info_name:                
                return mem.value.s

    print("missing %s" % info_name)
    return None


def build_docs_file(filepath):
    try:
        fp = open(filepath, "r")
    except (IOError, OSError):
        return False

    node = ast.parse(fp.read(), filepath, 'exec')

    title = (" %s - %s... " % (
            os.path.splitext(os.path.basename(filepath))[0],
            get_info(node, "__description__")[:35]))
    line = "=" * len(title)
    body = ast.get_docstring(node, True)
    license_ = get_info(node, "__license__")

    return (TEMPLATE % {
            "line": line,
            "title": title,
            "body": body,
            "license": license_})


def save_entry(filepath, entry):
    parent = os.path.dirname(filepath)
    if not os.path.exists(parent):
        os.makedirs(parent)

    f = open(filepath, "w")
    f.write(entry)
    f.close()


def get_plugins(plugindir, outputdir):
    for root, dirs, files in os.walk(plugindir):
        # remove skipped directories so we don't walk through them
        for mem in SKIP:
            if mem in dirs:
                dirs.remove(mem)
                break

        for file_ in files:
            if ((file_.startswith("_") or not file_.endswith(".py") or
                 file_ in SKIP)):
                continue

            filename = os.path.join(root, file_)
            print("working on %s" % filename)

            entry = build_docs_file(filename)

            output_filename = os.path.basename(filename)
            output_filename = os.path.splitext(output_filename)[0] + ".rst"
            output_filename = os.path.join(outputdir, output_filename)

            save_entry(output_filename, entry)


def main(args):
    print("update_registry.py")

    outputdir = "./plugins/"

    plugindir = "../Pyblosxom/plugins/"

    print("plugindir: %s" % plugindir)
    if not os.path.exists(plugindir):
        print("Plugindir doesn't exist.")
        sys.exit(1)

    print("outputdir: %s" % outputdir)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    get_plugins(plugindir, outputdir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
