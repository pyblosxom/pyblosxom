# vim: tabstop=4 shiftwidth=4 expandtab
# This document uses epydoc syntax, see http://epydoc.sf.net
"""
C{README} for Plugins and Plugin writing

Inside the C{contrib/} directory, you'll see the C{plugins/} directory. To
install a given plugin, move the plugin file you want from the C{contrib/}
directory to the C{Pyblosxom/plugins/} directory of your installation.

Some plugins take effect immediately, like the C{conditionalhttp.py} and the
C{statusnotfound.py}.  Some plugins require some setup before they work.
Read the plugin file in a text editor to see what installation steps are
required.

Below is documentation for plugin developers detailing the standard
callbacks that they can use to implement plugins.


B{Implementing a callback in a plugin}

If you want to implement a callback, you add a function corresponding
to the callback name to your plugin module.  For example, if you wanted
to modify the L{Request} object just before rendering, you'd implement
cb_prepare something like this::

    def cb_prepare(args):
        pass

Each callback passes in arguments through a single dictionary.  Each
callback passes in different arguments and expects different return
values.  Consult the documentation for the callback you're seeking
before implementing it in your code to understand what it does and
how to use it.


B{The BlosxomRenderer plugin callbacks}

The L{BlosxomRenderer} plugins are based on the blosxom 2.0 callbacks.
The names of the arguments are different, but the callbacks are called
at the same points that the blosxom 2.0 callbacks are called and serve
the same function.

The available blosxom renderer callbacks are:
 
    - L{cb_head} (corresponds to blosxom 2.0 head)
    - L{cb_date_head} (corresponds to blosxom 2.0 date)
    - L{cb_story} (corresponds to blosxom 2.0 story)
    - L{cb_foot} (corresponds to blosoxm 2.0 foot)

Some of the other blosxom 2.0 callbacks are handled slightly differently
in PyBlosxom.

     - The blosxom 2.0 entries callback is handled by L{cb_filelist}
     - The blosxom 2.0 filter callback is handled by L{cb_prepare}
     - The blosxom 2.0 sort callback is handled by L{cb_prepare}

See the callback documentation below for more details.


B{verify_installation}

As of PyBlosxom 0.9, the pyblosxom.cgi is able to test your PyBlosxom
installation.  It verifies certain items in your config file and also
loads all the plugins and lets them verify their configuration as well.

At the prompt, you would run::

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
from Pyblosxom.pyblosxom import Request
from Pyblosxom.renderers.blosxom import BlosxomRenderer
from Pyblosxom.entries.base import EntryBase
from Pyblosxom.pyblosxom import PyBlosxom

def cb_prepare(args):
    """
    The prepare callback is called in the default blosxom handler after 
    we've figured out what we're rendering and before we actually go to the
    renderer.

    Plugins should implement cb_prepare to modify the data dict which 
    is in the L{Request}.  Inside the data dict is C{'entry_list'} 
    (amongst other things) which holds the list of entries to be renderered 
    (in the order they will be rendered).

    Functions that implement this callback will get an args dict
    containing:

     - C{'request'} - The L{Request} object at the particular moment

    Functions that implement this callback can return whatever they want--it
    doesn't affect the callback chain.

    Example of a C{cb_prepare} function in a plugin::

        def cb_prepare(args):
            \"""
            This plugin shows the number of entries we are going to render and
            place the result in $countNoOfEntries.
            \"""
            request = args['request']
            data = request.getData()
            config = request.getConfiguration()

            # Can anyone say Ternary? :)
            IF = lambda a,b,c:(a() and [b()] or [c()])[0]

            num_entry = config['num_entries']
            entries = len(data['entry_list'])

            data['countNoOfEntries'] = IF(num_entry > entries, num_entry, entries)
    @param args: dict containing C{'request'}
    @type  args: dict

    @return: none
    @rtype:  none
    """
    pass


def cb_logrequest(args):
    """
    This callback is used to notify plugins of the current PyBlosxom
    request for the purposes of logging.

    Functions that implement this callback will get an args dict
    containing:

     - C{'filename'} - a filename (typically a base filename)
     - C{'return_code'} - A HTTP error code (e.g 200, 404, 304)
     - C{'request'} - a L{Request} object

    Functions that implement this callback can return whatever they want--it
    doesn't affect the callback chain.

    cb_logrequest is called after rendering and will contain all the
    modifications to the L{Request} object made by the plugins.

    An example input args dict is like this::

        {'filename': filename, 'return_code': '200', 'request': Request()}

    @param args: a dict containing C{'filename'}, C{'return_code'}, and
        C{'request'}
    @type  args: dict

    @return: none
    @rtype:  none
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
    handle.  A plugin can also replace the standard txt entryparser if the need
    be.  All plugins that registers C{cb_entryparser} are given a chance 
    to take a peek at the args, append to it, or modify it (not advisable).

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
    Callback that allows plugins to execute startup/initialization code.
    Use this callback for any setup code that your plugin needs, like:
    
        - reading saved data from a file
        - checking to make sure configuration variables are set
        - allocating resources

    Note: The cb_start callback is slightly different than in blosxom in 
    that cb_start is called for every PyBlosxom request regardless of 
    whether it's handled by the default blosxom handler.  In general,
    it's better to delay allocating resources until you absolutely know 
    you are going to use them.
    
    
    @param args: A dict containing a L{Request()} object
    @type args: dict
    """
    pass

def cb_end(args = {'request' : Request()}):
    """
    Allows plugins to perform teardown.
    
    The cb_end callback should be used to return any resources allocated,
    save any data that hasn't been saved, clean up temporary files,
    and otherwise return the system to a normal state.

    Use the end callback to clean up after your plugin has executed.  This
    is the place to
    
        - save data to a file
        - clean up any temporary files
    
    Note: The cb_end callback is called for every PyBlosxom request regardless
    of whether it's handled by the default blosxom handler.  This is slightly
    different than blosxom.

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

def cb_story(args = {'renderer': 'The Blosxom renderer', 
                     'request': 'The PyBlosxom Request',
                     'entry': 'The entry to render',
                     'template': 'The template to be filled in'}):
    """
    This callback gets called before the entry is rendered.  The template
    used is typically the story template, but we allow entries to override
    this if they have a "template" property.  If they have the "template"
    property, then we'll use that template instead.

    C{cb_story} is called before the variables in the entry are substituted
    into the template.  This is the place to modify the story template based
    on the entry content.  You have access to all the content variables via 
    entry.
    
    Blosxom 2.0 calls this callback 'story'

    C{args} contains
    
      - C{'renderer'} - the L{BlosxomRenderer} that called the callback
      - C{'request'} - the PyBlosxom a L{Request} being handled
      - C{'template'} - a string containing the flavour template to be processed
      - C{'entry'} - a L{EntryBase} object to be rendered

    Example:

    @param args: a dict containing a L{BlosxomRenderer}, L{Request}, L{EntryBase}, and template
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

