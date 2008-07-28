import _path_pyblosxom
import time
from StringIO import StringIO

from nose.tools import eq_, raises

from Pyblosxom.tools import STANDARD_FILTERS
from Pyblosxom.pyblosxom import Request
from Pyblosxom.entries.base import EntryBase, generate_entry

from helpers import req_

TIME1 = (2008, 7, 21, 12, 51, 47, 0, 203, 1)

class TestEntryBase:
    def test_data(self):
        e = EntryBase(req_())
        yield eq_, e.getData(), ""

        s1 = "la la la la la"
        e.setData(s1)
        yield eq_, e.getData(), s1
        yield eq_, type(e.getData()), str

        s2 = u"foo foo foo foo foo"
        e.setData(s2)
        yield eq_, e.getData(), s2
        yield eq_, type(e.getData()), str

        s3 = "foo bar"
        e.setData(StringIO(s3))
        yield eq_, e.getData(), s3

    def test_metadata(self):
        e = EntryBase(req_())
        yield eq_, e.getMetadataKeys(), STANDARD_FILTERS.keys()
        yield eq_, e.getMetadata("foo"), None
        yield eq_, e.getMetadata("foo", "bar"), "bar"
        e.setMetadata("foo", "bar")
        yield eq_, e.getMetadata("foo"), "bar"

    def test_time(self):
        # FIXME - these tests are locale dependent
        e = EntryBase(req_())
        e.setTime(TIME1)
        for mem in (("timetuple", TIME1),
                    ("mtime", 1216659107.0),
                    ("ti", "12:51"),
                    ("mo", "Jul"),
                    ("mo_num", "07"),
                    ("da", "21"),
                    ("dw", "Monday"),
                    ("yr", "2008"),
                    ("fulltime", "20080721125147"),
                    ("date", "Mon, 21 Jul 2008"),
                    ("w3cdate", "2008-07-21T16:51:47Z"),
                    ("rfc822date", "Mon, 21 Jul 2008 16:51 GMT")):
            yield eq_, e[mem[0]], mem[1]

    def test_dictlike(self):
        e = EntryBase(req_())
        e["foo"] = "bar"
        e["body"] = "entry body"

        def sortlist(l):
            l.sort()
            return l

        yield eq_, sortlist(e.keys()), sortlist(STANDARD_FILTERS.keys() + ["foo", "body"])

        yield eq_, e["foo"], "bar"
        yield eq_, e.get("foo"), "bar"
        yield eq_, e.get("foo", "fickle"), "bar"
        yield eq_, e.getMetadata("foo"), "bar"
        yield eq_, e.getMetadata("foo", "fickle"), "bar"

        yield eq_, e["body"], "entry body", "e[\"body\"]"
        yield eq_, e.get("body"), "entry body", "e.get(\"body\")"
        yield eq_, e.getData(), "entry body", "e.getData()"

        yield eq_, e.get("missing_key", "default"), "default"
        yield eq_, e.get("missing_key"), None

        e.set("faz", "baz")
        yield eq_, e.get("faz"), "baz"

        yield eq_, e.has_key("foo"), True
        yield eq_, e.has_key("foo2"), False
        yield eq_, e.has_key("body"), True
        yield eq_, "foo" in e, True
        yield eq_, "foo2" in e, False
        yield eq_, "foo2" not in e, True
        yield eq_, "body" in e, True

        e.update({"foo": "bah", "faux": "pearls"})
        yield eq_, e["foo"], "bah"
        yield eq_, e["faux"], "pearls"

        e.update({"body": "new body data"})
        yield eq_, e["body"], "new body data"
        yield eq_, e.getData(), "new body data"

        del e["foo"]
        yield eq_, e.get("foo"), None


    @raises(KeyError)
    def test_delitem_keyerror(self):
        e = EntryBase(req_())
        del e["missing_key"]

    @raises(ValueError)
    def test_delitem_valueerror(self):
        e = EntryBase(req_())
        del e["body"]


    def test_generate_entry(self):
        e = generate_entry(req_(), {"foo": "bar"}, "entry body", TIME1)

        yield eq_, e["foo"], "bar"
        yield eq_, e["body"], "entry body"
        yield eq_, e["rfc822date"], "Mon, 21 Jul 2008 16:51 GMT"

        e = generate_entry(req_(), {"foo": "bar"}, "entry body")

    def test_repr(self):
        # it doesn't really matter what __repr__ sends back--it's only used
        # for logging/debugging.  so this test adds coverage for that line to
        # make sure it doesn't error out.
        e = EntryBase(req_())
        repr(e)
