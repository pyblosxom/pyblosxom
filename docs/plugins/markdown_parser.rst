
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

============================================
 markdown_parser - Markdown entry parser... 
============================================

Summary
=======

A Markdown entry formatter for Pyblosxom.


Install
=======

Requires python-markdown to be installed.  See
http://www.freewisdom.org/projects/python-markdown/ for details.

1. Add ``Pyblosxom.plugins.markdown_parser`` to the ``load_plugins``
   list in your ``config.py`` file


Usage
=====

Write entries using Markdown markup.  Entry filenames can end in
``.markdown``, ``.md``, and ``.mkd``.

You can also configure this as your default preformatter for ``.txt``
files by configuring it in your config file as follows::

   py['parser'] = 'markdown'

Additionally, you can do this on an entry-by-entry basis by adding a
``#parser markdown`` line in the metadata section.  For example::

   My Little Blog Entry
   #parser markdown
   My main story...


License
=======

Plugin is distributed under license: GPLv3 or later
