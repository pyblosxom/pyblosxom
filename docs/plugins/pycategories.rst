
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

================================================
 pycategories - Builds a list of categories.... 
================================================

Summary
=======

Walks through your blog root figuring out all the categories you have
and how many entries are in each category.  It generates html with
this information and stores it in the ``$(categorylinks)`` variable
which you can use in your head or foot templates.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.pycategories`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Add ``$(categorylinks)`` to your head and/or foot templates.


Configuration
=============

You can format the output by setting ``category_begin``,
``category_item``, and ``category_end`` properties.

Categories exist in a hierarchy.  ``category_start`` starts the
category listing and is only used at the very beginning.  The
``category_begin`` property begins a new category group and the
``category_end`` property ends that category group.  The
``category_item`` property is the template for each category item.
Then after all the categories are printed, ``category_finish`` ends
the category listing.

For example, the following properties will use ``<ul>`` to open a
category, ``</ul>`` to close a category and ``<li>`` for each item::

    py["category_start"] = "<ul>"
    py["category_begin"] = "<li><ul>"
    py["category_item"] = (
        r'<li><a href="%(base_url)s/%(category_urlencoded)sindex">'
        r'%(category)s</a></li>')
    py["category_end"] = "</li></ul>"
    py["category_finish"] = "</ul>"


Another example, the following properties don't have a begin or an end
but instead use indentation for links and displays the number of
entries in that category::

    py["category_start"] = ""
    py["category_begin"] = ""
    py["category_item"] = (
        r'%(indent)s<a href="%(base_url)s/%(category_urlencoded)sindex">'
        r'%(category)s</a> (%(count)d)<br />')
    py["category_end"] = ""
    py["category_finish"] = ""

There are no variables available in the ``category_begin`` or
``category_end`` templates.

Available variables in the category_item template:

=======================  ==========================  ====================
variable                 example                     datatype
=======================  ==========================  ====================
base_url                 http://joe.com/blog/        string
fullcategory_urlencoded  'dev/pyblosxom/status/'     string
fullcategory             'dev/pyblosxom/status/'     string (urlencoded)
category                 'status/'                   string
category_urlencoded      'status/'                   string (urlencoed)
flavour                  'html'                      string
count                    70                          int
indent                   '&nbsp;&nbsp;&nbsp;&nbsp;'  string
=======================  ==========================  ====================


License
=======

Plugin is distributed under license: MIT
