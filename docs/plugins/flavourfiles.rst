
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

=======================================================
 flavourfiles - Serves static files related to flav... 
=======================================================

Summary
=======

This plugin allows flavour templates to use file urls that will
resolve to files in the flavour directory.  Those files will then get
served by PyBlosxom.

This solves the problem that flavour packs are currently difficult to
package, install, and maintain because static files (images, css, js,
...) have to get put somewhere else and served by the web server and
this is difficult to walk a user through.

It handles urls that start with ``flavourfiles/``, then the flavour
name, then the path to the file.

For example::

    http://example.com/blog/flavourfiles/html/style.css


.. Note::

   This plugin is very beta!  It's missing important functionality,
   probably has bugs, and hasn't been well tested!


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.flavourfiles`` to the ``load_plugins`` list
   of your ``config.py`` file.

2. In templates you want to use flavourfiles, use urls like this::

       $(base_url)/flavourfiles/$(flavour)/path-to-file

   For example::

       <img src="$(base_url)/flavourfiles/$(flavour)/header_image.jpg">

The ``$(base_url)`` will get filled in with the correct url root.

The ``$(flavour)`` will get filled in with the name of the url.  This
allows users to change the flavour name without having to update all
the templates.


License
=======

Plugin is distributed under license: MIT License
