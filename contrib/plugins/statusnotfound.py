# vim: tabstop=4 shiftwidth=4 expandtab
"""
404 Error Generator

If there are no entries in the entryList, abort with 404 Error
"""
__author__ = "Wari Wahab pyblosxom@wari.per.sg"
__version__ = "$Id$"
def load(py, entryList, renderer):
    # Generate our own 404 Error
    if not entryList:
        renderer.addHeader(['Status: 404 Not Found', 'Content-Type: text/html'])
        renderer.setContent({'title': 'The page you are looking for is not available',
            'body': 'Somehow I cannot find the page you want. Go Back to <a href="%(base_url)s">%(blog_title)s</a>?' % py})
        renderer.render()

        from libs import tools
        tools.logRequest(py.get('logfile',''), '404')
