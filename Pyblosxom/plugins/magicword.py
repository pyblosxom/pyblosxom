#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (c) 2005 Nathaniel Gray
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################


"""
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

"""

__author__ = "Nathaniel Gray"
__email__ = "n8gray /at/ caltech /dot/ edu"
__version__ = "2011-10-28"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Magic word method for reducing comment spam"
__category__ = "comments"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


from Pyblosxom.tools import pwrap_error


def verify_installation(request):
    config = request.get_configuration()

    status = True
    if not 'mw_question' in config:
        pwrap_error("Missing required property: mw_question")
        status = False

    if not 'mw_answer' in config:
        pwrap_error("Missing required property: mw_answer")
        return False

    a = config["mw_answer"]
    if a != a.strip().lower():
        pwrap_error("mw_answer must be lowercase, without leading "
                    "or trailing whitespace")
        return False

    return status


def cb_comment_reject(args):
    """
    Verifies that the commenter answered with the correct magic word.

    @param args: a dict containing: pyblosxom request, comment dict
    @type config: C{dict}
    @return: True if the comment should be rejected, False otherwise
    @rtype: C{bool}
    """
    request = args['request']
    form = request.get_form()
    config = request.get_configuration()

    try:
        mw = form["magicword"].value.strip().lower()
        if mw == config["mw_answer"]:
            return False
    except KeyError:
        pass
    return True
