from tests.helpers import UnitTestBase
from Pyblosxom.pyblosxom import Request

class TestRequest(UnitTestBase):
    """Need to be backwards compatible with pre-existing methods of
    getting config, data and http dicts from the Request object.
    """
    def test_conf(self):
        r = Request({"foo": "bar"}, {}, {})

        conf = r.get_configuration()

        for mem in (r.conf, r.config, r.configuration):
            yield self.eq_, mem, conf

    def test_http(self):
        r = Request({}, {"foo": "bar"}, {})

        self.eq_(r.http, r.get_http())

    def test_data(self):
        r = Request({}, {}, {"foo": "bar"})

        self.eq_(r.data, r.get_data())
