# vim: tabstop=4 shiftwidth=4 expandtab
# This document uses epydoc syntax, see http://epydoc.sf.net
"""
C{README} for Plugins

Inside the C{contrib/} directory, you'll see the C{plugins/} directory. To
install a given plugin, move the plugin file you want from the C{contrib/}
directory to the C{Pyblosxom/plugins/} directory of your installation.

Some plugins take effect immediately, like the C{conditionalhttp.py} and the
C{statusnotfound.py}.  Some plugins require some setup before they work.
Read the plugin file in a text editor to see what installation steps are
required.

Below is some basic documentation for plugin developers and details
callbacks available, how they should be used, and what they do.

B{The BlosxomRenderer plugin callbacks}

The L{BlosxomRenderer} plugins supports set of callback functions based on the
blosxom 2.0 callbacks.  The names arguments are different, but the
L{BlosxomRenderer} callbacks are called at the same points that the blosxom 2.0
callbacks are called.

All of the BlosxomRenderer callbacks take the same three arguments

The available blosxom renderer callbacks are:
 
    - L{cb_head} (corresponds to blosxom 2.0 head)
    - L{cb_date_head} (corresponds to blosxom 2.0 date)
    - L{cb_story} (corresponds to blosxom 2.0 story)
    - L{cb_foot} (corresponds to blosoxm 2.0 foot)

In PyBlosxom, the functionality some of the blosxom 2.0 callbacks are taken
care of by callback chains.

     - The blosxom 2.0 entries callback is handled by L{cb_filelist}
     - The blosxom 2.0 filter callback is handled by L{cb_prepare}
     - The blosxom 2.0 sort callback is handled by L{cb_prepare}

B{verify_installation}

For 0.9, I made changes to pyblosxom.cgi so that you could run it from 
the prompt::

   ./pyblosxom.cgi

It tells you your Python version, OS name, and then proceeds to verify
your config properties (did you specify a valid datadir?  does it
exist?...) and then initializes all your plugins and executes
verify_installation(request) on every plugin you have
installed that has the function.

As a plugin developer, you should add a verify_installation function
to your plugin module.  Something like this (taken from pycategories)::

   def verify_installation(request):
       config = request.getConfiguration()

       if not config.has_key("category_flavour"):
           print "missing optional config property 'category_flavour' which allows "
           print "you to specify the flavour for the category link.  refer to "
           print "pycategory plugin documentation for more details."
       return 1

Basically this gives you (the plugin developer) the opportunity to
walk the user through configuring your highly complex, quantum-charged,
turbo plugin in small baby steps without having to hunt for where
their logs might be.

So check the things you need to check, print out error messages
(informative ones), and then return a 1 if the plugin is configured 
correctly or a 0 if it's not configured correctly.

This is not a substitute for reading the installation instructions.  But
it should be a really easy way to catch a lot of potential problems
without involving the web server's error logs and debugging information
being sent to a web-browser and things of that nature.
"""
import Pyblosxom, os
from Pyblosxom.Request import Request
from Pyblosxom.renderers.blosxom import BlosxomRenderer
from Pyblosxom.entries.base import EntryBase
from Pyblosxom.pyblosxom import PyBlosxom

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
    A callback to generate a list of L{EntryBase} subclasses. 
    
    If C{None} is returned, then the callback chain will try the next plugin in
    the list.

    @param args: A dict containing a L{Request()} object
    @type args: dict
    @returns: None or list of L{EntryBase}.
    @rtype: list
    """
    pass


def cb_pathinfo(args = {'request' : Request()}):
    """
    A callback to allow plugins to alter the way HTTP PATH_INFO is parsed.
    The following keys must be set in args['request'].getData() in order to
    prevent conflicts with the default renderer and entry parsers::

      'bl_type'       (dir|file)
      'pi_bl'         typically the same as PATH_INFO
      'pi_yr'         yyyy
      'pi_mo'         (mm|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)
      'pi_da'         dd
      'root_datadir'  full path to the entry folder or entry file on filesystem
      'flavour'       The flavour gathered from the URL
    """
    pass


def cb_renderer(args = {'request' : Request()}):
    """
    A callback to returb a L{Pyblosxom.renderers.base.RendererBase} instance.
    The default renderer is the ones available in the L{Pyblosxom.renderers} as
    default, and called using::
                
      tools.importName('Pyblosxom.renderers', 
              config.get('renderer', 'blosxom')).Renderer(self._request, 
              config.get('stdoutput', sys.stdout)))
    
    If C{None} is returned, then the callback chain will try the next plugin in
    the list.

    @param args: A dict containing a L{Request()} object
    @type args: dict
    @returns: None or a L{Pyblosxom.renderers.base.RendererBase} instance
    @rtype: object instace
    """
    pass


def cb_entryparser(args = {'txt': 'A blosxom text entryparser'}):
    """
    A callback that tranforms a dict, containing a list of keys - the extension
    of files it can take, and a function reference, that accepts two arguments,
    a filename, and the standard request object.

    The function is supposed to return a dict, at least containing the key
    C{'title'} and C{'story'}. Entryparsers can use other callback facilities
    like L{cb_preformat} and the L{cb_postformat} callbacks. See
    L{Pyblosxom.pyblosxom.blosxom_entry_parser} on how to use such facilities.

    All outputs of entryparsers (and together with preformatters and
    postformatters) will be cached by the caching mechanisms.
    
    Plugins are supposed to add more keys as the extension of the file it can
    handle. A plugin can also replace the standard txt entryparser if the need
    be.  All plugins that registers C{cb_filestat} are given a chance to take a
    peek at the args, append to it, or modify it (not advisable).

    By default, typical contents of args::
        {'txt': L{Pyblosxom.pyblosxom.blosxom_entry_parser}}

    Here's an example code that reads *.plain files::

        import os
        def cb_entryparser(args):
            \"""
            Register self as plain file handler
            \"""
            args['plain'] = parse
            return args

        def parse(filename, request):
            \"""
            We just read everything off the file here, using the filename as
            title
            \"""
            entryData = {}
            entryData['title'] = os.path.basename(filename)
            entryData['story'] = open(filename).read()
            return entryData

    Upon a successful registration, pyblosxom will now read all *.plain and
    *.txt files from the data directory

    @param args: A dict that comtains function references to entryparsers
    @type args: dict
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
    entry text, called after a preformatter. It can also be used for 
    extensive operations on a particular entry, adding extra keys to the 
    given 'entry_data' dict. If a cache is used in a particular installation, 
    the resulting data will be saved in the cache, so using this chain may 
    not be useful for dynamic data like comment counts, for example. 

    Examples of usage:

        - Adding a word count property to the entry
        - Using a macro replacement plugin (Radio Userland glossary)
        - Acronym expansion
        - A 'more' text processor

    A typical C{args} contains the following:

        - C{'entry_data'} - A dict that minimally contains a C{'title'} and
              a C{'story'}
        - C{'request'} - A typical L{Request} object

    @param args: A dict containing a L{Request()} object, and an entry_data 
         dict
    @type args: dict
    """
    pass

