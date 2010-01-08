import os
import os.path
import shutil
import tempfile
import StringIO
import unittest

from Pyblosxom.pyblosxom import Request
from Pyblosxom import tools

def req_():
    return Request({}, {}, {})

class UnitTestBase(unittest.TestCase):
    def setUp(self):
        self._tempdir = None

    def tearDown(self):
        if self._tempdir:
            try:
                shutil.rmtree(self._tempdir)
            except OSError:
                pass

    def eq_(self, a, b, text=None):
        self.assertEquals(a, b, text)

    def get_temp_dir(self):
        if self._tempdir == None:
            self._tempdir = tempfile.mkdtemp()
        return self._tempdir

    def setup_files(self, files):
        # sort so that we're building the directories in order
        files.sort()

        tempdir = self.get_temp_dir()
        os.makedirs(os.path.join(tempdir, "entries"))

        for fn in files:
            d, f = os.path.split(fn)

            try:
                os.makedirs(d)
            except OSError, e:
                pass

            if f:
                f = open(fn, "w")
                f.write("test file: %s\n" % fn)
                f.close()
            
    def build_file_set(self, filelist):
        return [os.path.join(self.get_temp_dir(), "entries/%s" % fn)
                for fn in filelist]

    def build_request(self, cfg=None, http=None, data=None, inputstream=""):
        """
        process_path_info uses:
        - req.pyhttp["PATH_INFO"]         - string

        - req.config["default_flavour"]   - string
        - req.config["datadir"]           - string
        - req.config["blog_title"]        - string
        - req.config["base_url"]          - string

        - req.data["extensions"]          - dict of string -> func

        if using req.getForm():
        - req.pyhttp["wsgi.input"]        - StringIO instance
        - req.pyhttp["REQUEST_METHOD"]    - GET or POST
        - req.pyhttp["CONTENT_LENGTH"]    - integer
        """
        _config = {"default_flavour": "html",
                   "datadir": os.path.join(self.get_temp_dir(), "entries"),
                   "blog_title": "Joe's blog",
                   "base_url": "http://www.example.com/"}
        if cfg:
            _config.update(cfg)

        _data = {"extensions": {"txt": 0}}
        if data:
            _data.update(data)

        _http = {"wsgi.input": StringIO.StringIO(inputstream),
                 "REQUEST_METHOD": len(inputstream) and "GET" or "POST",
                 "CONTENT_LENGTH": len(inputstream)}
        if http: _http.update(http)

        return Request(_config, _http, _data)
        
    def test_setup_teardown(self):
        fileset1 = self.build_file_set(["file.txt",
                                        "cata/file.txt",
                                        "cata/subcatb/file.txt"])

        self.setup_files(fileset1)
        try:
            for mem in fileset1:
                assert os.path.isfile(mem)

        finally:
            self.tearDown()

        for mem in fileset1:
            assert not os.path.isfile(mem)

    def cmpdict(self, expected, actual):
        """expected <= actual
        """
        for mem in expected.keys():
            if mem in actual:
                assert expected[mem] == actual[mem]
            else:
                assert False

