# vim: shiftwidth=4 tabstop=4 expandtab
"""
XMLRPC services dispatcher.
"""
import xmlrpclib, sys
from Pyblosxom import plugin_utils

def debug(dbg):
    """
    Just a simple Debugger to see what happens when I screwed up.
    """
    file('xmlrpc.debug','a').write('DEBUG: %s\n' % str(dbg))

class xmlrpcHandler:
    """
    XMLRPC services dispatcher and handler.

    Responsible for handling XMLRPC services request. XMLRPC methods and
    services are available from C{Pyblosxom.xmlrpcplugins}.
    """
    
    def __init__(self, request, data):
        self._request = request
        self._data = data
        
        plugin_utils.initialize_xmlrpc_plugins(request.getConfiguration())

        self._request.addData({'xmlrpc_methods': plugin_utils.methods})

    def process(self):
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
            print 'Content-type: text/plain\n\nXML-RPC call expected\nDebug: %s:%s' % (sys.exc_type, sys.exc_value)
        else:
            print 'Content-type: text/xml\nContent-length: %d\n\n%s\n' % (len(response), response)


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
    A convenient authentication for plugins to use

    @param request: Request object for the current request
    @type request: L{libs.Request.Request} object
    @param username: Username for authentication
    @type username: string
    @param password: Password for authentication
    @type password: string
    @raises xmlrpclib.Fault: This happens when the username password combo is
        wrong
    @warning: The L{libs.Request.Request} must contain a configuration dict
        with C{['xmlrpc']['usernames']} in it. The username is derived from the
        key value pair dict there:

        >>> req = libs.Request.Request()
        >>> req.addConfiguration({'xmlrpc': {'usernames': {'foo': 'bar'}}})
        >>> authenticate(req, 'foo', 'bar')
    """
    auth = request.getConfiguration()['xmlrpc']['usernames']
    if not auth.has_key(username) or password != auth[username]:
        raise xmlrpclib.Fault('PasswordError','Error in username or password')
