from libs.xmlrpcplugins.__init__ import authenticate


def blogger_getUsersBlogs(request, appkey, username, password):
    """Returns trees below datadir"""
    authenticate(request, username, password)
    from libs import tools
    import re
    py = request.getConfiguration()
    url = py.get('base_url', '')
    result = [{'url':url + '/', 'blogid':'/', 'blogName':'/'}]
    for directory in tools.Walk(py['datadir'], 0, re.compile(r'.*'), 1):
        blogpath = directory.replace(py['datadir'],'') + '/'
        result.append({'url' : url + blogpath, 
                       'blogid' : blogpath, 
                       'blogName':blogpath})
    return result

def blogger_getUserInfo(request, appkey, username, password):
    authenticate(request, username, password)
    # Change these values? Not that important unless some apps needs it.
    py = request.getConfiguration()
    url = py.get('base_url', '')
    return {'firstname':'Ficticious',
            'lastname':'User',
            'userid':'01',
            'email':'someuser@example.com',
            'nickname':'pyblosxom',
            'url':url}

def register_xmlrpc_methods():
    return {'blogger.getUsersBlogs': blogger_getUsersBlogs,
            'blogger.getUserInfo': blogger_getUserInfo}

if __name__ == '__main__':
    from libs.Request import Request
    req = Request()
    req.addConfiguration({'base_url': 'http://roughingit.subtlehints.net/pyblosxom'})
    req.addConfiguration({'datadir': '/home/subtle/blosxom'})
    from pprint import pprint
    pprint(blogger_getUsersBlogs(req, '', '', ''))
    pprint(blogger_getUserInfo(req, '', '', ''))

