"""
This plugin acts as an XMLRPC services dispatcher.  In order to use 
any xmlrpc plugins, you must first have this plugin installed.

Requires the following block in your config.py file:

%<---------------------------------------------------------
# XML-RPC data
xmlrpc = {}

# Username to access this server
xmlrpc['usernames'] = {'username': 'password'}
xmlrpc['urltrigger'] = "/RPC"
xmlrpc['maxrequest_length'] = 10000
xmlrpc['load_xmlrpc_plugins'] = ["xmlrpc_blogger"]
%<---------------------------------------------------------

'usernames'  - a dict of username -> password key/value pairs.
'urltrigger' - the pathinfo trigger that causes the xmlrpc plugin
               to handle the request.
'maxrequest_length' - the maximum content length of a post.  this is
               partially to protect your blog from bad people.
'load_xmlrpc_plugins' - the list of plugins that are xmlrpc plugins
               and implement xmlrpc methods.  these are stored in
               the same directory as your other plugins.
"""

__author__ = "Wari"
__version__ = "$id$"
__description__ = "XMLRPC services dispatcher"

import xmlrpclib, sys, os
from Pyblosxom import plugin_utils, tools

class XMLRPCHandler:
    """
    XMLRPC services dispatcher and handler.

    Responsible for handling XMLRPC services request. XMLRPC methods and
    services are available from C{Pyblosxom.xmlrpcplugins}.
    """
    def __init__(self, request, data):
        self._request = request
        self._data = data
        
    def process(self):
        """
        Processes the xmlrpc request.
        """
        # XML-RPC starts here
        try:
            # Get parameters
            params, method = xmlrpclib.loads(self._data)
            params = list(params)
            params.insert(0, self._request)
            params = tuple(params)

            try:
                # Call the method
                response = self.xmlrpcCall(method, params)
                if type(response) != type (()):
                    response = (response,)
            except xmlrpclib.Fault, faultobj:
                # Throw an xmlrpc exception
                response = xmlrpclib.dumps(faultobj)
            except:
                # Format other exceptions into xmlrpc faults
                response = xmlrpclib.dumps(xmlrpclib.Fault(1, '%s:%s' %
                        (sys.exc_type, sys.exc_value)))
            else:
                # Passed.
                response = xmlrpclib.dumps(response, methodresponse=1)

        except:
            resp_str = 'Content-Type: text/plain\n\n' + \
                       'XML-RPC call expected\n' + \
                       'Debug: %s:%s\n' % (str(sys.exc_type), str(sys.exc_value)) + \
                       "'" + self._data + "'"
        else:
            resp_str = 'Content-Type: text/xml\n' + \
                       'Content-Length: %d\n\n' % len(response) + \
                       response

        sys.stdout.write(resp_str)
        sys.stdout.flush()


    def xmlrpcCall(self, meth_name, args):
        """XML-RPC dispatcher"""
        methods = self._request.getData()['xmlrpc_methods']
        func_obj = methods.get(meth_name, None)
        if callable(func_obj):
            return apply(func_obj, args)
        else:
            raise xmlrpclib.Fault('Method Error', 'Method Does not Exist')


def authenticate(request, username, password):
    """
    Takes a Request object, a username, and a password and authenticates
    the credentials against our configured user list.

    @param request: Request object for the current request
    @type request: L{Pyblosxom.Request.Request} object

    @param username: Username for authentication
    @type username: string

    @param password: Password for authentication
    @type password: string

    @raises xmlrpclib.Fault: This happens when the username password combo is
        wrong
    @warning: The L{Pyblosxom.Request.Request} must contain a configuration dict
        with C{['xmlrpc']['usernames']} in it. The username is derived from the
        key value pair dict there:

        >>> req = Pyblosxom.Request.Request()
        >>> req.addConfiguration({'xmlrpc': {'usernames': {'foo': 'bar'}}})
        >>> authenticate(req, 'foo', 'bar')
    """
    config = request.getConfiguration()
    xmlconfig = config["xmlrpc"]
    auth = xmlconfig['usernames']

    if not auth.has_key(username) or password != auth[username]:
        raise xmlrpclib.Fault('PasswordError', 'Error in username or password')


def cb_handle(args):
    """
    This takes in a request and handles the request.
    """
    request = args["request"]
    pyhttp = request.getHttp()
    config = request.getConfiguration()
    xmlconfig = config.get("xmlrpc", {})

    urltrigger = xmlconfig.get("urltrigger", "/RPC")

    if os.environ.get("PATH_INFO", "").startswith(urltrigger):
        try:
            content_length = int(os.environ.get("CONTENT_LENGTH", "0"))
            maxrequest_length = xmlconfig.get("maxrequest_length", 10000)

            if content_length > maxrequest_length:
                raise ValueError, 'Request too large - %s bytes' % content_length

        except: 
            response = xmlrpclib.dumps(xmlrpclib.Fault(1, "%s: %s" % sys.exc_info()[:2]))
            resp_str = ('Content-Type: text/xml\n') + \
                       ('Content-Length: %d\n\n' % len(response)) + \
                       response

            sys.stdout.write(resp_str)
            sys.stdout.flush()
            return 1

        # everything is cool--so we handle the xmlrpc request

        data = sys.stdin.read(content_length)
        request.addConfiguration( {"xmlrpc": xmlconfig} )

        # load the xmlrpc plugins
        xmlrpc_plugins = xmlconfig.get("load_xmlrpc_plugins", [])
        plugin_utils.initialize_plugins([], xmlrpc_plugins)

        # here we call the xmlrpc_init callback passing in a dict.
        # each function that registers with this callback adds their
        # xmlrpc functions to the dict.
        args = tools.run_callback("xmlrpc_register", 
                        {"request": request, "methods": {}},
                        mappingfunc=lambda x,y:y,
                        defaultfunc=lambda x:x)
        methods = args["methods"]
        request.addData({'xmlrpc_methods': methods})

        """
        if os.environ.get("REQUEST_METHOD", "") == "GET":
            resp = []
            resp.append("Content-Type: text/plain")
            resp.append("\n")
            resp.append("-" * 40)
            resp.append("Methods Defined:")
            resp.append("-" * 40)
            for mem in methods.keys():
                resp.append("  %s -> %s" % (mem, methods[mem]))
            sys.stdout.write("\n".join(resp))
            return 1
        """

        x = XMLRPCHandler(request, data).process()

        # return 1 indicating we've handled the request
        return 1

# vim: shiftwidth=4 tabstop=4 expandtab
