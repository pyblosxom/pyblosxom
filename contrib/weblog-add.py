#!/usr/bin/env python
#
# weblog-add
# add a .txt file into a webtree suitable for pyblosxom/blosxom processing
# (the first in a series of web-administration tools for pyblosxom/blosxom)
# 
# Be sure to change blog_root and user2Link()
#
# Warning, this script expects that it will be invoked by (mostly) trusted
# users of your website.  Although I have written some basic security checks
# covering the writing of files, the script is vulnerable to numerous cross
# site scripting issues.  To fix the cross site scripting issues would
# reduce the functionality of my trusted users.  I wouldn't be opposed to
# a patch that would strip out hostile html/javascript, so long as it was
# controlled with a simple boolean config option. 
# 
# William McVey <wam@wamber.net>
# Sept 29, 2002
#

import sys
import cgi
import os

# Comment this out when going into production
import cgitb; cgitb.enable()

# toplevel path to where the files should get created
blog_root='/home/wam/weblog'

# include HTML syntax summary table?
include_html_syntax = 1

def user2Link(user): 
	"""given a username, return some representation of that user
	Generally, this will be an anchor ref of a mailto URL
	""" 
	# could also look up mail addrs via a table lookup, etc
	return '<a href="mailto:%(user)s@somewebsite.com">%(user)s</a>' % {"user": user}

# Nothing below here should need to be tailored...

def get_blog_dirs():
	logdirs=[]
	os.path.walk(blog_root, lambda arg, dirPath, paths: logdirs.append(dirPath[len(blog_root)+1:]), None)
	logdirs.sort()
	return logdirs

def getUser(): return os.environ.get("REMOTE_USER", None)

def validPath(category, filename):
	if category == ".": 
		category = ""		# special case for main directory
	categories=get_blog_dirs()
	if category not in categories:
		# XXX: I should escape any html in category to prevent
		# error page from cross site scripting (of course, it's
		# assumed that the person submitting has been authenticated
		# and is trusted...)
		raise RuntimeError, "Category `%s' does not exist" % category
	for hostile_char in r"/.`$&*?|;":
		if hostile_char in filename:
			raise RuntimeError, "Invalid character `%s' in filename.  Try to stay with alphanumerics, space, and underscore." % hostile_char
	return os.path.join(blog_root, category, filename +".txt")
	
def genFormPage():
	categories=get_blog_dirs()
	print """\
<html>
<head>
<title>content creation</title>
</head>
<body>
<form action="weblog-add.py">
<b>Category:</b>
<select name="category">"""
	for path in categories:
		name=path
		if path == "":   	# special case for root
			path="."
			name="MAIN"
		print """<option value="%s">%s</option>""" %(path, name)
	print """\
</select>
<p> 
<b>Title:</b>
<br>
<input type=text name="title" size=80 value=""> 
<p>
<b>Filename (no path and no extension):</b>
<br>
<input type=text name="filename" size=40 value=""> 
<p>
"""

	if include_html_syntax:
		print """\
<b>HTML Summary:</b>
<br>
<table border=1>
<tr><th>Hypertext link</th><td>&lt;a href="URL"&gt;linked text&lt;/a&gt;</td></tr>
<tr><th>Paragraph</th><td>&lt;p&gt;Text&lt;/p&gt;</td></tr>
<tr><th>Embedded image</th><td>&lt;img href="URL" align=<code>"left|right|top|bottom|middle"</code>&gt</td></tr>
<tr><th>Emphasized text</th><td>&lt;em&gt;<em>Text to emphasize</em>&lt;/em&gt;</td></tr>
<tr><th>Strongly emphasized text</th><td>&lt;strong&gt;<strong>Text to emphasize</strong>&lt;/strong&gt;</td></tr>
</table>
<p>"""
	print """\
<b>Content:</b> 
<br>
<textarea cols=80 rows=10 name="text"></textarea>
<br>
<input type=submit> 
</body>
</html>
"""

def error(msg):
	print "<html><head><title>Content Error!</title></head><body><h1>Content Error!</h1>%s</body></html>" % msg
	sys.exit(0)

def addContent(form):
	try:
		filename=validPath(form.getfirst("category"), form.getfirst("filename"))
	except RuntimeError, msg:
		error(msg)
	# XXX: should perhaps do more error checking here
	datafile=open(filename, "w")
	print >>datafile, form.getfirst("title")
	print >>datafile, '#author %s' % user2Link(getUser())
	print >>datafile, form.getfirst("text")
	datafile.close()
	print '<html><body><h1>Posted!</h1><a href="/">Return to webroot</a></body></html>'
	# XXX: return page should probably link to page to which 
	# content was added...  HTTP_REFERRER seems to be broken for
	# for me though...

if __name__ == '__main__':
	form = cgi.FieldStorage()
	print "Content-type: text/html\n"
	if not getUser(): 
		error("User not authenticated.")
	if form.has_key("text"):
		addContent(form)
		sys.exit(0)
	genFormPage()
	sys.exit(0)
