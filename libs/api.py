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

	def register(self, func, place=LAST):
		"""
		Registers a function with the callback chain.  All functions
		should take one argument.  This argument's contents will depend
		on the callback chain involved.
		"""
		if place == FIRST:
			self._chain.insert(0, func)
		else:
			self._chain.append(func)

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
		"""
		for mem in self._chain:
			if mem(data) == HANDLED:
				break
		return

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
		"""
		for mem in self._chain:
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

