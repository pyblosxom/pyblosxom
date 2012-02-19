
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

====================================================
 magicword - Magic word method for reducing comm... 
====================================================

Summary
=======

This is about the simplest anti-comment-spam measure you can imagine,
but it's probably effective enough for all but the most popular blogs.
Here's how it works.  You pick a question and put a field on your
comment for for the answer to the question.  If the user answers it
correctly, his comment is accepted.  Otherwise it's rejected.  Here's
how it works:


Install
=======

Requires the ``comments`` plugin.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.magicword`` to the ``load_plugins`` list in
   your ``config.py`` file.

2. Configure as documented below.


Configure
=========

Here's an example of what to put in config.py::

    py['mw_question'] = "What is the first word in this sentence?"
    py['mw_answer'] = "what"

Note that ``mw_answer`` must be lowercase and without leading or
trailing whitespace, even if you expect the user to enter capital
letters.  Their input will be lowercased and stripped before it is
compared to ``mw_answer``.

Here's what you put in your ``comment-form`` file::

    The Magic Word:<br />
    <i>$(mw_question)</i><br />
    <input maxlenth="32" name="magicword" size="50" type="text" /><br />

It's important that the name of the input field is exactly "magicword".


Security note
=============

In order for this to be secure(ish) you need to protect your
``config.py`` file.  This is a good idea anyway!

If your ``config.py`` file is in your web directory, protect it from
being seen by creating or modifying a ``.htaccess`` file in the
directory where ``config.py`` lives with the following contents::

    <Files config.py>
    Order allow,deny
    deny from all
    </Files>

This will prevent people from being able to view ``config.py`` by
browsing to it.


License
=======

Plugin is distributed under license: MIT
