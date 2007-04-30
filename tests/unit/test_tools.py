import _path_pyblosxom

import string
from Pyblosxom import tools

class Testis_year:
    """tools.is_year"""

    def test_must_be_four_digits(self):
        assert tools.is_year("abab") == 0
        assert tools.is_year("ab") == 0
        assert tools.is_year("199") == 0
        assert tools.is_year("19999") == 0
        assert tools.is_year("1997") == 1
        assert tools.is_year("2097") == 1

    def test_must_start_with_19_or_20(self):
        assert tools.is_year("3090") == 0
        assert tools.is_year("0101") == 0
        
    def test_everything_else_returns_false(self):
        assert tools.is_year(None) == 0
        assert tools.is_year("") == 0
        assert tools.is_year("ab") == 0
        assert tools.is_year("97") == 0



class TestgenerateRandStr():
    """tools.generateRandStr

    Note: This is a mediocre test because generateRandStr produces
    a string that's of random length and random content.
    It's possible for this test to pass even when the code is bad.
    """

    def _gen_checker(self, s, minlen, maxlen):
        assert len(s) >= minlen and len(s) <= maxlen
        for c in s:
            assert c in string.letters or c in string.digits

    def test_generates_a_random_string(self):
        self._gen_checker(tools.generateRandStr(), 5, 10)
        self._gen_checker(tools.generateRandStr(), 5, 10)
        self._gen_checker(tools.generateRandStr(), 5, 10)
        self._gen_checker(tools.generateRandStr(), 5, 10)
        self._gen_checker(tools.generateRandStr(), 5, 10)

    def test_generates_a_random_string_between_minlen_and_maxlen(self):
        self._gen_checker(tools.generateRandStr(4, 10), 4, 10)
        self._gen_checker(tools.generateRandStr(4, 10), 4, 10)
        self._gen_checker(tools.generateRandStr(4, 10), 4, 10)
        self._gen_checker(tools.generateRandStr(4, 10), 4, 10)
        self._gen_checker(tools.generateRandStr(4, 10), 4, 10)
        self._gen_checker(tools.generateRandStr(3, 12), 3, 12)
        self._gen_checker(tools.generateRandStr(3, 12), 3, 12)
        self._gen_checker(tools.generateRandStr(3, 12), 3, 12)
        self._gen_checker(tools.generateRandStr(3, 12), 3, 12)
        self._gen_checker(tools.generateRandStr(3, 12), 3, 12)

class TestEscapeText():
    """tools.escape_text"""
    def test_single_quote_to_pos(self):
        assert tools.escape_text("a'b") == "a&apos;b"

    def test_double_quote_to_quot(self):
        assert tools.escape_text("a\"b") == "a&quot;b"

    def test_everything_else_unchanged(self):
        assert tools.escape_text(None) == None
        assert tools.escape_text("") == ""
        assert tools.escape_text("abc") == "abc"

class TestUrlencodeText():
    """tools.urlencode_text"""
    def test_equals_to_3D(self):
        assert tools.urlencode_text("a=c") == "a%3Dc"

    def test_ampersand_to_26(self):
        assert tools.urlencode_text("a&c") == "a%26c"

    def test_space_to_20(self):
        assert tools.urlencode_text("a c") == "a%20c"

    def test_everything_else_unchanged(self):
        assert tools.urlencode_text(None) == None
        assert tools.urlencode_text("") == ""
        assert tools.urlencode_text("abc") == "abc"

class TestVariableDict():
    """tools.VariableDict"""

    def __init__(self):
        self.vd = tools.VariableDict()
        self.vd.update( { "a": "b", \
                          "title": "This is my story", \
                          "title2": "Story: \"aha!\"", \
                          "filename": "joe.txt" } )

    def _compare_unordered_lists(self, lista, listb):
        assert len(lista) == len(listb)

        lista.sort()
        listb.sort()

        for mem in lista:
            print "comparing '" + mem + "' and '" + listb[0] + "'"
            assert mem == listb[0]
            listb.pop(0)

        assert len(listb) == 0

    def test_extends_dicts(self):
        assert self.vd.get("a") == "b"
        assert self.vd.get("title") == "This is my story"
        assert self.vd.get("title2") == "Story: \"aha!\""
        assert self.vd.get("badkey", "novalue") == "novalue"
        
        self._compare_unordered_lists(self.vd.keys(),
                                      ["a", "title", "title2", "filename"])
        self._compare_unordered_lists(self.vd.values(),
                                      ["b", "This is my story",
                                       "Story: \"aha!\"", "joe.txt"])

    def test_can_escape_value(self):
        assert self.vd.get("a_escaped") == "b"
        assert self.vd.get("title_escaped") == "This is my story"
        assert self.vd.get("title2_escaped") == "Story: &quot;aha!&quot;"
        assert self.vd.get("badkey_escaped", "novalue") == "novalue"
        assert self.vd.get("badkey_escaped", "no value") == "no value"

    def test_can_urlencode_value(self):
        assert self.vd.get("a_urlencoded") == "b"
        assert self.vd.get("title_urlencoded") == "This%20is%20my%20story"
        assert self.vd.get("title2_urlencoded") == "Story%3A%20%22aha%21%22"
        assert self.vd.get("badkey_urlencoded", "novalue") == "novalue"
        assert self.vd.get("badkey_urlencoded", "no value") == "no%20value"

