"""
check_javascript.py
A PyBlosxom comment spam plugin

This plugin filters spam with a dash of JavaScript on the client side. The
JavaScript sets a hidden input field "secretToken" in the comment form to the
blog's title. This plugin checks the secretToken URL parameter and rejects the
comment if it's not set correctly.

The benefit of JavaScript as an anti-spam technique is that it's very
successful. It has extremely low false positive and false negative rates, as
compared to conventional techniques like CAPTCHAs, bayesian filtering, and
keyword detection.

Of course, JavaScript has its own drawbacks, primarily that it's not supported
in extremely old browsers, and that users can turn it off. That's a very small
minority of cases, though. Its effectiveness as an anti-spam technique usually
make that tradeoff worthwhile.

This is distributed as part of the PyBlosxom contributed plugins pack:
http://sourceforge.net/project/showfiles.php?group_id=67445

Copyright 2006 Ryan Barrett

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
__author__      = "Ryan Barrett <pyblosxom@ryanb.org>"
__version__     = "0.1"
__url__         = "http://pyblosxom.bluesock.org/"
__description__ = "Use JavaScript to filter out spam comments"

from Pyblosxom import tools

def verify_installation(request):
  return 1

def cb_comment_reject(args):
  request = args["request"]
  config = request.getConfiguration()
  http = request.getHttp()
  form = http['form']

  if ('secretToken' in form and
      form['secretToken'].value == config['blog_title']):
    return 0
  else:
    dump = '\n'.join(['%s: %s' % (arg.name, arg.value)
                      for arg in dict(form).values()])
    logger = tools.getLogger()
    logger.info('Comment rejected from %s:\n%s' % (http['REMOTE_ADDR'], dump))
    return 1