def cb_start(args = {'request': Request()}):
    """
    A start up callback for plugins
    
    The start callback can be used to perform initialization of a callback.
    Use this callback for any setup code that your plugin needs, like
    
        - reading saved data from a file
        - checking to make sure configuration variables are set
    
    @param args: A dict containing a L{Request()} object
    @type args: dict
    """
    pass

def cb_end(args = {'request' : Request()}):
    """
    A finalization callback for plugins
    
    The end callback can be used to perform finalization for a callback.
    Use the end callback to clean up after your plugin has executed.  This
    is the place to
    
        - save data to a file
        - clean up any temporary files
    
    @param args: A dict containing a L{Request()} object
    @type args: dict
    """
    pass


def cb_head(args = {'renderer':'The Blosxom renderer', 
                    'entry':'The entry to render',
                    'template':'The template to be filled in'}):
    """
    A callback that is called before a head flavour template is rendered
    
    C{cb_head} is called before the variables in the entry are substituted
    into the template.  This is the place to modify the head template based
    on the entry content.  You can also set variables on the entry that will
    be used by the C{cb_story} or C{cb_foot} templates.  You have access to 
    all the content variables via entry.
    
    Blosxom 2.0 calls this callback 'head'

    C{args} contains
    
      - C{'renderer'} - the L{BlosxomRenderer} that called the callback
      - C{'entry'} - a L{EntryBase} to be rendered
      - C{'template'} - a string containing the flavour template to be processed

    @param args: a dict containing a L{BlosxomRenderer}, L{EntryBase}, and template
    @type args: dict
    """
    pass

