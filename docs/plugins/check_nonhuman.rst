
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

=================================================
 check_nonhuman - Rejects non-human comments.... 
=================================================

Summary
=======

This works in conjunction with the comments plugin and allows you to
significantly reduce comment spam by adding a "I am human" checkbox to
your form.  Any comments that aren't "from a human" get rejected
immediately.

This shouldn't be the only way you reduce comment spam.  It's probably
not useful to everyone, but would be useful to some people as a quick
way of catching some of the comment spam they're getting.

Usually this works for a while, then spam starts coming in again.  At
that point, I change the ``nonhuman_name`` config.py variable value
and I stop getting comment spam.


Install
=======

Requires the ``comments`` plugin.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.check_nonhuman`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Configure as documented below.


Usage
=====

For setup, copy the plugin to your plugins directory and add it to
your load_plugins list in your config.py file.

Then add the following item to your config.py (this defaults to
"iamhuman")::

   py["nonhuman_name"] = "iamhuman"


Then add the following to your comment-form template just above the
submit button (make sure to match the input name to your configured
input name)::

   <input type="checkbox" name="iamhuman" value="yes">
   Yes, I am human!


Alternatively, if you set the ``nonhuman_name`` property, then you should
do this::

   <input type="checkbox" name="$(nonhuman_name)" value="yes">
   Yes, I am human!


Additionally, the nonhuman plugin can log when it rejected a comment.
This is good for statistical purposes.  1 if "yes, I want to log" and
0 (default) if "no, i don't want to log".  Example::

   py["nonhuman_log"] = 1


And that's it!

The idea came from::

   http://www.davidpashley.com/cgi/pyblosxom.cgi/2006/04/28#blog-spam


License
=======

Plugin is distributed under license: MIT
