=========
Renderers
=========

.. _renderers:

Summary
=======

PyBlosxom supports multiple renderers and comes with two by default:
debug and blosxom.


blosxom
=======

You can set which renderer to use in your ``config.py`` file like
this::

    py["renderer"] = "blosxom"

.. Note::

    If you don't specify the ``renderer`` configuration variable, 
    PyBlosxom uses the blosxom renderer.

The blosxom renderer is named as such because it operates similarly to
blosxom.  Read the chapter on :ref:`flavours and templates
<flavours-and-templates>`.


debug
=====

The debug renderer outputs your blog in a form that makes it easy to 
see the data generated when handling a PyBlosxom request.  This is 
useful for debugging plugins, working on blosxom flavours and
templates, and probably other things as well.

To set PyBlosxom to use the debug renderer, do this in your
``config.py`` file::

    py["renderer"] = "debug"


Other renderers
===============

If you want your blog rendered by a different renderer, say one that
uses a different template system like Jinja or Cheetah, then you will
need to install a plugin that implements the ``renderer`` callback.