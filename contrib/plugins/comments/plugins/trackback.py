"""
This plugin allows pyblosxom to process trackback pings.  You must have the 
comments plugin installed as well, although you don't need to enable comments 
on your blog in order for trackbacks to work

%<---------------------------------------------------------
py['trackback_urltrigger'] = "/trackback"
%<---------------------------------------------------------

"""
import cgi
from Pyblosxom import tools

tools.make_logger('/tmp/trackback.log')

tb_good_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>0</error>
</response>"""

tb_bad_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>1</error>
<message>%s</message>
</response>"""

def verify_installation(request):
    config = request.getConfiguration()
    retval = 1

    # all config properties are optional
    if not config.has_key('trackback_urltrigger'):
        print("missing optional property: 'trackback_urltrigger'")

    return retval

def cb_handle(args):
    """

    @param args: a dict of plugin arguments
    @type args: dict
    """
    request = args['request']
    pyhttp = request.getHttp()
    config = request.getConfiguration()

    urltrigger = config.get('trackback_urltrigger','/trackback')

    path_info = pyhttp['PATH_INFO']
    if path_info.startswith(urltrigger):
        print "Content-type: text/xml"
        print

        form = cgi.FieldStorage()

        message = "not trackback"
        if form.has_key("title") and form.has_key("excerpt") and \
               form.has_key("url") and form.has_key("blog_name"):
            import time
            cdict = { 'title': form['title'].value, \
                      'author': 'Trackback from %s' % form['blog_name'].value, \
                      'pubDate' : str(time.time()), \
                      'link' : form['url'].value, \
                      'source' : form['blog_name'].value, \
                      'description' : form['excerpt'].value }
            from Pyblosxom.entries.fileentry import FileEntry
            from Pyblosxom.Request import Request
            from Pyblosxom.pyblosxom import PyBlosxom

            datadir = config['datadir']

            from comments import writeComment    
            try:
                import os
                pi = path_info.replace(urltrigger,'')
                path = os.path.join(datadir, pi[1:])
                data = request.getData()
                ext = tools.what_ext(data['extensions'].keys(), path)
                entry = FileEntry(request, '%s.%s' % (path, ext), datadir )
                data = {}
                data['entry_list'] = [ entry ]
                writeComment(config, data, cdict)
                print tb_good_response
            except OSError:
                message = 'URI '+path_info+" doesn't exist"
                tools.log(message)
                print tb_bad_response % message

        else:
            tools.log(message)
            print tb_bad_response % message

        import sys
        sys.stdout.flush()
        # no further handling is needed
        return 1
    else:
        return 0
