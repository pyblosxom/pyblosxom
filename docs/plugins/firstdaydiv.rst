=====================
 Plugin: firstdaydiv 
=====================

Summary
=======

Adds a token which allows you to differentiate between the first day
of entries in a series of entries to be displayed from the other days.


Install
=======

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