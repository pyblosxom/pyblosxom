
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

======================================================
 firstdaydiv - Adds a token which tells us whether... 
======================================================

Summary
=======

Adds a token which allows you to differentiate between the first day
of entries in a series of entries to be displayed from the other days.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. In your ``config.py`` file, add ``Pyblosxom.plugins.firstdaydiv``
   to the ``load_plugins`` list.

2. (optional) Set the ``firstDayDiv`` config variable.  This defaults
   to ``blosxomFirstDayDiv``.

   Example::

      py['firstDayDiv'] = 'blosxomFirstDayDiv'


Usage
=====

This denotes the first day with the css class set in the
``firstDayDiv`` config variable.  This is available in the
``$(dayDivClass)`` template variable.  You probably want to put this
in your ``date_head`` template in a ``<div...>`` tag.

For example, in your ``date_head``, you could have::

   <div class="$dayDivClass">
   <span class="blosxomDate">$date</span>

and in your ``date_foot``, you'd want to close that ``<div>`` off::

   </div>

Feel free to use this in other ways.


License
=======

Plugin is distributed under license: MIT
