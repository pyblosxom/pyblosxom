# vim: tabstop=4 shiftwidth=4
import os, glob

ext = {}

def initialize_extensions():
	"""
	Imports and initializes extensions from this directory so they can register
	with Walk
	"""
	index = __file__.rfind(os.sep)
	if index == -1:
		path = "." + os.sep
	else:
		path = __file__[:index]

	_module_list = glob.glob( os.path.join(path, "*.py"))

	for mem in _module_list:
		mem2 = mem[mem.rfind(os.sep)+1:mem.rfind(".")]

		# we skip modules whose names start with an _ .  this
		# allows people to test stuff without having to move
		# it in and out of a directory.
		if mem2[0] == "_":
			continue

		try:
			name = "libs.entryparsers." + mem2
			_module = __import__(name)
			for comp in name.split(".")[1:]:
				_module = getattr(_module, comp)

			ext[mem2] = _module

		except Exception, e:
			# FIXME - we kicked up an exception--where to we spit 
			# it out to?
			print e

if __name__ == '__main__':
	initialize_extensions()
	from pprint import pprint
	pprint(ext)
