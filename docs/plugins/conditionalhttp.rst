
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

==========================================================
 conditionalhttp - Allows browser-side caching with if... 
==========================================================

Summary
=======

This plugin can help save bandwidth for low bandwidth quota sites.

This is done by outputing cache friendly HTTP header tags like Last-Modified
and ETag. These values are calculated from the first entry returned by
``entry_list``.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. In your ``config.py`` file, add ``Pyblosxom.plugins.conditionalhttp`` to
   the ``load_plugins`` variable.


License
=======

Plugin is distributed under license: MIT
