.. _using-plugins:

=======
Plugins
=======

Pyblosxom allows you to extend and augment its base functionality with
plugins.  Plugins allow you to: to create additional variables; provide
additional entry parsers, renderers, post-formatters, and
pre-formatters; create new output data types; pull information from
other non-blog sources; create images; and a variety of other things.

Plugins hook into Pyblosxom using callbacks which allow plugins to
handle, augment, and otherwise affect Pyblosxom's behavior.


Setting Pyblosxom up to use plugins
===================================

There are two properties in your ``config.py`` file that affect the
behavior for loading plugins: ``plugin_dirs`` and ``load_plugins``.
There's more documentation on these in :ref:`plugin-configuration`.


Finding plugins
===============

As of 1.5, Pyblosxom comes with a core set of plugins.  Documentation
for these plugins is in :ref:`part-two`.

Not all plugins come with Pyblosxom.  You can find more plugins in the
plugin registry on the `website`_.

Additionally, some people write plugins, but never register with the
plugin registry. Sometimes this is because the author doesn't feel the
plugin is finished for public consumption. Even so, it might meet your
needs. The best way to find these plugins is to ask on the
pyblosxom-users mailing list for a plugin that has the functionality
you desire.

.. _website: http://pyblosxom.bluesock.org/


Installing plugins
==================

When you're installing a plugin, refer to its documentation.  The
documentation could be in a ``README`` file, but more commonly it's in
the plugin code itself at the top of the file.  This documentation
should tell you how to install the plugin, what template variables the
plugin exposes, how to invoke the plugin, how to get in touch with the
author should you find bugs or need help, and any additional things
you should know about.

Most plugins should have a pretty easy installation method. You should
be able to copy the plugin into the directory defined in your
``config.py`` file in the ``plugin_dirs`` property.  Then there might
be some additional properties you'll have to set in your ``config.py``
file to define the plugin's behavior.  That should be about it.  On
some occasions, you may have to change the code in the plugin itself
to meet your specific needs.

.. Note::

   A note about Apache, no suexec, .pyc files, and permission
   problems:

   If you're not running suexec, then Apache may not be able to
   generate the ``.pyc`` files for your plugins.  This may result in
   your plugins failing to load.

   If that happens, you should run ``./pyblosxom.cgi`` in your shell
   to generate the ``.pyc`` files.

   Every time you install a new plugin or change an existing plugin,
   you'll need to remove the existing ``.pyc`` files and regenerate
   them.



Writing Your Own plugins
========================

You may find that you desire functionality and there is no plugin that
anyone knows about that performs that functionality.  It's probably
best at this point for you to ask someone to write the plugin you need
or write it yourself.

Pyblosxom plugins are fairly easy to write and can cover a lot of
really different functionality.  The best way to learn how to write
Pyblosxom plugins is to read through the plugins in the plugin
registry.  Many of them are well written and may provide insight as to
how to solve your specific problem.

If you plan on writing your own plugin, check out
:ref:`writing-plugins`.
