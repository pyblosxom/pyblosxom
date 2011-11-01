
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

=======================================================
 yeararchives - Builds year-based archives listing.... 
=======================================================

Summary
=======

Walks through your blog root figuring out all the available years for
the archives list.  It stores the years with links to year summaries
in the variable ``$(archivelinks)``.  You should put this variable in
either your head or foot template.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.yeararchives`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Add ``$(archivelinks)`` to your head and/or foot templates.

3. Configure as documented below.


Usage
=====

When the user clicks on one of the year links
(e.g. ``http://base_url/2004/``), then yeararchives will display a
summary page for that year.  The summary is generated using the
``yearsummarystory`` template for each month in the year.

My ``yearsummarystory`` template looks like this::

   <div class="blosxomEntry">
   <span class="blosxomTitle">$title</span>
   <div class="blosxomBody">
   <table>
   $body
   </table>
   </div>
   </div>


The ``$(archivelinks)`` link can be configured with the
``archive_template`` config variable.  It uses the Python string
formatting syntax.

Example::

    py['archive_template'] = (
        '<a href="%(base_url)s/%(Y)s/index.%(f)s">'
        '%(Y)s</a><br />')

The vars available with typical example values are::

    Y      4-digit year   ex: '1978'
    y      2-digit year   ex: '78'
    f      the flavour    ex: 'html'

.. Note::

   The ``archive_template`` variable value is formatted using Python
   string formatting rules--not Pyblosxom template rules!


License
=======

Plugin is distributed under license: MIT
