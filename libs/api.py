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
        Executes a callback chain on a given piece of data.  This
        data could be a string or an object.  Consult the documentation
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

        @param data: data is a tuple--refer to the callback chain 
            documentation for what it might hold
        @type  data: tuple of stuff

        @return: returns whatever is returned by the handler or None
            if nothing handled the thing
        @rtype: varies
        """
        chain = self.__getchain__()
        ret = None
        for mem in chain:
            ret = mem(data)
            if ret:
                break
                
        return ret

    def executeListHandler(self, data):
        """
        Executes a callback chain on a given piece of data.  This
        data could be a string or an object.  Consult the documentation
        for the specific callback chain you're executing.

        Each function tries to see if it can handle the data being
        passed in as input.  If it can handle the data, then it does
        so and returns a list of data, otherwise it returns None.
        We continue through the list of registered functions until
        we hit the end (none of them handled it) or one of the
        functions has handled the data and we don't need to proceed further.
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
        data could be a string or an object.  Consult the documentation
        for the specific callback chain you're executing.

        Each function of the chain takes the input, applies some
        transformation to it, and then returns the newly changed
        input as output.  This output is then passed to the next function
        in the chain as input and we proceed until all registered
        functions have had a chance to operate on the data.  We then
        return the data to the caller.

        This is guaranteed to be adjusted by every link in the chain.

        @param data: data is a tuple--refer to the callback chain 
            documentation for what it might hold
        @type  data: tuple of stuff

        @returns: the transformed tuple
        @rtype: varies
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
# Input:
#    filename (string)
#    tuple (from os.stat)
#
# Output:
#    filename
#    adjusted tuple
filestat = CallbackChain()

# CallbackChain to parse a given story item (head, foot, or story)
# and expand variables.
#
# Input:
#    entry_dict (dict)
#    text_string (string) - the story item
#
# Output:
#    entry_dict (dict)
#    adjusted text_string (string)
parseitem = CallbackChain()

# CallbackChain to do a final logging based on a log plugin
#
# Input:
#    filename (string) - Filename to log to
#    returnCode (string) - Error code to log
#
# Output: None
logRequest = CallbackChain()


# CallbackChain to generate file list based on a plugin
#  
# Input:
#   entry dict 
#
# Output:
#   list of files
fileListHandler = CallbackChain()

# CallbackChain to notify all the plugins of the completed
# request and the entry list.  This allows plugins to 
# modify the entry list and add variables to the runtime
# data dict prior to rendering.
#
# Input: 
#   Request
#
# Output:
#   none
prepareChain = CallbackChain()
