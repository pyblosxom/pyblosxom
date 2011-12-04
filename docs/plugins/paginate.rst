
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

===================================================
 paginate - Allows navigation by page for index... 
===================================================

Summary
=======

Plugin for paging long index pages.

Pyblosxom uses the num_entries configuration variable to prevent more
than ``num_entries`` being rendered by cutting the list down to
``num_entries`` entries.  So if your ``num_entries`` is set to 20, you
will only see the first 20 entries rendered.

The paginate overrides this functionality and allows for paging.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.paginate`` to your ``load_plugins`` list
   variable in your ``config.py`` file.

   Make sure it's the first plugin in the ``load_plugins`` list so
   that it has a chance to operate on the entry list before other
   plugins.

2. add the ``$(page_navigation)`` variable to your head or foot (or
   both) templates.  this is where the page navigation HTML will
   appear.


Here are some additional configuration variables to adjust the
behavior::

``paginate_count_from``

   Defaults to 0.

   This is the number to start counting from.  Some folks like their
   pages to start at 0 and others like it to start at 1.  This enables
   you to set it as you like.

   Example::

      py["paginate_count_from"] = 1


``paginate_previous_text``

   Defaults to "&lt;&lt;".

   This is the text for the "previous page" link.


``paginate_next_text``

   Defaults to "&gt;&gt;".

   This is the text for the "next page" link.


``paginate_linkstyle``

   Defaults to 1.

   This allows you to change the link style of the paging.

   Style 0::

       [1] 2 3 4 5 6 7 8 9 ... >>

   Style 1::

      Page 1 of 4 >>

   If you want a style different than that, you'll have to copy the
   plugin and implement your own style.


Note about static rendering
===========================

This plugin doesn't work with static rendering.  The problem is that
it relies on the querystring to figure out which page to show and when
you're static rendering, only the first page is rendered.  At some
point, someone will fix this.


License
=======

Plugin is distributed under license: MIT
