# vim: shiftwidth=4 tabstop=4 expandtab
import xmlrpclib, sys

def debug(dbg):
    """
    Just a simple Debugger to see what happens when I screwed up.
    """
    file('xmlrpc.debug','a').write('DEBUG: %s\n' % str(dbg))

class xmlrpcHandler:

    def __init__(self, request, data):
        import libs.xmlrpcplugins.__init__
        self._request = request
        self._data = data
        
        xmlrpc = libs.xmlrpcplugins.__init__
        xmlrpc.initialize_plugins()

        self._request.addData({'xmlrpc_methods': xmlrpc})

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
        methods = self._request.getData()['xmlrpc_methods'].methods
        func_obj = methods.get(meth_name, None)
        if callable(func_obj):
            return apply(func_obj, args)
        else:
            raise xmlrpclib.Fault('Method Error', 'Method Does not Exist')
