# vim: shiftwidth=4 tabstop=4 expandtab
"""
XMLRPC plugin initializer and simple authentication handler

@var methods: This contains function references of XMLRPC api calls. This
    will populate after a call to C{initialize_plugins()}
@type methods: dict
"""
import os, glob, xmlrpclib

methods = {}

def initialize_plugins():
    """
    Imports and initializes plugins from this directory so they can register
    with the xmlrpc method callbacks.

    Plugins in this directory must have the C{register_xmlrpc_methods} in the
    plugin module. It must return a dict containing the XMLRPC method name as
    the key, and a function reference as its value. For example:

        def helloWorld(request, name):
            return "Hello %s" % name

        def test(request):
            return "Test Passed"

        def register_xmlrpc_methods():
            return {'system.testing': test,
                    'system.helloWorld': helloWorld}
    """
    index = __file__.rfind(os.sep)
    if index == -1:
        path = "." + os.sep
    else:
        path = __file__[:index]

    _module_list = glob.glob( os.path.join(path, "*.py"))

    for mem in _module_list:
        mem2 = mem[mem.rfind(os.sep)+1:mem.rfind(".")]

        # we skip modules whose names start with an _ .  this allows people to
        # test stuff without having to move it in and out of a directory.
        if mem2[0] == "_":
            continue

        name = "libs.xmlrpcplugins." + mem2
        _module = __import__(name)
        for comp in name.split(".")[1:]:
            _module = getattr(_module, comp)

        # if the module has a register_xmlrpc_methods function, we call it with
        # our py dict so it can bind itself to variable names of its own accord
        if _module.__dict__.has_key("register_xmlrpc_methods"):
            api = _module.register_xmlrpc_methods()

        methods.update(api)

def authenticate(request, username, password):
    """
    A convenient authentication for plugins to use

    @param request: Request object for the current request
    @param username: Username for authentication
    @param password: Password for authentication
    @type request: C{libs.Request} object
    @type username: string
    @type password: string
    @raise xmlrpclib.Fault: This happens when the username password combo is wrong
    @warning: The C{libs.Request} must contain a configuration dict with
        C{['xmlrpc']['usernames']} in it. The username is devired from the key
        value pair dict there:

        >>> req = libs.Request()
        >>> req.addConfiguration({'xmlrpc': {'usernames': {'foo': 'bar'}}})
        >>> authenticate(req, 'foo', 'bar')
                    
    """
    auth = request.getConfiguration()['xmlrpc']['usernames']
    if not auth.has_key(username) or password != auth[username]:
        raise xmlrpclib.Fault('PasswordError','Error in username or password')
