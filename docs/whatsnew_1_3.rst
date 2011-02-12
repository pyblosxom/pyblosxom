What's new in 1.3.2
===================

Pertinent to users
------------------

1. Fixes a security issue where the path_info can come in with
   multiple / at the beginning.  Whether this happens or not depends
   on the web-server you're using and possibly other things.  Some
   people have the issue and some don't.  If you're in doubt, upgrade.
   Thanks FX!


What's new in 1.3.1
===================

Pertinent to users
------------------

1. The ``num_entries`` property now affects the home page and category
   index pages.  It no longer affects archive index pages.

2. Fixed the RSS 0.9.1 feed templates.  It has the correct link url
   and shows the entry bodies.  Thanks Norbert!

3. The version string is correct.

4. Added support for ``$body_escaped`` .

5. Fixed the blog encoding on the RSS 2.0 feed so that it uses the
   value provided in the config.py ``$blog_encoding`` variable.

6. Fixed the Atom 1.0 story flavour to use ``$body_escaped`` instead
   of ``<![CDATA[ $body ]]>``

7. Fixed a problem with static rendering where we'd render
   ``/index.html`` and ``//index.html`` if the user had entries in
   their root category.


Pertinent to developers
-----------------------

1. If you have plugins that use the logger functions in PyBlosxom 1.2,
   you need to update those plugins to use the new logger functions in
   PyBlosxom 1.3.  Read through the API for details.

2. Moved documentation in ReadMeForPlugins.py over to the manual.



What's new in 1.3
=================

Pertinent to users
------------------

1. We added a ``blog_rights`` property.  This holds a textual
   description of the rights you give to others who read your blog.
   Leaving this blank or not filling it in will affect the RSS 2.0 and
   Atom 1.0 feeds.

2. If you set ``flavourdir``in your config.py file, you have to put
   your flavour files in that directory tree.  If you don't set
   ``flavourdir``, then PyBlosxom expects to find your flavour files
   in your ``datadir``.

   The flavour overhaul is backwards compatible with previous
   PyBlosxom versions.  So if you want to upgrade your blog, but don't
   want to move your flavour files to a new directory, DON'T set your
   ``flavourdir`` property.

3. Moved the content that was in README to CHANGELOG.

4. You can now organize the directory hierarchy of your blog by date.
   For example, you could create a category for each year and put
   posts for that year in that year (2003, 2004, 2005, ...).
   Previously URLs requesting "2003", "2004", ... would get parsed as
   dates and would pull blog entries by mtime and not by category.

5. Logging works now.  The following configuration properties are
   useful for determining whether events in PyBlosxom are logged and
   what will get logged:

   * "log_file" - the file that PyBlosxom events will be logged
     to---the web-server MUST be able to write to this file.

   * "log_level" - the level of events to write to the log.  options
     are "critical", "error", "warning", "info", and "debug"

   * "log_filter" - the list of channels that should have messages
     logged.  if you set the log_filter and omit "root", then
     app-level messages are not logged.

   It's likely you'll want to set log_file and log_level and that's
   it.  Omit log_file and logging will fall back to stderr which
   usually gets logged to your web-server's error log.


Pertinent to developers and plugin developers
---------------------------------------------

1. Plugins that used logging in 1.2 need to be changed to use the new
   logging utilities in 1.3.  Until that happens, they won't work.

