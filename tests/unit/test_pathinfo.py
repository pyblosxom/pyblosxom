import _path_pyblosxom

import os
import os.path
import shutil
import tempfile
import StringIO

from Pyblosxom.pyblosxom import Request, blosxom_process_path_info
from Pyblosxom import tools

class Testpathinfo:
    """pyblosxom.blosxom_process_path_info

    This tests default parsing of the path.
    """

    _tempdir = tempfile.mkdtemp()

    def _setup(self, files):
        # sort so that we're building the directories in order
        files.sort()

        os.makedirs(os.path.join(Testpathinfo._tempdir, "entries"))

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
            
    def _teardown(self):
        shutil.rmtree(Testpathinfo._tempdir)

    def _buildfileset(self, filelist):
        return [ os.path.join(Testpathinfo._tempdir, "entries/%s" % fn) for fn in filelist ]

    def _build_request(self, cfg={}, http={}, data={}, inputstream=""):
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
        _config = { "default_flavour": "html", 
                    "datadir": os.path.join(Testpathinfo._tempdir, "entries"),
                    "blog_title": "Joe's blog",
                    "base_url": "http://www.example.com/" }
        _config.update(cfg)

        _data = { "extensions": { "txt": 0 } }
        _data.update(data)

        _http = { "wsgi.input": StringIO.StringIO(inputstream),
                  "REQUEST_METHOD": len(inputstream) and "GET" or "POST",
                  "CONTENT_LENGTH": len(inputstream) }
        _http.update(http)

        return Request(_config, _http, _data)
        
    def test_setup_teardown(self):
        fileset1 = self._buildfileset( [ "file.txt",
                                         "cata/file.txt",
                                         "cata/subcatb/file.txt" ] )

        self._setup(fileset1)
        try:
            for mem in fileset1:
                assert os.path.isfile( mem )

        finally:
            self._teardown()

        for mem in fileset1:
            assert not os.path.isfile( mem )

    def cmpdict(self, expected, actual):
        for mem in expected.keys():
            assert expected[mem] == actual[mem]

    def _basic_test(self, pathinfo, expected):
        req = self._build_request(http={ "PATH_INFO": pathinfo })
        blosxom_process_path_info(args={"request": req})
        print repr(expected), repr(req.data)
        self.cmpdict( expected, req.data )
 
    def test_root(self):
        entries = self._buildfileset( [ ] )

        self._setup(entries)
        try:
            # /
            self._basic_test( "/",
                              { "bl_type": "dir",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /index
            self._basic_test( "/index", 
                              { "bl_type": "dir",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /index.xml
            self._basic_test( "/index.xml", 
                              { "bl_type": "dir",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "xml" } )
        finally:
            self._teardown()

    def test_files(self):
        entries = self._buildfileset( [ "file1.txt", "cata/file2.txt", "catb/file3.txt" ] )

        self._setup(entries)
        try:
            # /file1
            self._basic_test( "/file1", 
                              { "bl_type": "file",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /cata/file2
            self._basic_test( "/cata/file2", 
                              { "bl_type": "file",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
        finally:
            self._teardown()

    def test_categories(self):
        entries = self._buildfileset( [ "cata/entry1.txt", "cata/suba/entry1.txt", "catb/entry1.txt" ])

        self._setup(entries)
        try:
            # /cata
            self._basic_test( "/cata", 
                              { "bl_type": "dir",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /cata/
            self._basic_test( "/cata/", 
                              { "bl_type": "dir",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /cata/suba
            self._basic_test( "/cata/suba", 
                              { "bl_type": "dir",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /cata/suba
            self._basic_test( "/cata/suba/entry1.html", 
                              { "bl_type": "file",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
        finally:
            self._teardown()

    def test_dates(self):
        tools.initialize( {} )

        self._basic_test( "/2002",
                          { "bl_type": "dir",
                            "pi_yr": "2002", "pi_mo": "", "pi_da": "",
                            "flavour": "html" } )
        self._basic_test( "/2002/02",
                          { "bl_type": "dir",
                            "pi_yr": "2002", "pi_mo": "02", "pi_da": "",
                            "flavour": "html" } )
        self._basic_test( "/2002/02/04", 
                          { "bl_type": "dir",
                            "pi_yr": "2002", "pi_mo": "02", "pi_da": "04",
                            "flavour": "html" } )

    def test_categories_and_dates(self):
        tools.initialize( {} )
        entries = self._buildfileset( [ "cata/entry1.txt", "cata/suba/entry1.txt", "catb/entry1.txt" ])

        self._setup(entries)
        try:
            # /2006/cata/
            self._basic_test( "/2006/cata/", 
                              { "bl_type": "dir",
                                "pi_yr": "2006", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /2006/04/cata/
            self._basic_test( "/2006/04/cata/", 
                              { "bl_type": "dir",
                                "pi_yr": "2006", "pi_mo": "04", "pi_da": "",
                                "flavour": "html" } )
            # /2006/04/02/cata/
            self._basic_test( "/2006/04/02/cata/", 
                              { "bl_type": "dir",
                                "pi_yr": "2006", "pi_mo": "04", "pi_da": "02",
                                "flavour": "html" } )
            # /2006/04/02/cata/suba/
            self._basic_test( "/2006/04/02/cata/suba/", 
                              { "bl_type": "dir",
                                "pi_yr": "2006", "pi_mo": "04", "pi_da": "02",
                                "flavour": "html" } )

        finally:
            self._teardown()

    def test_date_categories(self):
        tools.initialize( {} )
        entries = self._buildfileset( [ "2007/entry1.txt", "2007/05/entry3.txt", "cata/entry2.txt" ] )

        self._setup(entries)
        try:
            # /2007/              2007 here is a category
            self._basic_test( "/2007/",
                              { "bl_type": "dir",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /2007/05            2007/05 here is a category
            self._basic_test( "/2007/05",
                              { "bl_type": "dir",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )
            # /2007/05/entry3     2007/05/entry3 is a file
            self._basic_test( "/2007/05/entry3.html",
                              { "bl_type": "file",
                                "pi_yr": "", "pi_mo": "", "pi_da": "",
                                "flavour": "html" } )

        finally:
            self._teardown()
