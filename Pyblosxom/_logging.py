"""
Emulates part of the Python2.3 logging module.

Note: This will probably not work with Python < 2.2.
"""

import os
import sys
import time
import string
try: from cStringIO import StringIO
except ImportError: from StringIO import StringIO

_devlogfile = "/tmp/dev-log.log"
_log = None

def dump(msg, *args):
    """
    Utility function to log stuff while working on the _logging module.
    """
    global _log
    if _log == None or _log.closed:
        _log = open(_devlogfile, "a")
    if args:
        msg = msg % args
    _log.write(str(msg))
    _log.write("\n")
    _log.flush()


# Log levels
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

# order matters!
_names = ['FATAL', 'CRITICAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
_levels = {}
_level_names = {}

def __populate_levels():
    """
    Fills in the _levels and _level_names dictionaries.
    """
    for n in _names:
        i = eval(n)
        _levels[n] = i
        _level_names[i] = n

__populate_levels()


# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame.
if string.lower(__file__[-4:]) in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

# _startTime is used as the base when calculating the relative time of events
_startTime = time.time()

def getLevelName(level):
    """
    Return the textual representation of logging level 'level'.
    
    @param level: Numeric representation of a logging level
    @type level: C{int}
    @return: Texutal representation of the logging level
    @rtype: C{str}
    """
    return _level_names.get(level, ("Level %s" % level))


# repository of handlers (for flushing when shutdown is called)
_handlers = {}  

class Filterer(object):
    """
    A stripped down version of the logging.Filterer class.
    See the logging module for documentation.
    """
    def __init__(self):
        self.filters = []

    def addFilter(self, filter):
        if not (filter in self.filters):
            self.filters.append(filter)

    def removeFilter(self, filter):
        if filter in self.filters:
            self.filters.remove(filter)

    def filter(self, record):
        rv = 1
        for f in self.filters:
            if not f.filter(record):
                rv = 0
                break
        return rv

class StreamHandler(Filterer):
    """
    A stripped down version of the logging.StreamHandler class.
    See the logging module for documentation.
    """
    def __init__(self, strm=sys.stderr):
        Filterer.__init__(self)
        #dump("StreamHandler.__init__: %s", strm)
        self.stream = strm
        self.formatter = None
        self.level = None
        global _handlers
        # store this handler in the global handler repository
        _handlers[self] = 1

    def setLevel(self, level):
        self.level = level

    def format(self, record):
        return self.formatter.format(record)

    def emit(self, record):
        try:
            msg = self.format(record)
            try:
                self.stream.write("%s\n" % msg)
            except UnicodeError:
                self.stream.write("%s\n" % msg.encode("UTF-8"))
            self.flush()
        except:
            self.handleError(record)

    def handleError(self, record):
        # handle errors in the logging implementation
        import traceback
        ei = sys.exc_info()
        traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
        del ei

    def handle(self, record):
        rv = self.filter(record)
        if rv:
            self.emit(record)
        return rv

    def setFormatter(self, formatter):
        self.formatter = formatter

    def flush(self):
        self.stream.flush()

    def close(self):
        # do nothing here, could be sys.stdout/stderr
        pass


class FileHandler(StreamHandler):
    """
    A stripped down version of the logging.FileHandler class.
    See the logging module for documentation.
    """
    def __init__(self, filename, mode="a"):
        super(FileHandler, self).__init__(open(filename, mode))
        self.baseFilename = filename
        self.mode = mode

    def close(self):
        self.stream.close()


class Formatter(object):
    """
    A stripped down version of the logging.Formatter class.
    See the logging module for documentation.
    """    
    converter = time.localtime

    def __init__(self, fmt="%(message)s"):
        self._fmt = fmt
        self.datefmt = None

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s,%03d" % (t, record.msecs)
        return s

    def formatException(self, ei):
        import traceback
        sio = StringIO()
        traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1] == "\n":
            s = s[:-1]
        return s

    def format(self, record):
        record.message = record.getMessage()
        if string.find(self._fmt,"%(asctime)") >= 0:
            record.asctime = self.formatTime(record, self.datefmt)
        s = self._fmt % record.__dict__
        if record.exc_info:
            if s[-1] != "\n":
                s = s + "\n"
            s = s + self.formatException(record.exc_info)
        return s

