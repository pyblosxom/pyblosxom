"""
This plugin allows pyblosxom to process trackback pings.  You must have the 
comments plugin installed as well, although you don't need to enable comments 
on your blog in order for trackbacks to work

%<---------------------------------------------------------
py['trackback_urltrigger'] = "/trackback"
%<---------------------------------------------------------

"""
import cgi, os, os.path
from Pyblosxom import tools

tb_good_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>0</error>
</response>"""

tb_bad_response = """<?xml version="1.0" encoding="iso-8859-1"?>
<response>
<error>1</error>
<message>%s</message>
</response>"""

def cb_start(args):
    request = args["request"]
    config = request.getConfiguration()
    logdir = config.get("logdir", "/tmp")
    logfile = os.path.normpath(logdir + os.sep + "trackback.log")

    tools.make_logger(logfile)

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
        response = request.getResponse()
        response.addHeader("Content-type", "text/xml")

        form = request.getForm()

        message = "A trackback must have at least a URL field (see http://www.sixapart.com/pronet/docs/trackback_spec )"

        if form.has_key("url"):
            import time
            cdict = { 'title': form.getvalue('title', ''), \
                      'author': 'Trackback from %s' % form.getvalue('blog_name', ''), \
                      'pubDate' : str(time.time()), \
                      'link' : form['url'].value, \
                      'source' : form.getvalue('blog_name', ''), \
                      'description' : form.getvalue('excerpt', '') }
            from Pyblosxom.entries.fileentry import FileEntry
            from Pyblosxom.pyblosxom import Request
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
                writeComment(request, config, data, cdict, config['blog_encoding'])
                print >> response, tb_good_response
            except OSError:
                message = 'URI '+path_info+" doesn't exist"
                tools.log(message)
                print >> response, tb_bad_response % message

        else:
            tools.log(message)
            print >> response, tb_bad_response % message

        # no further handling is needed
        return 1
    else:
        return 0
