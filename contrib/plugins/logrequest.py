# vim: tabstop=4 shiftwidth=4 expandtab
"""
Standard logRequest plugin.

Drop this file in the Pyblosxom/plugins/ directory of pyblosxom, and in your
config.py (or your config INI file depending on your installation), create a
config entry called logfile and this will be the filename you want this
logRequest plugin to log to.

For example in config.py:
py['logfile'] = '/path/to/file'

or in the INI file:
logfile = /path/to/file

The resulting file will be file + the extension of .txt

If the filename is relative, then it will be written to where pyblosxom runs.
"""
def cb_logrequest(args):
    import os, time
    filename = args["filename"] + '.txt'
    returnCode = args["return_code"]
    httpData = args['request'].getHttp()

    file(filename, 'a').write('%s - - [%s] "%s %s" %s - "%s" "%s"\n' %
        (httpData.get('REMOTE_ADDR', '-'),
        time.strftime('%d/%b/%Y:%H:%M:%S %Z', time.localtime()),
        httpData.get('REQUEST_METHOD', '-'),
        httpData.get('REQUEST_URI', '-'),
        returnCode,
        httpData.get('HTTP_REFERER', '-'),
        httpData.get('HTTP_USER_AGENT', '-')))