class LogRecord:
    """
    A stripped down version of the logging.LogRecord class.
    See the logging module for documentation.
    """
    def __init__(self, name, level, pathname, lineno, msg, args, exc_info):
        ct = time.time()
        self.name = name
        self.msg = msg
        self.args = args
        self.levelname = getLevelName(level)
        self.levelno = level
        self.pathname = pathname
        try:
            self.filename = os.path.basename(pathname)
            self.module = os.path.splitext(self.filename)[0]
        except:
            self.filename = pathname
            self.module = "Unknown module"
        self.exc_info = exc_info
        self.lineno = lineno
        self.created = ct
        self.msecs = (ct - long(ct)) * 1000
        self.relativeCreated = (self.created - _startTime) * 1000
        if hasattr(os, 'getpid'):
            self.process = os.getpid()
        else:
            self.process = None

    def __str__(self):
        return '<LogRecord: %s, %s, %s, %s, "%s">'%(self.name, self.levelno,
            self.pathname, self.lineno, self.msg)

    def getMessage(self):
        try:
            msg = str(self.msg)
        except UnicodeError:
            msg = self.msg      #Defer encoding till later
        if self.args:
            msg = msg % self.args
        return msg


class Logger(Filterer):
    """
    A stripped down version of the logging.Logger class.
    See the logging module for documentation.
    """
    def __init__(self, name, level=NOTSET):
        Filterer.__init__(self)
        self.name = name
        self.setLevel(level)
        self.handlers = []
        self.disabled = 0

    def _log(self, level, msg, args, exc_info=None):
        # log the message or not depending on the current loglevel
        if self.level > level:
            return
        if _srcfile:
            fn, lno = self.__findCaller()
        else:
            fn, lno = "<unknown file>", 0
        if exc_info:
            exc_info = sys.exc_info()
        record = self.__makeRecord(self.name, level, fn, lno, msg, args, exc_info)
        self.__callHandlers(record)

    def __findCaller(self):
        f = sys._getframe(1)
        while 1:
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            return filename, f.f_lineno

    def __makeRecord(self, name, level, fn, lno, msg, args, exc_info):
        return LogRecord(name, level, fn, lno, msg, args, exc_info)

    def __callHandlers(self, record):
        for hdlr in self.handlers:
            if record.levelno >= hdlr.level:
                hdlr.handle(record)


    # public methods

    def setLevel(self, level):
        self.level = level

    def critical(self, msg, *args, **kwargs):
        apply(self._log, (CRITICAL, msg, args), kwargs)
    fatal = critical

    def error(self, msg, *args, **kwargs):
        apply(self._log, (ERROR, msg, args), kwargs)

    def warning(self, msg, *args, **kwargs):
        apply(self._log, (WARNING, msg, args), kwargs)
    warn = warning

    def info(self, msg, *args, **kwargs):
        apply(self._log, (INFO, msg, args), kwargs)

    def debug(self, msg, *args, **kwargs):
        apply(self._log, (DEBUG, msg, args), kwargs)

    def exception(self, msg, *args):
        apply(self.error, (msg,) + args, {'exc_info': 1})

    def addHandler(self, hdlr):
        if not (hdlr in self.handlers):
            self.handlers.append(hdlr)

    def removeHandler(self, hdlr):
        if hdlr in self.handlers:
            self.handlers.remove(hdlr)




# A dict to keep track of created loggers.
_logger_registry = {}

def getLogger(log_name=None):
    """
    Creates and returns a logging channel.
    Registers the created logger in the logger-registry for further reference.
    """
    #dump("getLogger: %s", log_name)
    global _logger_registry
    if not log_name:
        log_name == "root"
    if not log_name in _logger_registry:
        _logger_registry[log_name] = Logger(log_name)
    return _logger_registry[log_name]


def shutdown():
    """
    Close logfiles and clear the logger-registry.
    """
    #dump("shutdown")
    global _handlers, _logger_registry
    for h in _handlers.keys():
        h.flush()
        h.close()
    _handlers = {}
    _logger_registry = {}
