What's new in 1.4.3 (January 2008)
==================================

Pertinent to users
------------------

1. Adjusted the code that parses blog.ini values so that it can take
   values like::

      foo = 'a'                 # string
      foo = "a"                 # string
      foo = 23                  # integer
      foo = [ "a", 23, "b" ]    # list of strings and integers

   as well as::

      foo = a                   # string

   Note: if you want the string "23", then you MUST enclose it in
   quotes, otherwise it will be parsed as an integer.

   blog.ini is used when you set up PyBlosxom using Paste.

2. Fixed PyBlosxomWSGIApp so that it's WSGI compliant as an
   application.  Thanks Michael!

3. Template variables can be parenthesized.  Examples::

      $foo                      - variable is "foo"
      $(foo)                    - variable is "foo"
      $(url)index.atom          - variable is "url"

   This reduces ambiguity which was causing problems with recognition
   of variables.


Pertinent to developers
-----------------------

1. Fixed tools.importname---it now logs errors to the logger.

2. Fixed PyBlosxomWSGIApp so that it's WSGI compliant as an
   application.  Thanks Michael!

3. Added more unit tests and corrected more behavior.  Details on
   running unit tests are in the REDAME.


What's new in 1.4.2 (August 2007)
=================================

Pertinent to users
------------------

1. Fixed another bug with the WSGI application creation code.  (Thanks
   Christine!)

2. Added instructions for installing PyBlosxom with mod_wsgi to
   ``install_wsgi.txt``.  This includes a basic wsgi script for
   PyBlosxom.  (Thanks Christine!)

3. Fixed up the Python Paste installation document.  (Thanks Liz!)

4. Fixed the ``month2num`` code in tools so that PyBlosxom runs on
   Windows (Windows doesn't have ``nl_langinfo`` in the ``locale``
   module).  (Thanks Liz!)


What's new in 1.4.1 (July 2007)
===============================

Pertinent to users
------------------

1. Fixed a problem where running PyBlosxom under Paste won't pick up
   the ``config.py`` file.  Be sure to add a ``configpydir`` property
   to your ``blog.ini`` file which points to the directory your
   ``config.py`` file is in.

2. Fixed a problem where running PyBlosxom in Python 2.5 won't pick up
   the ``config.py`` file.

3. Merged Ryan's optimization to Walk (removes an os.listdir call).

4. Updated documentation.


What's new in 1.4 (July 2007)
=============================

Pertinent to users
------------------

1. Added a pyblcmd command line program for PyBlosxom command line
   things.  This now handles static rendering, rendering a single url
   to stdout, testing your blog setup, ...

2. The Atom story template now has a $default_flavour bit in the link.
   Bug 1667937.  (Thanks Michael!)

3. PyBlosxom is now locale aware in respects to dates, months, days of
   the week and such.  Users should set the locale config property to
   a valid locale if they don't want English.

4. Added a ``blog_icbm`` config variable for use in the ICBM meta tag.
   See config_variables.txt for more information.

5. Changed the ``num_entries`` property in config.py from 40 to a much
   more conservative 5.  Also changed the default value from 0 to 5 if
   you happened not to set ``num_entries`` at all.
   http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=373658 (Thanks
   Jon!)

6. Changed the self link in the atom feed to be of type
   application/atom+xml.
   http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=403008 (Thanks
   Brian!)

7. Added DOCUMENT_ROOT to the python path per Martin's suggestion.
   http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=367127 (Thanks
   Martin!)

8. Translated all documentation from Docbook to reST.  reST
   documentation is easier to read in "source-form" and a lot easier
   to convert to HTML and other formats using the Python docutils
   tools.  (Thanks John!)

9. Added support for Paste and brought the WSGI support into the
   codebase.  (Thanks Steven and Yury!)


Pertinent to developers
-----------------------

1. Lots of code clean-up, documentation, test-code, and some
refactoring.

2. cb_filestat will only do an os.stat if no plugin handles the
   filestat.  Previously, cb_filestat did an os.stat and ran through
   all the plugins allowing them to over-ride it.

3. Added some testing framework pieces.  This requires nose.  To run
   the tests, do::

      nosetests --verbose --include unit
      nosetests --verbose --include functional

