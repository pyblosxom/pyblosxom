# vim: tabstop=4 shiftwidth=4
"""
This module holds a series of connectors that plugins can replace
(in the case of callbacks) or add themselves to (in the case of
callback chains and callback handlers).

Callbacks allow us to override pyblosxom behavior by adding in a 
plugin module.

Callback chains allow us to add onto pyblosxom behavior and the
behavior of other plugin modules where each link in the chain
takes a given input, modifies it, and then passes it to the
next link in the chain as input.

Because pyblosxom is a CGI process, these mechanisms are designed 
to reduce the build cost as well as the run-time cost required.

This module defines a series of callbacks and callbackchains and
what they're used for.
"""

FIRST = 0
MIDDLE = 50
LAST = 99

HANDLED = 1

class CallbackChain:
    """
    This is a callback chain.  It allows a series of functions to
    register for a specific kind of event.

    Callback chains can be used in different ways.  One way is
    to notify all the registered functions about an event.  Data
    returned by each function is not preserved in this case.

    Another way is to have each function take a piece of data and
    modify it and return that data.

    Another way is to handle a piece of data.
    """
    def __init__(self, firstfunc=None):
        self._chain = []
        if firstfunc:
            self._chain.append(firstfunc)

    def register(self, func, place=MIDDLE):
        """
        Registers a function with the callback chain.  All functions
        should take one argument.  This argument's contents will depend
        on the callback chain involved.

        @param func: the function to be called which takes in the argument
            tuple specified by the callback chain in question
        @type  func: callable

        @param place: the priority for the function to kick off.  0 is the
            lowest, 99 is the highest, and we default to 50 if you don't
            care
        @type  place: int
        """
        self._chain.append((place, func))

    def __getchain__(self):
        """
        Returns a list of the functions in order of priority.
        """
        self._chain.sort(lambda x,y: cmp(x[0], y[0]))
        chain = [mem[1] for mem in self._chain]
        return chain

    def executeHandler(self, data):
        """
        Executes a callback chain passing a dict with a series of name/value
        pairs in it to the registered functions.  Consult the documentation
        for the specific callback chain you're executing.

        Each function tries to see if it can handle the data being
        passed in as input.  If it can handle the data, then it does
        so and returns api.HANDLED.  We continue through the list of 
        registered functions until we hit the end (none of them 
        handled it) or one of the functions has handled the data 
        and we don't need to proceed further.

        This is will stop when one function returns something other
        than None.  It is not guaranteed that every link in the chain
        will be called.

        @param data: data is a dict filled with name/value pairs--refer
            to the callback chain documentation for what's in the data 
            dict.
        @type  data: dict

        @return: returns whatever is returned by the handler or None
            if nothing handled the thing
        @rtype: varies
        """
        chain = self.__getchain__()
        ret = None
        for mem in chain:
            ret = mem(data)
            if ret != None:
                break
                
        return ret

    def executeListHandler(self, data):
        """
        Executes a callback chain on a given piece of data.  The data
        passed in is a dict of name/value pairs.  Consult the documentation
        for the specific callback chain you're executing.

        Each function tries to see if it can handle the data being
        passed in as input.  If it can handle the data, then it does
        so and returns a list of things, otherwise it returns None.
        We continue through the list of registered functions until
        we hit the end (none of them handled it) or one of the
        functions has handled the data and we don't need to proceed further.

        @param data: data is a dict filled with name/value pairs--refer
            to the callback chain documentation for what's in the data 
            dict.
        @type  data: dict

        @returns: a list of data or an empty list
        @rtype: list
        """
        chain = self.__getchain__()
        for mem in chain:
            result = mem(data)
            if result != None:
                break
        if result == None:
            return []
        return result
            
    def executeTransform(self, data):
        """
        Executes a callback chain on a given piece of data.  This
        passed in is a dict of name/value pairs.  Consult the documentation
        for the specific callback chain you're executing.

        Each function of the chain takes the input, applies some
        transformation to it, and then returns the newly changed
        input as output.  This output is then passed to the next function
        in the chain as input and we proceed until all registered
        functions have had a chance to operate on the data.  We then
        return the data to the caller.

        This is guaranteed to be adjusted by every link in the chain.

        @param data: data is a dict filled with name/value pairs--refer
            to the callback chain documentation for what's in the data 
            dict.
        @type  data: dict

        @returns: the transformed dict
        @rtype: dict
        """
        chain = self.__getchain__()
        for mem in chain:
            data = mem(data)

        return data

import os

# CallbackChain to generate a os.stat tuple about a given file.
# call filestat.executeTransform(filename) and get back a os.stat like
# tuple with all the pieces worked out.
#
# Data dict:
#    "filename": filename (string)
#    "mtime": tuple (from os.stat)
# 
filestat = CallbackChain()

# CallbackChain to do a final logging based on a log plugin
#
# Data dict:
#    "filename": filename to log to (string)
#    "return_code": error code to log (string)
#
logRequest = CallbackChain()


# CallbackChain to generate file list based on a plugin
#  
# Data dict:
#   "request": the request object
#
# Output:
#   the list of entries
fileListHandler = CallbackChain()

# CallbackChain to notify all the plugins of the completed
# request and the entry list.  This allows plugins to 
# modify the entry list and add variables to the runtime
# data dict prior to rendering.
#
# Data dict:
#   "request": Request
#
prepareChain = CallbackChain()
