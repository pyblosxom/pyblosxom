"""
PyBlosxom does most of its work on "entries".  Each entry is a single
unit of content which has a series of metadata properties (mtime, filename,
id, ...) and also a block of data content.  Entries can come from the
filesystem, SQL, or anywhere else.  They can be generated dynamically
or statically.

The purpose of an Entry object is to encapsulate the metadata and data 
of the entry for later filtering and rendering by the other components 
of Pyblosxom.
"""
