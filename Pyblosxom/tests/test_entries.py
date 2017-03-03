#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2010-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################

from os import environ
import time

from Pyblosxom.tests import req_, UnitTestBase

from Pyblosxom.tools import STANDARD_FILTERS
from Pyblosxom.entries.base import EntryBase, generate_entry

TIME1 = (2008, 7, 21, 12, 51, 47, 0, 203, 1)

class TestEntryBase(UnitTestBase):
    def test_data(self):
        e = EntryBase(req_())
        self.eq_(e.get_data(), "")

        s1 = "la la la la la"
        e.set_data(s1)
        self.eq_(e.get_data(), s1)
        self.eq_(type(e.get_data()), str)

        s2 = "foo foo foo foo foo"
        e.set_data(s2)
        self.eq_(e.get_data(), s2)
        self.eq_(type(e.get_data()), str)

        s3 = "foo bar"
        e.set_data(s3)
        self.eq_(e.get_data(), s3)

    def test_metadata(self):
        e = EntryBase(req_())
        self.eq_(e.get_metadata_keys(), list(STANDARD_FILTERS.keys()))
        self.eq_(e.get_metadata("foo"), None)
        self.eq_(e.get_metadata("foo", "bar"), "bar")
        e.set_metadata("foo", "bar")
        self.eq_(e.get_metadata("foo"), "bar")

    def test_time(self):
        e = EntryBase(req_())
        # set_time takes local time, and results depend on time zone.
        self.__force_tz()
        e.set_time(TIME1)
        self.__restore_tz()
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
            self.eq_(e[mem[0]], mem[1], \
                  "%s != %s (note: this is a time zone dependent test)" % (mem[0], mem[1]))

    def test_dictlike(self):
        e = EntryBase(req_())
        e["foo"] = "bar"
        e["body"] = "entry body"

        def sortlist(l):
            l.sort()
            return l

        self.eq_(sortlist(list(e.keys())), sortlist(list(STANDARD_FILTERS.keys()) + ["foo", "body"]))

        self.eq_(e["foo"], "bar")
        self.eq_(e.get("foo"), "bar")
        self.eq_(e.get("foo", "fickle"), "bar")
        self.eq_(e.get_metadata("foo"), "bar")
        self.eq_(e.get_metadata("foo", "fickle"), "bar")

        self.eq_(e["body"], "entry body", "e[\"body\"]")
        self.eq_(e.get("body"), "entry body", "e.get(\"body\")")
        self.eq_(e.getData(), "entry body", "e.getData()")

        self.eq_(e.get("missing_key", "default"), "default")
        self.eq_(e.get("missing_key"), None)

        # e.set("faz", "baz")
        # yield eq_, e.get("faz"), "baz"

        self.eq_(e.has_key("foo"), True)
        self.eq_(e.has_key("foo2"), False)
        self.eq_(e.has_key("body"), True)

        # FIXME - EntryBase doesn't support "in" operator.
        # self.eq_("foo" in e, True)
        # self.eq_("foo2" in e, False)
        # self.eq_("foo2" not in e, True)
        # self.eq_("body" in e, True)

        e.update({"foo": "bah", "faux": "pearls"})
        self.eq_(e["foo"], "bah")
        self.eq_(e["faux"], "pearls")

        e.update({"body": "new body data"})
        self.eq_(e["body"], "new body data")
        self.eq_(e.get_data(), "new body data")

        # del e["foo"]
        # yield eq_, e.get("foo"), None

    # @raises(KeyError)
    # def test_delitem_keyerror(self):
    #     e = EntryBase(req_())
    #     del e["missing_key"]

    # @raises(ValueError)
    # def test_delitem_valueerror(self):
    #     e = EntryBase(req_())
    #     del e["body"]

    def test_generate_entry(self):
        # generate_entry takes local time, and we test the resulting
        # rfc822date which is UTC.  Result depends on time zone.
        self.__force_tz()
        e = generate_entry(req_(), {"foo": "bar"}, "entry body", TIME1)
        self.__restore_tz()

        self.eq_(e["foo"], "bar")
        self.eq_(e["body"], "entry body")
        self.eq_(e["rfc822date"], "Mon, 21 Jul 2008 16:51 GMT")

        e = generate_entry(req_(), {"foo": "bar"}, "entry body")

    def test_repr(self):
        # it doesn't really matter what __repr__ sends back--it's only used
        # for logging/debugging.  so this test adds coverage for that line to
        # make sure it doesn't error out.
        e = EntryBase(req_())
        repr(e)

    def __force_tz(self):
        """
        Force time zone to 'US/Eastern'.

        Some of the above tests are time zone dependent.
        """
        self.__tz = environ.get('TZ')
        environ['TZ'] = 'US/Eastern'
        time.tzset()
    
    def __restore_tz(self):
        """
        Restore time zone to what it was before __force_tz() call.
        """
        if self.__tz:
            environ['TZ'] = self.__tz
            self.__tz = None
        else:
            del environ['TZ']
        time.tzset()
