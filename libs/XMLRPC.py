# vim: shiftwidth=4 tabstop=4 expandtab
import xmlrpclib, string, re, sys, os
from libs import tools
from libs.pyblosxom import PyBlosxom


def debug(str):
    file('xmlrpc.debug','a').write('DEBUG: %s\n' % str)

class xmlrpcHandler:

    def __init__(self, py, xmldata, data):
        self.py = py
        self.data = data
        self.xmldata = xmldata

    def process(self):
        # XML-RPC starts here
        try:
            params, method = xmlrpclib.loads(self.data)

            try:
                response = self.xmlrpcCall(method, params)
                if type(response) != type (()):
                    response = (response,)
            except xmlrpclib.Fault, faultobj:
                response = xmlrpclib.dumps(faultobj)
            except:
                response = xmlrpclib.dumps(1,
                    xmlrpclib.Fault(1, '%s:%s' % (sys.exc_type, sys.exc_value)))
            else:
                response = xmlrpclib.dumps(response, methodresponse=1)

        except:
            print 'Content-type: text/plain\n\nXML-RPC call expected\n'
        else:
            print 'Content-type: text/xml\nContent-length: %d\n\n%s\n' % (len(response), response)


    def xmlrpcCall(self, meth_name, args):
        """XML-RPC dispatcher"""
        try:
            func_obj = eval("self.xmlrpc_" + string.replace(meth_name, '.', '_'))
            return apply(func_obj, args)
        except:
            raise xmlrpclib.Fault('MethodError', 'Error Executing Method: %s' % meth_name)
            #raise MethodError, 'Error Executing Method: %s' % meth_name


    # Blogger API methods
    def authenticate(self, username, password):
        if username != self.xmldata['username'] or password != self.xmldata['password']:
            raise xmlrpclib.Fault('PasswordError','Error in username or password')

    def xmlrpc_blogger_newPost(self, appkey, blogid, username, password, content, publish=1):
        self.authenticate(username, password)
        if os.path.isdir(self.py['datadir'] + blogid):
            # Look at content
            blogTitle = content.split('\n')[0].strip()
            tempMarker = (not publish and '-' or '')
            blogID = self.py['datadir'] + blogid + re.sub('[^A-Za-z0-9]','_',blogTitle) + '.txt' + tempMarker
            if os.path.isfile(blogID) or os.path.isfile(blogID + '-'):
                blogID = self.py['datadir'] + blogid + re.sub('[^A-Za-z0-9]','_',blogTitle) + tools.generateRandStr() + '.txt' + tempMarker
            file(blogID, 'w').write(content)
            # Generate BlogID
            return blogID.replace(self.py['datadir'], '')
        else: raise xmlrpclib.Fault('PostError','Blog %s does not exist' % blogid)

    def xmlrpc_blogger_editPost(self, appkey, postid, username, password, content, publish=1):
        self.authenticate(username, password)
        filename = self.py['datadir'] + postid
        if publish and re.search(r'-$', filename):
            switchTo = re.sub(r'-$','',filename)
        elif not publish and re.search(r'txt$', filename):
            switchTo = filename + '-'
        else:
            switchTo = filename
        if os.path.isfile(filename):
            file(switchTo, 'w').write(content)
            if filename != switchTo:
                os.remove(filename)
                if os.path.isfile(filename + self.py['cache_ext']):
                    os.remove(filename + self.py['cache_ext'])
            return xmlrpclib.True
        else:
            raise xmlrpclib.Fault('UpdateError','Post does not exist')

    def xmlrpc_blogger_deletePost(self, appkey, postid, username, password, publish=1):
        # Really want to implement this? hmmm
        self.authenticate(username, password)
        if os.path.isfile(self.py['datadir'] + postid):
            os.remove(self.py['datadir'] + postid)
            if os.path.isfile(self.py['datadir'] + postid + self.py['cache_ext']):
                os.remove(self.py['datadir'] + postid + self.py['cache_ext'])
            return xmlrpclib.True
        else:
            raise xmlrpclib.Fault('DeleteError','Post does not exist')

    def xmlrpc_blogger_getRecentPosts(self, appkey, blogid, username, password, numberOfPosts=5):
        self.authenticate(username, password)
        p = PyBlosxom(self.py, self.xmldata)
        result = []
        dataList = []
        filelist = tools.Walk(self.py['datadir'] + blogid, pattern = re.compile(r'.*\.txt-?$'), recurse = 1)
        for ourfile in filelist:
            dataList.append(p.getProperties(ourfile, self.py['datadir']))
        dataList = tools.sortDictBy(dataList,"mtime")
        
        count = 1
        for entry in dataList:
            self.py.update(entry)
            result.append({'dateCreated' : xmlrpclib.DateTime(self.py['mtime']),
                           'userid' : '01',
                           'postid' : self.py['filename'].replace(self.py['datadir'],''),
                           'content' : file(self.py['filename']).read()})
            if count >= int(numberOfPosts):
                break
            count += 1
        return result

    def xmlrpc_blogger_getUsersBlogs(self, appkey, username, password):
        """Returns trees below datadir"""
        self.authenticate(username, password)
        result = [{'url':self.py['url'] + '/', 'blogid':'/', 'blogName':'/'}]
        for directory in tools.Walk(self.py['datadir'], 0, re.compile(r'.*'), 1):
            blogpath = directory.replace(self.py['datadir'],'') + '/'
            result.append({'url' : self.py['url'] + blogpath, 
                           'blogid' : blogpath, 
                           'blogName':blogpath})
        return result

    def xmlrpc_blogger_getUserInfo(self, appkey, username, password):
        self.authenticate(username, password)
        # Change these values? Not that important unless some apps needs it.
        return {'firstname':'Ficticious',
                'lastname':'User',
                'userid':'01',
                'email':'someuser@example.com',
                'nickname':'pyblosxom',
                'url':self.py['url']}

    def xmlrpc_pingback_ping(self, sourceURI, targetURI):
        """pyblosxom pingback implemetation, see
        http://www.hixie.ch/specs/pingback/pingback-1.0 for details"""
        # TODO in this method.
        # target is me
        # source is THEM (return 16 if invalid, else 17 if does not contain target
        # string)
        # 1. Check if the target link is available (33 if error)
        # 2. MAY attempt to see if source is valid
        # 3. Check if pingbacks already exists, yes? return 48
        # 4. else record the pingback
        # 5. return a string containing anything, else return errors.
        postid = string.replace(self.py['base_url'], '', targetURI)
        postfile = self.py['datadir'] + postid
        postpingfile = self.py['datadir'] + postid + '.pingback'
        pingbackdata = []
        if os.path.isfile(postfile):
            if os.path.isfile(postpingfile):
                pingbackdata = marshal.loads(file(postpingfile).read())
            if len(pingbackdata) and sourceURI in pingbackdata[0]:
                raise xmlrpclib.Fault(48,"sourceURI exists")
        else:
            raise xmlrpclib.Fault(33,"targetURI not found")

    def xmlrpc_mt_getTrackbackPings(self, postid):
        pass

