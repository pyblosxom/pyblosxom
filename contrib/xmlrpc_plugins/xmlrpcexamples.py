# vim: tabstop=4 shiftwidth=4 expandtab
"""
XMLRPC service that does math.

Use this as an example of how to implement xmlrpc services.


Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright 2004, 2005 Wari Wahab
"""
__version__ = "$Id$"

def add(request, a, b):
    return a + b

def sub(request, a, b):
    return a - b

def test(request):
    return {'dicttest': "This is a test",
            'requestTest': request.getConfiguration()['blog_title'],
            'list test': [1, 2, 3, 'Go!'],
            'complex list/dict': ['hi', {'test': 'A test',
            'list':['list']}]}

def sureFireFault(request):
    raise IOError, 'This is why you should give up programming'

def cb_xmlrpc_register(args):
    args["methods"].update(
           {'math.add': add,
            'math.sub': sub,
            'system.test': test,
            'system.fault': sureFireFault})

    return args

if __name__ == '__main__':
    from Pyblosxom.Request import Request
    from pprint import pprint
    request = Request()
    request.addConfiguration({'blog_title': 'RoughingIT'})

    pprint(test(request))
    pprint(add(request, 1, 2))
    pprint(sub(request, 1, 2))
    pprint(sureFireFault(request))
