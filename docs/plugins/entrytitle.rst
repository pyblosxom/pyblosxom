====================
 Plugin: entrytitle 
====================

Summary
=======

If PyBlosxom is rendering a single entry (i.e. entry_list has 1 item in it),
then this populates the ``entry_title`` variable for the header template.


Usage
=====

To use, add the ``$entry_title`` variable to your header template in the
``<title>`` area.

Example::

    <title>$(blog_title)$(entry_title)</title>

The default ``$(entry_title)`` starts with a ``::`` and ends with the title
of the entry.  For example::

    :: Guess what happened today

You can set the entry title template in the configuration properties
with the ``entry_title_template`` variable::

    config["entry_title_template"] = ":: %(title)s"

The ``%(title)s`` is a Python string formatter that gets filled in with
the entry title.