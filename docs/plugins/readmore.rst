
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

===================================================
 readmore - Breaks blog entries into summary an... 
===================================================

Summary
=======

Allows you to break a long entry into a summary and the rest making it
easier to show just the summary in indexes.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.readmore`` to the ``load_plugins`` list in
   your ``config.py`` file.

   .. Note::

      If you're using the rst_parser plugin, make sure this plugin
      shows up in load_plugins list before the rst_parser plugin.

      See the rst_parser section below.

2. Configure as documented below.


Configuration
=============

``readmore_breakpoint``

   (optional) string; defaults to "BREAK"

   This is the text that you'll use in your blog entry that breaks the
   body into the summary part above and the rest of the blog entry
   below.

   For example::

      py["readmore_breakpoint"] = "BREAK"

``readmore_template``

   (optional) string; defaults to::

       '<p class="readmore"><a href="%(url)s">read more after the break...</a></p>'

   When the entry is being shown in an index with other entries, then
   the ``readmore_breakpoint`` text is replaced with this text.  This
   text is done with HTML markup.

   Variables available:

   * ``%(url)s``       - the full path to the story
   * ``%(base_url)s``  - base_url
   * ``%(flavour)s``   - the flavour selected now
   * ``%(file_path)s`` - path to the story (without extension)

   .. Note::

      This template is formatted using Python string formatting---not
      Pyblosxom template formatting!


Usage
=====

For example, if the value of ``readmore_breakpoint`` is ``"BREAK"``,
then you could have a blog entry like this::

    First post
    <p>
      This is my first post.  In this post, I set out to explain why
      it is that I'm blogging and what I hope to accomplish with this
      blog.  See more below the break.
    </p>
    BREAK
    <p>
      Ha ha!  Made you look below the break!
    </p>


Usage with rst_parser
=====================

Since the rst_parser parses the restructured text and turns it into
HTML and this plugin operates on HTML in the story callback, we have
to do a two-step replacement.

Thus, instead of using BREAK or whatever you have set in
``readmore_breakpoint`` in your blog entry, you use the break
directive::

    First post

    This is my first post.  In this post, I set out to explain why
    it is that I'm blogging and what I hope to accomplish with this
    blog.

    .. break::

    Ha ha!  Made you look below the break!


History
=======

This is based on the original readmore plugin written by IWS years
ago.  It's since been reworked.

Additionally, I folded in the rst_break plugin break directive from
Menno Smits at http://freshfoo.com/wiki/CodeIndex .


License
=======

Plugin is distributed under license: MIT
