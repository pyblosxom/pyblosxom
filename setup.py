#!/usr/bin/env python

import os.path, sys, os
from distutils.core import setup

# this affects the names of all the directories we do stuff with
sys.path.insert(0, "./")
from Pyblosxom import pyblosxom

VER = pyblosxom.VERSION
PVER = "pyblosxom-" + VER

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

doc_files = ["INSTALL", "LICENSE", 
             os.path.normpath("docs/README.plugins"), 
             os.path.normpath("docs/ReadMeForPlugins.py")]

# FIXME - this doesn't account for a variety of platforms
platform = sys.platform
matrix = { "win32": "win32",
           "linux": "nix",
           "cygwin": "nix",
           "netbsd": "nix",
           "openbsd": "nix",
           "darwin": "nix",
           "freebsd": "nix" }

for mem in matrix.keys():
    if platform.startswith(mem):
        platform = matrix[mem]
        break

if platform == "win32":
    pydf = []
    root = "c:\\Program Files\\" + PVER + "\\"

elif platform == "nix":
    pydf = []

    # we want to move the web script files as well, so we sneak them
    # in here.
    pydf.append( [os.path.join('share', PVER, 'web'),
                  [os.path.normpath("web/pyblosxom.cgi"), 
                   os.path.normpath("web/pyblosxom.tac"), 
                   os.path.normpath("web/wsgi_app.py"), 
                   os.path.normpath("web/config.py")]])

else:
    # we don't know what platform they have, so we print out
    # this message and hope they tell us.  it'd be nice if i
    # could find a listing of the possible platforms, but i suck.
    # (wbg 7/31/2003)
    pydf = []
    print """
NOTE: We want to install documentation and the web scripts to some 
central location where you can access them.  However, we don't know 
where to put it for your platform.  If you could send an email to 
<pyblosxom-users@lists.sourceforge.net> with the following information:

  Dear Pyblosxom Users,
  I have platform '""" + sys.platform + """' and you told me to send you
  an email with this information!
  Sincerely,
  <your name>

Thanks!

In the meantime, you'll have to put the docs and web scripts where you 
want them on your own.  They're in subdirectories of this one: web/ 
and docs/ .  Sorry for the inconvenience.
"""


if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name="pyblosxom",
    version=VER,
    description="pyblosxom weblog engine",
    author="Wari Wahab",
    author_email="pyblosxom-devel@lists.sourceforge.net",
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
