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

		Each function tries to see if it can handle the data.  If it
		can't, then it returns None.  If it can, then it handles the
		data (possibly by converting it into something else) and then
		returns that data at which point the CallbackChain ceases and
		we return the result.
		"""
		for mem in self._chain:
			data = mem(data)
			if data != None:
				return data
		return

	def executeChain(self, data):
		"""
		Executes a callback chain on a given piece of data.  This
		data could be a string or an object.  Consult the documentation
		for the specific callback chain you're executing.

		Changed data is returned by each function in the chain until
		the last function returns data--then that data is returned
		to the executor.
		"""
		for mem in self._chain:
			data = mem(data)
			if data == None:
				return
		return data

import os
# CallbackChain to generate a os.stat tuple about a given file.
# call filestat.executeChain(filename) and get back a os.stat like
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

