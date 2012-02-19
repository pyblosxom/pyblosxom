
.. only:: text

   This document file was automatically generated.  If you want to edit
   the documentation, DON'T do it here--do it in the docstring of the
   appropriate plugin.  Plugins are located in ``Pyblosxom/plugins/``.

==============================================
 disqus - Lets me use Disqus for comments.... 
==============================================

Summary
=======

Plugin for adding Disqus comments.

It's not hard to do this by hand, but this plugin makes it so that comments
only show up when you're looking at a single blog entry.


Install
=======

This plugin comes with Pyblosxom.  To install, do the following:

1. In your ``config.py`` file, add ``Pyblosxom.plugins.disqus`` to the
   ``load_plugins`` variable.

2. Set ``disqus_shortname`` in your ``config.py`` file.  This comes from
   Disqus when you set up your account.

   For help, see http://docs.disqus.com/help/2/ .

3. Save the ``comment_form`` template into your html flavour.


comment_form template::

    <div id="disqus_thread"></div>
    <script type="text/javascript">
      var disqus_shortname = '$(escape(disqus_shortname))';
      var disqus_identifier = '$(escape(disqus_id))';
      var disqus_title = '$(escape(title))';
  
      /* * * DON'T EDIT BELOW THIS LINE * * */
      (function() {
        var dsq = document.createElement('script');
        dsq.type = 'text/javascript';
        dsq.async = true;
        dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] ||
         document.getElementsByTagName('body')[0]).appendChild(dsq);
      })();
    </script>
    <noscript>Please enable JavaScript to view the
      <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a>
    </noscript>
    <a href="http://disqus.com" class="dsq-brlink"
      >blog comments powered by <span class="logo-disqus">Disqus</span></a>


License
=======

Plugin is distributed under license: MIT
