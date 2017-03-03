#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2011 Blake Winton
# Copyright (c) 2011 Will Kahn-Greene
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

"""
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
"""

__author__ = "Blake Winton"
__email__ = "willg at bluesock dot org"
__version__ = "2011-12-12"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Lets me use Disqus for comments."
__category__ = "comments"
__license__ = "MIT"
__registrytags__ = "1.5, core"


import os
from Pyblosxom.tools import pwrap_error


def verify_installation(request):
    config = request.get_configuration()

    if 'disqus_shortname' not in config:
        pwrap_error(
            "missing required config property 'disqus_shortname' which"
            "is necessary to determine which disqus site to link to.")
        return False

    return True


def cb_story(args):
    renderer = args['renderer']
    entry = args['entry']
    template = args['template']
    request = args["request"]
    config = request.get_configuration()

    did = os.path.realpath(entry['filename'])
    did = did.replace(entry['datadir'], '')
    did = os.path.splitext(did)[0]
    entry['disqus_id'] = did
    entry['disqus_shortname'] = config.get(
        'disqus_shortname', 'missing disqus_shortname')

    # This uses the same logic as comments.py for determining when
    # to show the comments.
    if (('absolute_path' in entry
         and len(renderer.getContent()) == 1
         and 'comment_form' in renderer.flavour
         and 'nocomments' not in entry)):

        # entry.getId() contains the path.
        output = []
        renderer.output_template(output, entry, 'comment_form')
        args['template'] = template + "".join(output)
    return args
