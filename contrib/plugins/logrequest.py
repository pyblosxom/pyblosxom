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


Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright 2004, 2005 Wari Wahab
"""
__version__ = "$Id$"

def cb_logrequest(args):
    import os, time
    filename = args["filename"] + '.txt'
    returnCode = args["return_code"]
    httpData = args['request'].getHttp()

    open(filename, 'a').write('%s - - [%s] "%s %s" %s - "%s" "%s"\n' %
        (httpData.get('REMOTE_ADDR', '-'),
        time.strftime('%d/%b/%Y:%H:%M:%S %Z', time.localtime()),
        httpData.get('REQUEST_METHOD', '-'),
        httpData.get('REQUEST_URI', '-'),
        returnCode,
        httpData.get('HTTP_REFERER', '-'),
        httpData.get('HTTP_USER_AGENT', '-')))
