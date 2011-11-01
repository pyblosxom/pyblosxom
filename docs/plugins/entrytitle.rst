
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

=================================================
 entrytitle - Puts entry title in page title.... 
=================================================

Summary
=======

If PyBlosxom is rendering a single entry (i.e. entry_list has 1 item in it),
then this populates the ``entry_title`` variable for the header template.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.entrytitle`` to the ``load_plugins`` list
   of your ``config.py`` file.

2. Configure as documented below.


Configuration
=============

To use, add the ``entry_title`` variable to your header template in
the ``<title>`` area.

Example::

    <title>$(blog_title)$(entry_title)</title>

The default ``$(entry_title)`` starts with a ``::`` and ends with the
title of the entry.  For example::

    :: Guess what happened today

You can set the entry title template in the configuration properties
with the ``entry_title_template`` variable::

    config["entry_title_template"] = ":: %(title)s"

.. Note::

   ``%(title)s`` is a Python string formatter that gets filled in with
   the entry title.


License
=======

Plugin is distributed under license: MIT
