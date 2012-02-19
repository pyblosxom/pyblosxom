
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

=========================================================
 check_javascript - Rejects comments using JavaScript... 
=========================================================

Summary
=======

This plugin filters spam with a dash of JavaScript on the client side.
The JavaScript sets a hidden input field ``secretToken`` in the
comment form to the blog's title.  This plugin checks the
``secretToken`` URL parameter and rejects the comment if it's not set
correctly.

The benefit of JavaScript as an anti-spam technique is that it's very
successful.  It has extremely low false positive and false negative
rates, as compared to conventional techniques like CAPTCHAs, bayesian
filtering, and keyword detection.

Of course, JavaScript has its own drawbacks, primarily that it's not
supported in extremely old browsers, and that users can turn it off.
That's a very small minority of cases, though.  Its effectiveness as
an anti-spam technique usually make that tradeoff worthwhile.


Install
=======

Requires the ``comments`` plugin.

This plugin comes with Pyblosxom.  To install, do the following:

1. Add ``Pyblosxom.plugins.check_javascript`` to the ``load_plugins``
   list in your ``config.py`` file.

2. Configure as documented below.


Configure
=========

1. Make sure you have ``blog_title`` set in your ``config.py``.

2. Add the following bits to your ``comment-form`` template inside
   the ``<form>`` tags::

      <input type="hidden" name="secretToken" id="secretTokenInput"
        value="pleaseDontSpam" />

      <script type="text/javascript">
      // used by check_javascript.py. this is almost entirely backwards
      // compatible, back to 4.x browsers.
      document.getElementById("secretTokenInput").value = "$(blog_title)";
      </script>


License
=======

Plugin is distributed under license: GPLv2
