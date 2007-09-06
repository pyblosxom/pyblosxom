import _path_pyblosxom

import string
import os
import os.path
from Pyblosxom import tools

class TestVAR_REGEXP:
    """tools.VAR_REGEXP

    This tests the various syntaxes for variables in PyBlosxom templates.
    """
    def _get_match(self, compiled_regexp, s):
        r = compiled_regexp.search(s)
        print repr(r)
        return r and r.group(1)

    def test_escaped_variables(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, "\\$test") == None
        # FIXME - this is bad behavior
        assert self._get_match(VR, "\\\\$test") == None

    def test_dollar_then_string(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, "$test") == "test"
        assert self._get_match(VR, "$test-test") == "test-test"
        assert self._get_match(VR, "$test_test") == "test_test"
        assert self._get_match(VR, " $test ") == "test"
        assert self._get_match(VR, "other stuff $test ") == "test"
        assert self._get_match(VR, "other $test stuff") == "test"
        assert self._get_match(VR, "other $test $test2 stuff") == "test"

    def test_delimiters(self):
        VR = tools.VAR_REGEXP
        for c in ('|', '=', '+', ' ', '$'):
            assert self._get_match(VR, "$test%s1" % c) == "test"

    def test_namespace(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, "$foo::bar") == "foo::bar"
        assert self._get_match(VR, " $foo::bar ") == "foo::bar"
        assert self._get_match(VR, "other $foo::bar stuff") == "foo::bar"

    def test_function(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, "$foo()") == "foo()"
        assert self._get_match(VR, " $foo() ") == "foo()"
        assert self._get_match(VR, "other $foo() stuff") == "foo()"
        assert self._get_match(VR, "other $foo::bar() stuff") == "foo::bar()"

    def test_function_with_arguments(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, '$foo("arg1", 1, {"foo": "bar"})') == 'foo("arg1", 1, {"foo": "bar"})'

    def test_parens(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, "$(foo)") == "foo"
        assert self._get_match(VR, "$(foo())") == "foo()"
        assert self._get_match(VR, "$(foo::bar)") == "foo::bar"
        assert self._get_match(VR, "$(foo::bar())") == "foo::bar()"
        assert self._get_match(VR, "$(foo::bar(1, 2, 3))") == "foo::bar(1, 2, 3)"

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


class Testparse_args:
    """tools.parse_args"""
    def test_args_can_be_len_0(self):
        assert tools.parse_args( [] ) == []

    def test_single_args(self):
        assert tools.parse_args( ["--test"] ) == [ ("--test", "") ]
        assert tools.parse_args( ["-a", "-b", "--c"] ) == [ ("-a", ""),
                                                            ("-b", ""),
                                                            ("--c", "") ]
    def test_key_value_args(self):
        assert tools.parse_args( ["--test", "foo"] ) == [ ("--test", "foo") ]
        assert tools.parse_args( ["--test", "foo",
                                  "-a",
                                  "--bar", "baz"] ) == [ ("--test", "foo"),
                                                         ("-a", ""),
                                                         ("--bar", "baz") ]

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
    def test_none_to_none(self):
        assert tools.escape_text(None) == None

    def test_empty_string_to_empty_string(self):
        assert tools.escape_text("") == ""

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
    def test_none_to_none(self):
        assert tools.urlencode_text(None) == None

    def test_empty_string_to_empty_string(self):
        assert tools.urlencode_text("") == "" 

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
    """tools.VariableDict class"""

    def __init__(self):
        # we use the same VariableDict instance through all
        # the tests since none of them mutate the instance.
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
        assert self.vd.get("badkey_escaped", 'no"value') == 'no"value'

    def test_can_urlencode_value(self):
        assert self.vd.get("a_urlencoded") == "b"
        assert self.vd.get("title_urlencoded") == "This%20is%20my%20story"
        assert self.vd.get("title2_urlencoded") == "Story%3A%20%22aha%21%22"
        assert self.vd.get("badkey_urlencoded", "novalue") == "novalue"
        assert self.vd.get("badkey_urlencoded", "no value") == "no value"

class TestStripper:
    """tools.Stripper class"""

    def _strip(self, text):
        s = tools.Stripper()
        s.feed(text)
        s.close()
        return s.gettext()

    def test_replaces_html_markup_from_string_with_space(self):
        s = tools.Stripper()
        assert self._strip("") == ""
        assert self._strip("abc") == "abc"
        assert self._strip("<b>abc</b>") == " abc "
        assert self._strip("abc<br />") == "abc "
        assert self._strip("abc <b>def</b> ghi") == "abc  def  ghi"
        
class TestWhatExt:
    """tools.what_ext"""
    def __init__(self):
        self._files = ["a.txt", "b.html", "c.txtl"]
        d = os.path.dirname(__file__)
        self._d = os.path.join(d, "what_ext_test_dir")
        
    def _setup(self):
        """
        Creates the directory with some files in it.
        """
        try:
            os.mkdir(self._d)

            for mem in self._files:
                f = open(os.path.join(self._d, mem), "w")
                f.write("lorem ipsum")
                f.close()
        except:
            self._teardown()

    def _teardown(self):
        """
        Cleans up the test files and the directory that we created.
        """
        for mem in self._files:
            try:
                os.remove(os.path.join(self._d, mem))
            except:
                pass

        try:
            os.rmdir(self._d)
        except:
            pass
    
    def test_returns_extension_if_file_has_extension(self):
        self._setup()
        try:
            assert "txt" == tools.what_ext(["txt", "html"],
                                           os.path.join(self._d, "a"))
            assert "html" == tools.what_ext(["txt", "html"],
                                           os.path.join(self._d, "b"))
        finally:
            self._teardown()

    def test_returns_None_if_extension_not_present(self):
        self._setup()
        try:
            assert None == tools.what_ext([],
                                          os.path.join(self._d, "a"))
            assert None == tools.what_ext(["html"],
                                          os.path.join(self._d, "a"))
        finally:
            self._teardown()
