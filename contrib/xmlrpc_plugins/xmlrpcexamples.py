# vim: tabstop=4 shiftwidth=4 expandtab
"""
XMLRPC service that does math.

Use this as an example of how to implement xmlrpc services.
"""

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
