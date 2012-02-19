========
Comments
========

Summary
=======

Pyblosxom does not come with comments functionality built-in.  There are 
several ways you can add comments functionality to your blog.  This chapter
talks about those.


Disqus
======

Disqus is a comments platform web service that allows you to add comments to
your blog.

Pros:

* it's easy to install
* it handles spam for you
* supports notifications and replies

Cons:

* it's a web service that you have no control over
* it might be difficult to move your comments over to a new system

If this is interesting to you, `sign up for a Disqus account`_.

.. _sign up for a Disqus account: http://disqus.com/


Writing your own comments plugin
================================

Pyblosxom allows for plugins allowing you to write a plugin to add comments
to your website.  This isn't for the feint of heart--there are a lot of bits
to think about.

Pros:

* you're in complete control over how comments work on your site

Cons:

* not for the feint of heart


Comments plugin
===============

Pyblosxom comes with a comments plugin that has a series of features, but
also has some issues and isn't trivial to set up.

Pros:

* it's entirely in your control
* you can extend and modify it to meet your needs
* a lot of Pyblosxom users use it

Cons:

* many people find it difficult to install
* it's missing common comment system features like replies, threads, ...
* you have to implement and maintain your own anti-spam measures
* it hasn't been well maintained in the last couple of years

This comments plugin is documented in the comments chapter of :ref:`part-two`.
