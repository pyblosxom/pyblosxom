# vim: tabstop=4 shiftwidth=4 expandtab
"""
C{README} for Plugins

Inside the C{contrib/} directory, you'll see the C{plugins/} directory. To
install a given plugin, move the plugin file you want from the C{contrib/}
directory to the C{libs/plugins/} directory of your installation.

Some plugins take effect immediately, like the C{conditionalhttp.py} and the
C{statusnotfound.py}. Some requires a little bit more information in using it,
like files to store data, or some variables to put inside your flavour
templates.  Do read the plugin file itself to see what extra steps you need 
to do before installing it.

Below is a basic documentation for plugin developers and it exposes them
of what callbacks are available to them and documents on how to use them
if possible.
"""
import libs, os
from libs.Request import Request

def cb_prepare(args):
    """
    A callback to prepare data before a renderin.
    
    This callback is called before we go through the renderer. Arguments
    contains:

     - C{'request'} - The L{Request} object at the particular moment

    Most plugins can use the prepare chain to either transform or add to the
    L{Request.getData()} dict. Some plugins could also use the C{'entry_list'}
    list of entries and modify data there.

    Here's an example of a prepare chain plugin::

        def cb_prepare(args):
            \"""
            This plugin shows the number of entry we are going to print and
            place the result in $countNoOfEntries
            \"""
            request = args['request']
            data = request.getData()
            config = request.getConfiguration()
            # Can anyone say Ternary? :)
            IF = lambda a,b,c:(a() and [b()] or [c()])[0]

            num_entry = config['num_entries']
            entries = len(data['entry_list'])

            data['countNoOfEntries'] = IF(num_entry > entries, num_entry, entries)

    @param args: A dict containing a L{Request()} object
    @type args: dict
    """
    pass


def cb_logrequest(args = {'filename': 'A file', 
        'return_code': 'A http return code', 'request': Request()}):
    """
    This callback is responsible for logging a typical request. 
    
    A dict, C{args} is given containing:

     - C{'filename'} - a filename (typically a base filename)
     - C{'return_code'} - A HTTP error code (e.g 200, 404, 304)
     - C{'request'} - a L{Request} object

    No return is expected from this callback. This is usually called at the
    last point of rendering

    A typical contents of args::
        filename = config.get('logfile', '')
        {'filename': filename, 
         'return_code': '200',
         'request': Request()}

    @param args: A dict containing the keys request, filename and return_code
    @type args: dict
    """
    pass


def cb_filestat(args = {'filename': 'A file', 'mtime': os.stat('/')}):
    """
    A callback that returns a file C{stat} based on the arguments received. 
    
    The args received is a dict containing:
        
     - C{'filename'} - a physical file and 
     - C{'mtime'} - what is returned by C{os.stat} function. 

    Plugins are supposed to transform the value of mtime if a certain condition
    is met, according to the plugin. All plugins that registers C{cb_filestat}
    are given a chance to take a peek at the args.

    A typical contents of args::
        filename = '/home/someone/blosxom/cat/file.txt'
        {'filename': filename, 
         'mtime': os.stat(filename)}

    @param args: A dict with two keys, filename and mtime
    @type args: dict
    """
    pass


def cb_filelist(args = {'request' : Request()}):
    """
    A callback to generate a list of L{libs.entries.base.EntryBase} subclasses. 
    
    If C{None} is returned, then the callback chain will try the next plugin in
    the list.

    @param args: A dict containing a L{Request()} object
    @type args: dict
    @returns: None or list of L{libs.entries.base.EntryBase}.
    @rtype: list
    """
    pass


def cb_preformat(args = 
        {'parser': 'somepreformatter', 
         'story': ['The\n','text\n'], 
         'request': Request()}):
    """
    A callback for preformatters.
    
    A preformatter is a text transformation tool.  Only one preformatter can
    run at an entry at a time. In this chain, all preformatters are called
    until one returns a string and not C{None}.

    Preformatters should act on the parser, and if it matches what the
    preformatter can handle it can carry on an deal with the story.

    C{args} contains:

     - C{'parser'} - A string that determines whether a preformatter should run
     - C{'story'} - A list containing lines of text (with '\\n' included)
     - C{'request'} - a L{Request} object

    A typical preformat plugin look like::

        def cb_preformat(args):
            if args['parser'] == 'linebreaks':
                return parse(''.join(args['story']))

        def parse(text):
            # A preformatter to convert linebreak to its HTML counterpart
            text = re.sub('\\n\\n+','</p><p>',text)
            text = re.sub('\\n','<br />',text)
            return '<p>%s</p>' % text

    @param args: A dict containing a L{Request()} object, parser identifier and
            story list of lines
    @type args: dict
    @returns: A string containing formatted text
    @rtype: string
    """
    pass


def cb_postformat(args = {'entry_data': {}, 'request': Request()}):
    """
    A callback for postformatters

    Postformatters are callbacks that may make further modification to the
    entry text, called after a preformatter, it can also be used for extensive
    operations on a particular entry, adding extra keys to the given
    'entry_data' dict. If a cache is used in a particular installation, the
    resulting data will be saved in the cache, so using this chain may not be
    useful for dynamic data like comment counts, for example. Acceptable
    operations includes:

        - Adding a word count
        - Using a macro replacement plugin (Radio Userland glossary)
        - Acronym expansion
        - A 'more' text processor

    A typical C{args} contains the following:

        - C{'entry_data'} - A dict that minimally contains a C{'title'} and a
              C{'story'}
        - C{'request'} - A typical L{Request} object

    @param args: A dict containing a L{Request()} object, and an entry_data dict
    @type args: dict
    """
    pass
