import _path_pyblosxom

import os
import os.path
import shutil
import tempfile
import StringIO

from Pyblosxom.pyblosxom import Request
from Pyblosxom import tools

class UnitTestBase:
    _tempdir = tempfile.mkdtemp()

    def _gettempdir(self):
        return UnitTestBase._tempdir

    def _setup(self, files):
        # sort so that we're building the directories in order
        files.sort()

        os.makedirs(os.path.join(self._gettempdir(), "entries"))

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
        shutil.rmtree(self._gettempdir())

    def _buildfileset(self, filelist):
        return [ os.path.join(self._gettempdir(), "entries/%s" % fn) for fn in filelist ]

    def _build_request(self, cfg=None, http=None, data=None, inputstream=""):
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
                    "datadir": os.path.join(self._gettempdir(), "entries"),
                    "blog_title": "Joe's blog",
                    "base_url": "http://www.example.com/" }
        if cfg: _config.update(cfg)

        _data = { "extensions": { "txt": 0 } }
        if data: _data.update(data)

        _http = { "wsgi.input": StringIO.StringIO(inputstream),
                  "REQUEST_METHOD": len(inputstream) and "GET" or "POST",
                  "CONTENT_LENGTH": len(inputstream) }
        if http: _http.update(http)

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
            if mem in actual:
                assert expected[mem] == actual[mem]
            else:
                assert False


