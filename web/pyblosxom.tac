"""
Example tac file for running Pyblosxom on twisted:

Dependencies
============

* Pyblosxom 1.2+
* wsgiref library from http://cvs.eby-sarna.com/wsgiref/
* twisted wsgi wrapper (twisted_wsgi.py)
  from http://svn.webwareforpython.org/WSGIKit/trunk/wsgikit/

Configuration
=============

Fill in the desired username and port in the options dict below.
The username defaults to the current users name if the one specified
does not exist.

Usage::

  twistd -noy pyblosxom.tac    # for testing
  twistd -y pyblosxom.tac      # for real

Read the twistd manpage for more information.
"""
# twisted imports
from twisted.application import internet, service
from twisted.web import server
from twisted.python import usage

# Pyblosxom and wsgi imports
from twisted_wsgi import WSGIResource
from wsgi_app import application as pyblosxom_application

options = {
    'user': 'doesnotexist',
    'port': 8080
}

def makeApplication(config):
    try:
        # *NIX
        import pwd
        p_user = pwd.getpwnam(config['user'])
        uid = p_user[2]
        gid = p_user[3]
    except ImportError:
        # Windows
        uid = 0
        gid = 0
    except:
        import os
        # use current users uid/gid
        uid = os.getuid()
        gid = os.getgid()

    return service.Application('pyblosxom', uid=uid, gid=gid)


def makeService(config):
    resource = WSGIResource(pyblosxom_application, async=False)
    return internet.TCPServer(config.get('port', 8080), server.Site(resource))

application = makeApplication(options)
makeService(options).setServiceParent(application)
