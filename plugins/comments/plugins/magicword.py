"""
Magic Word Plugin.

Requires: The "comments" plugin.

This is about the simplest anti-comment-spam measure you can imagine, but it's
probably effective enough for all but the most popular blogs.  Here's how it 
works.  You pick a question and put a field on your comment for for the answer 
to the question.  If the user answers it correctly, his comment is accepted.  
Otherwise it's rejected.  Here's how it works:

Here's an example of what to put in config.py:
    py['mw_question'] = "What is the first word in this sentence?"
    py['mw_answer'] = "what"

Note that mw_answer must be lowercase and without leading or trailing 
whitespace, even if you expect the user to enter capital letters.  Their input
will be lowercased and stripped before it is compared to mw_answer.

Here's what you put in your comment-form.html file:
    The Magic Word:<br />
    <i>$mw_question</i><br />
    <input maxlenth="32" name="magicword" size="50" type="text" /><br />

It's important that the name of the input field is exactly "magicword".

SECURITY NOTE:

In order for this to be secure(ish) you need to protect your config.py file.
This is a good idea anyway!  To protect config.py, create or modify a
.htaccess file in the directory where config.py lives with the following
contents:
    <Files config.py>
    Order allow,deny
    deny from all
    </Files>

This will prevent people from being able to view config.py by browsing to it.
"""

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# Copyright 2005 Nathaniel Gray  <n8gray /at/ caltech /dot/ edu>

__author__ = "Nathaniel Gray"
__version__ = "0.1"

def verify_installation(request):
    config = request.getConfiguration()
    
    status = 1
    if not config.has_key('mw_question'):
        print("Missing required property: mw_question")
        status = 0
    if not config.has_key('mw_answer'):
        print("Missing required property: mw_answer")
        return 0
    a = config["mw_answer"]
    if a != a.strip().lower():
        print("Error: mw_answer must be lowercase, without leading or trailing whitespace")
        return 0
    
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
    form = request.getForm()
    data = request.getData()
    config = request.getConfiguration()
    
    try:
        mw = form["magicword"].value.strip().lower()
        if mw == config["mw_answer"]:
            return False
    except KeyError:
        pass
    return True
