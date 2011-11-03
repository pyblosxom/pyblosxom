
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

=====================================================
 rst_parser - restructured text support for blog ... 
=====================================================

Summary
=======

A reStructuredText entry formatter for pyblosxom.  reStructuredText is
part of the docutils project (http://docutils.sourceforge.net/).  To
use, you need a *recent* version of docutils.  A development snapshot
(http://docutils.sourceforge.net/#development-snapshots) will work
fine.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.rst_parser`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Install docutils.  Instructions are at
   http://docutils.sourceforge.net/


Usage
=====

Blog entries with a ``.rst`` extension will be parsed as
restructuredText.

You can also configure this as your default preformatter for ``.txt``
files by configuring it in your config file as follows::

   py['parser'] = 'reST'

Additionally, you can do this on an entry-by-entry basis by adding a
``#parser reST`` line in the metadata section.  For example::

   My Little Blog Entry
   #parser reST
   My main story...


Configuration
=============

There's two optional configuration parameter you can for additional
control over the rendered HTML::

   # To set the starting level for the rendered heading elements.
   # 1 is the default.
   py['reST_initial_header_level'] = 1

   # Enable or disable the promotion of a lone top-level section title to
   # document title (and subsequent section title to document subtitle
   # promotion); enabled by default.
   py['reST_transform_doctitle'] = 1


.. Note::

   If you're not seeing headings that you think should be there, try
   changing the ``reST_initial_header_level`` property to 0.


License
=======

Plugin is distributed under license: MIT
