#!/usr/bin/env python

import os.path, sys, os
from distutils.core import setup

def Walk(root='.'):
    """
    A really really scaled down version of what we have in tools.py.
    """
    # initialize
    result = []

    # must have at least root folder
    try:
        names = os.listdir(root)
    except os.error:
        return result

    # check each file
    for name in names:
        if name == "CVS":
            continue
        fullname = os.path.normpath(os.path.join(root, name))

        # recursively scan other folders, appending results
        if os.path.isdir(fullname) and not os.path.islink(fullname):
            result.append(fullname)
            result = result + Walk(fullname)
                
    return result

# this affects the names of all the directories we do stuff with
VERSION="cvs"
PVER = "pyblosxom-" + VERSION

# we grab all the files in the contrib directory
contrib_folders = Walk("contrib")

doc_files = ["INSTALL", "LICENSE", 
             os.path.normpath("docs/README.contrib"), 
             os.path.normpath("docs/README.plugins"), 
             os.path.normpath("docs/ReadMeForPlugins.py")]

# FIXME - this doesn't account for a variety of platforms
if sys.platform == "win32":
    pydf = []
    root = "c:\\Program Files\\" + PVER + "\\"

    for mem in contrib_folders:
        f = os.listdir(mem)
        f = [mem + os.sep + m for m in f if os.path.isfile(mem + os.sep + m)]
        pydf.append( (root + mem, f) )

elif sys.platform in ["linux1", "linux2"]:
    pydf = []

    root = "/usr/share/" + PVER + "/"
    for mem in contrib_folders:
        f = os.listdir(mem)
        f = [mem + os.sep + m for m in f if os.path.isfile(mem + os.sep + m)]
        pydf.append( (root + mem, f) )
        print repr((root + mem, f))

    # we want to move the web script files as well, so we sneak them
    # in here.
    pydf.append( ("/usr/share/doc/" + PVER, doc_files) )
    pydf.append( ("/usr/share/" + PVER + "/web", ["web/pyblosxom.cgi", 
                                                  "web/xmlrpc.cgi", 
                                                  "web/config.py"]) )


else:
    # we don't know what platform they have, so we print out
    # this message and hope they tell us.  it'd be nice if i
    # could find a listing of the possible platforms, but i suck.
    # (wbg 7/31/2003)
    pydf = []
    print """
NOTE: We want to install documentation, contributed plugins, and
the web scripts to some central location where you can access them.
However, we don't know where to put it for your platform.  If you could
send an email to <pyblosxom-users@lists.sourceforge.net> with the following
information:

  Dear Pyblosxom Users,
  I have platform '""" + sys.platform + """' and you told me to send you
  an email with this information!
  Sincerely,
  <your name>

Thanks!

In the meantime, you'll have to put the docs, contributed plugins, and
web scripts where you want them on your own.  They're in subdirectories
of this one: web/, contrib/ and docs/ .  Sorry for the inconvenience.
"""


if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

print "## Pyblosxom debug"
print "## version: " + VERSION
print "## datafiles: " + repr(pydf)

setup(name="pyblosxom",
    version=VERSION,
    description="pyblosxom weblog engine",
    author="Wari Wahab",
    author_email="wari@home.wari.org",
    url="http://roughingit.subtlehints.net/pyblosxom",
    packages=['Pyblosxom', 'Pyblosxom.cache', 'Pyblosxom.entries', 'Pyblosxom.renderers'],
    license = 'MIT',
    long_description =
"""Pyblosxom is a weblog engine that uses the filesystem as the database of
your entries.
""",
    data_files=pydf,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console (Text Based), Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT/X Consortium License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
        ],
    )

