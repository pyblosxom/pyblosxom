# vim: shiftwidth=4 tabstop=4 expandtab
import os, time, string, re, cgi
from libs import tools
import cPickle as pickle

class PyBlosxom:
    def __init__(self, py, xmlrpc):
        self.py = py
        self.xmlrpc = xmlrpc
        self.flavour = {}
        self.dayFlag = 1 # Used to print valid date footers
        
    def startup(self):
        self.py['pi_bl'] = ''
        path_info = []

        # If we use XML-RPC, we don't need favours and GET/POST fields
        if not (os.environ.get('PATH_INFO','') == self.xmlrpc['path'] and int(self.xmlrpc['enable'])):
            form = cgi.FieldStorage()
            self.py['flavour'] = (form.has_key('flav') and form['flav'].value or 'html')

            # Get the blog name if possible
            if os.environ.has_key('PATH_INFO'):
                path_info = os.environ['PATH_INFO'].split('/')
                if path_info[0] == '':
                    path_info.pop(0)
                while re.match(r'^[a-zA-Z]\w*', path_info[0]):
                    self.py['pi_bl'] += '/%s' % path_info.pop(0)
                    if len(path_info) == 0:
                        break

            self.py['root_datadir'] = self.py['datadir']
            if os.path.isdir(self.py['datadir'] + self.py['pi_bl']):
                if self.py['pi_bl'] != '':
                    self.py['blog_title'] += ' : %s' % self.py['pi_bl']
                self.py['root_datadir'] = self.py['datadir'] + self.py['pi_bl']
                self.py['bl_type'] = 'dir'
            elif os.path.isfile(self.py['datadir'] + self.py['pi_bl'] + '.txt'):
                self.py['blog_title'] += ' : %s' % re.sub(r'/[^/]+$','',self.py['pi_bl'])
                self.py['bl_type'] = 'file'
                self.py['root_datadir'] = self.py['datadir'] + self.py['pi_bl'] + '.txt'
            else:
                match = re.search(r'\.(\w+)$',self.py['pi_bl'])
                probableFile = self.py['datadir'] + re.sub(r'\.\w+$','',self.py['pi_bl']) + '.txt'
                if match and os.path.isfile(probableFile):
                    self.py['flavour'] = match.groups()[0]
                    self.py['root_datadir'] = probableFile
                    self.py['blog_title'] += ' : %s' % re.sub(r'/[^/]+\.\w+$','',self.py['pi_bl'])
                    self.py['bl_type'] = 'file'
                else:
                    self.py['pi_bl'] = ''
                    self.py['bl_type'] = 'dir'

        # Get our URL
        if os.environ.has_key('SCRIPT_NAME'):
            self.py['url'] = 'http://%s%s%s' % (os.environ['HTTP_HOST'], os.environ['SCRIPT_NAME'], self.py['pi_bl'])
            self.py['base_url'] = 'http://%s%s' % (os.environ['HTTP_HOST'], os.environ['SCRIPT_NAME'])

        # Python is unforgiving as perl in this case
        self.py['pi_yr'] = (len(path_info) > 0 and path_info.pop(0) or '')
        self.py['pi_mo'] = (len(path_info) > 0 and path_info.pop(0) or '')
        self.py['pi_da'] = (len(path_info) > 0 and path_info.pop(0) or '')


    def getFlavour(self, taste = 'html'):
        """
        Flavours, or views, or templates, as some may call it, defaults are
        given, but can be overidden with files on the datadir. Don't like the
        default html templates, add your own, head.html, story.html etc.
        """
        # Ugly default templates, have to though :(
        html = {'content_type' : 'text/html',
                'head' : """<html><head><link rel="alternate" type="application/rss+xml" title="RSS" href="$url/?flav=rss" /><title>$blog_title $pi_da $pi_mo $pi_yr</title></head><body><center><font size="+3">$blog_title</font><br />$pi_da $pi_mo $pi_yr</center><p />""",
                'date_head' : '<div class="blosxomDayDiv">\n<span class="blosxomDate">$date</span>',
                'story' : """<p><a name="$fn"><b>$title</b></a><br />$body<br /><br />posted at: $ti | path: <a href="$url/$path">/$path</a> | <a href="$base_url/$file_path.$flavour">permanent link to this entry</a></p>\n""",
                'date_foot' : '</div>',
                'foot' : """<p /><center><a href="http://roughingit.subtlehints.net/pyblosxom/weblogs/tools/pyblosxom/#pyblosxom_0+5i"><img src="http://roughingit.subtlehints.net/images/pb_pyblosxom.gif" border="0" /></body></html>"""}
        rss = {'content_type' : 'text/xml',
               'head' : """<?xml version="1.0"?>\n<!-- name="generator" content="pyblosxom/0+5i" -->\n<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n\n<rss version="0.91">\n  <channel>\n    <title>$blog_title $pi_da $pi_mo $pi_yr</title>\n    <link>$url</link>\n    <description>$blog_description</description>\n    <language>$blog_language</language>\n""",
               'story' : """<item>\n    <title>$title</title>\n    <link>$base_url/$file_path.html</link>\n    <description>$body</description>\n  </item>\n""",
               'foot' : '   </channel>\n</rss>'}
        rss3 = {'content_type' : 'text/plain',
                'head' : """title: $blog_title\ndescription: $blog_description\nlink: $url\ncreator: wari@wari.per.sg Wari Wahab\nerrorsTo: wari@wari.per.sg Wari Wahab\nlang: $blog_language\n\n""",
                'story' :  """title: $title\nlink: $base_url/$file_path.html\ncreated: $w3cdate\nsubject: $path\nguid: $file_path\n""",
                'foot' : ''}
        esf = {'content_type' : 'text/plain',
                'head' : """title: $blog_title\ncontact: contact@example.com (The Contact Person)\nlink: $url\n\n""",
                'story' :  """$mtime\t$title\t$base_url/$file_path""",
                'foot' : ''}
        error = {'content_type' : 'text/plain',
                 'head' : """ Error: I'm afraid this is the first I've heard of a "$flavour" flavoured pyblosxom.\n Try dropping the "?flav=$flavour" bit from the end of the URL.\n\n"""}
        flavours = {'html' : html, 'rss' : rss, 'error' : error, 'rss3' : rss3, 'esf' : esf}
        # End of ugly portion! Yucks :)
        # Look for flavours in datadir

        pattern = re.compile(r'(content_type|head|date_head|date_foot|foot|story)\.' + taste)
        flavourlist = tools.Walk(self.py['root_datadir'], 1, pattern)
        if not flavourlist:
            flavourlist = tools.Walk(self.py['datadir'], 1, pattern)

        for filename in flavourlist:
            flavouring = os.path.basename(filename).split('.')
            if flavours.has_key(flavouring[1]):
                flavours[flavouring[1]][flavouring[0]] = file(filename).read().strip()
            else:
                flavours[flavouring[1]] = { flavouring[0] : file(filename).read().strip() }

        if not flavours.has_key(taste):
            taste = 'error'
        return flavours[taste]

    def getProperties(self, filename, root):
        """Returns a dictionary of file related contents"""
        mtime = os.stat(filename)[8]
        timetuple = time.localtime(mtime)
        path = string.replace(filename, root, '')
        path = string.replace(path, os.path.basename(filename), '')
        path = path[1:][:-1]
        absolute_path = string.replace(filename, self.py['datadir'], '')
        absolute_path = string.replace(absolute_path, os.path.basename(filename), '')
        absolute_path = absolute_path[1:][:-1]
        fn = re.sub(r'\.txt$', '', os.path.basename(filename))
        tb = '-'
        tb_id = '%s/%s' % (absolute_path, fn)
        tb_id = re.sub(r'[^A-Za-z0-9]', '_', tb_id)
        if os.path.isfile('%s/%s.stor' % (self.py['tb_data'], tb_id)):
            tb = '+'

        return {'mtime' : mtime, 
                'path' : path,
                'tb' : tb,
                'tb_id' : tb_id,
                'absolute_path' : absolute_path,
                'file_path' : absolute_path + '/' + fn,
                'fn' : fn,
                'filename' : filename,
                'ti' : time.strftime('%H:%M',timetuple),
                'mo' : time.strftime('%b',timetuple),
                'mo_num' : time.strftime('%m',timetuple),
                'da' : time.strftime('%d',timetuple),
                'yr' : time.strftime('%Y',timetuple),
                'timetuple' : timetuple,
                'fulltime' : time.strftime('%Y%m%d%H%M%S',timetuple),
                'w3cdate' : time.strftime('%Y-%m-%dT%H:%M:%S%Z',timetuple), # YYYY-MM-DDThh:mm:ssTZD
                'date' : time.strftime('%a, %d %b %Y',timetuple)}


    def processEntry(self, filename, current_date):
        """Main workhorse of pyblosxom stories, comments and other miscelany goes
        here"""

        def printTemplate(text, template):
            if template != '':
                print tools.parse(text, template)

        entryData = {}
        try:
            story = file(filename).readlines()
        except:
            return current_date
        cachedFile = filename + self.py['cache_ext']
        if os.path.isfile(cachedFile) and os.stat(cachedFile)[8] >= self.py['mtime']:
            cached = 1
            try:
                fp = file(cachedFile, 'rb')
                entryData = pickle.load(fp)
                fp.close()
            except:
                cached = 0
        else:
            cached = 0

        if not cached:
            if len(story) > 0:
                entryData['title'] = story.pop(0).strip()

            while len(story) > 0:
                match = re.match(r'^#(\w+)\s+(.*)', story[0])
                if match:
                    story.pop(0)
                    entryData[match.groups()[0]] = match.groups()[1].strip()
                else:
                    break
                    
            if entryData.has_key('parser'):
                preformatter = tools.importName('libs.preformatters', entryData['parser'])
                if preformatter:
                    entryData['body'] = preformatter.PreFormatter(story).parse()
                else:
                    entryData['body'] = ''.join(story)
            else:
                preformatter = tools.importName('libs.preformatters', self.py['parser'])
                if preformatter:
                    entryData['body'] = preformatter.PreFormatter(story).parse()
                else:
                    entryData['body'] = ''.join(story)
            
            if int(self.py['cache_enable']):
                try:
                    fp = file(cachedFile, 'w+b')
                    pickle.dump(entryData, fp, 1)
                    fp.close()
                except:
                    # Somehow we cannot create a cache file
                    pass

        if self.py['content-type'] == 'text/xml':
            entryData['body'] = cgi.escape(entryData['body'])
        elif self.py['content-type'] == 'text/plain':
            s = tools.Stripper()
            s.feed(entryData['body'])
            s.close()
            p = ['  ' + line for line in s.gettext().split('\n')]
            entryData['body'] = '\n'.join(p)
            
        entryData.update(self.py)
        if self.py['date'] != current_date:
            current_date = self.py['date']
            if not self.dayFlag:
                printTemplate(entryData, self.flavour.get('date_foot' ,''))
            self.dayFlag = 0
            printTemplate(entryData, self.flavour.get('date_head' ,''))
        printTemplate(entryData, self.flavour.get('story' ,''))
        return current_date


    def run(self):
        """Main loop for pyblosxom"""
        filelist = (self.py['bl_type'] == 'dir' and tools.Walk(self.py['root_datadir'], int(self.py['depth'])) or [self.py['root_datadir']])
        dataList = []
        for ourfile in filelist:
            dataList.append(self.getProperties(ourfile, self.py['root_datadir']))
        dataList = tools.sortDictBy(dataList,"mtime")
        
        # Match dates with files if applicable
        if not self.py['pi_yr'] == '':
            month = (self.py['pi_mo'] in tools.month2num.keys() and tools.month2num[self.py['pi_mo']] or self.py['pi_mo'])
            valid_list = ([x for x in dataList
                       if re.match('^' + self.py['pi_yr'] + month + self.py['pi_da'], x['fulltime'])])
        else:
            valid_list = dataList

        # Generate our own 404 Error
        if not valid_list:
            print 'Status: 404 Not Found'
            print 'Content-Type: text/html\n'
            print 'The page you are looking for is not available:'
            print 'Back to <a href="%(base_url)s">%(blog_title)s</a>' % self.py
            sys.exit()
    
        if self.py['conditionalHTTP'] == 'yes':
            # Get our first file timestamp for ETag and Last Modified
            # Last-Modified: Wed, 20 Nov 2002 10:08:12 GMT
            # ETag: "2bdc4-7b5-3ddb5f0c"
            lastModed = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(valid_list[0]['mtime']))
            if ((os.environ.get('HTTP_IF_NONE_MATCH','') == '"%s"' % valid_list[0]['mtime']) or
                (os.environ.get('HTTP_IF_NONE_MATCH','') == '%s' % valid_list[0]['mtime']) or
                (os.environ.get('HTTP_IF_MODIFIED_SINCE','') == lastModed)):
                print 'Status: 304 Not Modified\nETag: "%s"\nLast-Modified: %s' % (
                        valid_list[0]['mtime'], lastModed)
                # Enable if you want logging
                #tools.logRequest(returnCode = '304')
                import sys
                sys.exit()
            print 'ETag: "%s"' % valid_list[0]['mtime']
            print 'Last-Modified: %s' % lastModed

        self.flavour = self.getFlavour(self.py['flavour'])
        self.py['content-type'] = self.flavour['content_type'].strip()
        print 'Content-type: %s\n' % self.flavour['content_type']
        if self.flavour.has_key('head'): print tools.parse(self.py, self.flavour['head'])
        if self.flavour.has_key('story'):
            # Body stuff
            current_date = ''
            count = 1
            for entry in valid_list:
                self.py.update(entry)
                current_date = self.processEntry(entry['filename'], current_date)
                if self.py['pi_yr'] == '' and count >= int(self.py['num_entries']):
                    break
                count += 1
        
        if self.flavour.has_key('date_foot'): print tools.parse(self.py, self.flavour['date_foot'])
        # Archive list plugin
        from libs.plugins import pyarchives
        self.py['archivelinks'] = pyarchives.genLinearArchive(self.py['datadir'], self.py.get('base_url',''))
        if self.flavour.has_key('foot'): print tools.parse(self.py, self.flavour['foot'])
        
        # Enable if you want logging
        #tools.logRequest()
