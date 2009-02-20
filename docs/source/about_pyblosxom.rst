=================
What is PyBlosxom
=================

PyBlosxom is a lightweight weblog system.  It was originally a Python
clone of `Blosxom`_ but has since evolved into a weblog system of its own
reminiscent of `Blosxom`_.  PyBlosxom focuses on three things:

.. _Blosxom: http://www.blosxom.com/

**simplicity**
  PyBlosxom uses the file system for all its data storage.  Because 
  of this you can use whatever editor you want to use to create, update,
  and manipulate entries.

**extensibility**
  PyBlosxom has plugin framework allowing you to build plugins in 
  Python to augment and change PyBlosxom's default behavior.

**community**
  There are several hundred PyBlosxom users out there all of whom 
  have different needs.  PyBlosxom is used on a variety of operating
  systems in a variety of environments.

PyBlosxom is a pretty straight-forward system that allows you to do
the things you need to do without building everything from scratch.


Who shouldn't use PyBlosxom
===========================

PyBlosxom is a small project.  As such, we have no customer support
hotline, our documentation will be eternally half-done, and it's
likely you will run into problems eventually.  PyBlosxom offers
mailing lists through SourceForge for support, we do have some
documentation, and you're encouraged to read the code.

PyBlosxom is a CGI program at its heart.  While there have been
changes to make it work with WSGI and mod_python and other
web-servers, it's still architected as a CGI program.  Using it in
other ways may cause headaches.

PyBlosxom by default uses the file-system to store entries where each
entry is a separate file with the mtime of the file acting as the time
stamp.  Files are stored in a directory hierarchy which matches the
category structure of your blog.  As such, each entry ends up in a
single category.

We recognize that PyBlosxom will never be all things to all people and
thus PyBlosxom has a framework for building plugins that are written
in Python which allow you to augment and override the default
behavior.  There are many plugins out there already, but it's likely
that you will have needs that aren't met adequately.  If you don't
have any interest in tinkering with plugins, then it's possible
PyBlosxom is not for you.

If this program doesn't sound like something that will meet your needs
or if this sounds like it's going to be really frustrating, we don't
think you should use PyBlosxom.  There are many other weblog systems
out there which meet a wide variety of needs--there's no need to try
to shoe-horn PyBlosxom into your requirements and get frustrated in
the process.

However, if this invigorates you, join the mailing lists and we'll
work together to make PyBlosxom better for all of us.


Basic Overview of PyBlosxom
===========================

PyBlosxom is a file-based weblog system.  Entries are stored in
text files (one file per entry) in a directory corresponding to the
category for the entry.  The directory tree of your entries and
categories is called a *datadir*.  For more about this see 
``install`` and ``writing_entries``.

The look and feel of your blog is determined by flavours.  A
flavour is a group of templates.  Examples of flavours include:

* RSS
* RSS 2.0
* Atom 1.0
* HTML
* XHTML

For more information about flavours, see ``flavours_and_templates``.
The PyBlosxom web-site maintains flavours submitted by people like you
at http://pyblosxom.sourceforge.net/registry/flavours/ .

PyBlosxom behavior can be adjusted by using PyBlosxom plugins.  Plugins
are written in Python and use the PyBlosxom callback system to override
or adjust PyBlosxom behavior.  For more information on plugins, see
``plugins``, ``writing_plugins``, and ``dev_architecture``.  The PyBlosxom 
web-site maintains plugins submitted by people like you at 
http://pyblosxom.sourceforge.net/registry/ .  

Additionally, there's a contributed plugins pack that contains many 
often-used plugins that are maintained by the PyBlosxom developers.  You
can download the contributed plugins pack from our `web-site`_.

.. web-site: http://pyblosxom.sourceforge.net/


Where to go for help
====================

PyBlosxom comes with documentation in the ``docs`` directory.  This
should be the first place you should go to for help.

On the PyBlosxom project `web-site`_, you can find up-to-date documentation, 
manuals, project status and mailing list information.

.. _web-site: http://pyblosxom.sourceforge.net/

The pyblosxom-users mailing list is the place to go if you're having
difficulties.  Discussions from the mailing list affect the content of
this manual.  Mailing list information can be found on our `Contact Us`_ 
page.

.. _Contact Us: http://pyblosxom.sourceforge.net/blog/static/contact