def cb_date_head(args = {'renderer':'The Blosxom renderer', 
                         'entry':'The entry to render',
                         'template':'The template to be filled in'}):
    """
    A callback that is called before a date_head flavour template is rendered
    
    C{cb_head} is called before the variables in the entry are substituted
    into the template.  This is the place to modify the date_head template 
    based on the entry content.  You have access to all the content variables 
    via entry.
    
    Blosxom 2.0 calls this callback 'date'

    C{args} contains
    
      - C{'renderer'} - the L{BlosxomRenderer} that called the callback
      - C{'entry'} - a L{EntryBase} to be rendered
      - C{'template'} - a string containing the flavour template to be processed

    @param args: a dict containing a L{BlosxomRenderer}, L{EntryBase}, and template
    @type args: dict
    """
    pass

def cb_story(args = {'renderer':'The Blosxom renderer', 
                     'entry':'The entry to render',
                     'template':'The template to be filled in'}):
    """
    A callback that is called before a story flavour template is rendered
    
    C{cb_story} is called before the variables in the entry are substituted
    into the template.  This is the place to modify the story template based
    on the entry content.  You have access to all the content variables via 
    entry.
    
    Blosxom 2.0 calls this callback 'story'

    C{args} contains
    
      - C{'renderer'} - the L{BlosxomRenderer} that called the callback
      - C{'entry'} - a L{EntryBase} to be rendered
      - C{'template'} - a string containing the flavour template to be processed

    @param args: a dict containing a L{BlosxomRenderer}, L{EntryBase}, and template
    @type args: dict
    """
    pass

def cb_story_end(args = {'renderer':'The Blosxom renderer', 
                     'entry':'The entry to render',
                     'template':'The template to be filled in'}):
    """
    A callback that is called after a story flavour template is rendered
    
    C{cb_story} is called after the variables in the entry are substituted
    into the template.  You have access to all the content variables via 
    entry.
    
    C{args} contains
    
      - C{'renderer'} - the L{BlosxomRenderer} that called the callback
      - C{'entry'} - a L{EntryBase} to be rendered
      - C{'template'} - a string containing the flavour template to be processed

    @param args: a dict containing a L{BlosxomRenderer}, L{EntryBase}, and template
    @type args: dict
    """
    pass

def cb_foot(args = {'renderer':'The Blosxom renderer', 
                    'entry':'The entry to render',
                    'template':'The template to be filled in'}):
    """
    A callback that is called before a footflavour template is rendered
    
    C{cb_foot} is called before the variables in the entry are substituted
    into the template.  This is the place to modify the foot template based
    on the entry content.  You have access to all the content variables via 
    entry.
    
    Blosxom 2.0 calls this callback 'foot'

    C{args} contains
    
      - C{'renderer'} - the L{BlosxomRenderer} that called the callback
      - C{'entry'} - a L{EntryBase} to be rendered
      - C{'template'} - a string containing the flavour template to be processed

    @param args: a dict containing a L{BlosxomRenderer}, L{EntryBase}, and template
    @type args: dict
    """
    pass

