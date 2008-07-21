import _path_pyblosxom

from nose.tools import eq_
from Pyblosxom.pyblosxom import Request

class TestRequest:
    """Need to be backwards compatible with pre-existing methods of getting
    config, data and http dicts from the Request object.
    """
    def test_conf(self):
        r = Request({}, {}, {})

        conf = r.getConfiguration()

        for mem in (r.conf, r.config, r.configuration):
            yield eq_, mem, conf

    def test_http(self):
        r = Request({}, {}, {})

        eq_(r.http, r.getHttp())

    def test_data(self):
        r = Request({}, {}, {})

        eq_(r.data, r.getData())
