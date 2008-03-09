import _path_pyblosxom

import string
import os
import os.path

from Pyblosxom import tools, pyblosxom

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
        for c in ('|', '=', '+', ' ', '$', '<', '>'):
            assert self._get_match(VR, "$test%s1" % c) == "test"

    def test_namespace(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, "$foo::bar") == "foo::bar"
        assert self._get_match(VR, " $foo::bar ") == "foo::bar"
        assert self._get_match(VR, "other $foo::bar stuff") == "foo::bar"

    def test_single_function(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, "$foo()") == "foo()"
        assert self._get_match(VR, " $foo() ") == "foo()"
        assert self._get_match(VR, "other $foo() stuff") == "foo()"
        assert self._get_match(VR, "other $foo::bar() stuff") == "foo::bar()"

    def test_function_with_arguments(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, '$foo("arg1")') == 'foo("arg1")'
        assert self._get_match(VR, '$foo("arg1", 1)') == 'foo("arg1", 1)'

    def test_parens(self):
        VR = tools.VAR_REGEXP
        assert self._get_match(VR, "$(foo)") == "(foo)"
        assert self._get_match(VR, "$(foo())") == "(foo())"
        assert self._get_match(VR, "$(foo::bar)") == "(foo::bar)"
        assert self._get_match(VR, "$(foo::bar())") == "(foo::bar())"
        assert self._get_match(VR, "$(foo::bar(1, 2, 3))") == "(foo::bar(1, 2, 3))"


class Testparse:
    """tools.parse"""
    def _get_req(self):
        return pyblosxom.Request( {}, {}, {} )

    def test_simple(self):
        def pt(d, t):
            return tools.parse(self._get_req(), "iso-8859-1", d, t)

        assert pt( { "foo": "FOO" }, "foo foo foo") == "foo foo foo"
        assert pt( { "foo": "FOO" }, "foo $foo foo") == "foo FOO foo"
        assert pt( { "foo": "FOO" }, "foo $foor foo") == "foo  foo"

    def test_delimited(self):
        def pt(d, t):
            return tools.parse(self._get_req(), "iso-8859-1", d, t)

        assert pt( { "foo": "FOO" }, "foo $(foo) foo") == "foo FOO foo"
        assert pt( { "foo": "FOO" }, "foo $(foor) foo") == "foo  foo"

    def test_functions(self):
        def pt(d, t):
            return tools.parse(self._get_req(), "iso-8859-1", d, t)

        assert pt( { "foo": lambda req, vd: "FOO" }, "foo foo foo") == "foo foo foo"
        assert pt( { "foo": lambda req, vd: "FOO" }, "foo $foo() foo") == "foo FOO foo"
        assert pt( { "foo": lambda req, vd, z: z }, "foo $foo('a') foo") == "foo a foo"
        assert pt( { "foo": lambda req, vd, z: z, "bar": "BAR" }, "foo $foo(bar) foo") == "foo BAR foo"
        assert pt( { "foo": lambda req, vd, z: z, "bar": "BAR" }, "foo $foo($bar) foo") == "foo BAR foo"

    def test_functions_old_behavior(self):
        def pt(d, t):
            return tools.parse(self._get_req(), "iso-8859-1", d, t)

        # test the old behavior that allowed for functions that have no
        # arguments--in this case we don't pass a request object in
        assert pt( { "foo": (lambda : "FOO") }, "foo $foo() foo") == "foo FOO foo"

    def test_functions_with_args_that_have_commas(self):
        def pt(d, t):
            return tools.parse(self._get_req(), "iso-8859-1", d, t)

        vd = { "foo": lambda req, vd, x: (x + "A"),
               "foo2": lambda req, vd, x, y: (y + x) }

        assert pt(vd, '$foo("ba,ar")') == "ba,arA"
        assert pt(vd, '$foo2("a,b", "c,d")') == "c,da,b"

    def test_functions_with_var_args(self):
        def pt(d, t):
            return tools.parse(self._get_req(), "iso-8859-1", d, t)

        vd = { "foo": lambda req, vd, x: (x + "A"), "bar": "BAR" }

        # this bar is a string
        assert pt(vd, "foo $foo('bar') foo") == "foo barA foo"

        # this bar is also a string
        assert pt(vd, 'foo $foo("bar") foo') == "foo barA foo"

        # this bar is an identifier which we lookup in the var_dict and pass
        # into the foo function
        assert pt(vd, "foo $foo(bar) foo") == "foo BARA foo"

    def test_escaped(self):
        def pt(d, t):
            ret = tools.parse(self._get_req(), "iso-8859-1", d, t)
            print ret
            return ret

        vd = dict(tools.STANDARD_FILTERS)
        vd.update( { "foo": "'foo'" } )
        # this is old behavior
        assert pt(vd, "$foo_escaped") == "&apos;foo&apos;"

        # this is the new behavior using the escape filter
        assert pt(vd, "$escape(foo)") == "&apos;foo&apos;"

class Testcommasplit:
    """tools.commasplit"""
    def test_commasplit(self):
        tcs = tools.commasplit
        assert tcs( None ) == []
        assert tcs( "" ) == [""]
        assert tcs( "a" ) == ["a"]
        assert tcs( "a b c" ) == ["a b c"]
        assert tcs( "a, b, c" ) == ["a", " b", " c"]
        assert tcs( "a, 'b, c'" ) == ["a", " 'b, c'"]
        assert tcs( "a, \"b, c\"" ) == ["a", " \"b, c\""]
 
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

class TestgenerateRandStr:
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

class Testescape_text:
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

class Testurlencode_text:
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

class Testimportname:
    """tools.importname"""
    def _setup(self):
        tools._config = {}

    def _teardown(self):
        del tools.__dict__["_config"]

    def _c(self, mn, n):
        m = tools.importname(mn, n)
        print repr(m)
        return m

    def test_goodimport(self):
        self._setup()

        import string
        assert self._c("", "string") == string

        import os.path
        from os import path
        assert self._c("os", "path") == path

        self._teardown()

class Testwhat_ext:
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

class Testrun_callback:
    """tools.run_callback

    This tests run_callback functionality.
    """
    def test_run_callback(self):
        def fun1(args):
            assert args["x"] == 0
            return { "x": 1 }

        def fun2(args):
            assert args["x"] == 1
            return { "x": 2 }

        def fun3(args):
            assert args["x"] == 2
            return { "x": 3 }

        args = { "x": 0 }
        ret = tools.run_callback( [fun1, fun2, fun3], args, 
                                  mappingfunc = lambda x,y: y )
        assert ret["x"] == 3

class Testconvert_configini_values:
    """tools.convert_configini_values

    This tests config.ini -> config conversions.
    """
    def cmp(self, a, b):
        print "comparing %s with %s" % (repr(a), repr(b))
        if not a and not b: 
            return True
        if (not a and b) or (a and not b): 
            return False

        if not type(a) == type(b):
            return False

        # this handles strings and integers
        if a == b:
            return True

        if type(a) == type( [] ) or type(a) == type( () ):
            if not len(a) == len(b):
                return False
            for i in range(len(a)):
                if not self.cmp(a[i], b[i]):
                    return False
            return True
                
        if type(a) == type( {} ):
            if not len(a) == len(b):
                return False

            for k in a.keys():
                if not self.cmp(a[k], b[k]):
                    return False
            return True        

        return False

    def test_cmp(self):
        assert self.cmp( {}, {} )
        assert self.cmp( {"a": 1}, {"a": 1} )
        assert self.cmp( {"a": "b"}, {"a": "b"} )
        assert (not self.cmp( {"a": 1}, {"a": 2} ))

    def test_empty(self):
        assert self.cmp(tools.convert_configini_values( {} ),
                        {})

    def test_no_markup(self):
        assert self.cmp(tools.convert_configini_values( { "a": "b" } ),
                        { "a": "b" })

    def test_integers(self):
        assert self.cmp(tools.convert_configini_values( { "a": "1" } ),
                        { "a": 1 })
        assert self.cmp(tools.convert_configini_values( { "a": "1", "b": "2" } ),
                        { "a": 1, "b": 2 })
        assert self.cmp(tools.convert_configini_values( { "a": "10" } ),
                        { "a": 10 })
        assert self.cmp(tools.convert_configini_values( { "a": "100" } ),
                        { "a": 100 })
        assert self.cmp(tools.convert_configini_values( { "a": " 100  " } ),
                        { "a": 100 })

    def test_strings(self):
        assert self.cmp(tools.convert_configini_values( { "a": "'b'" } ),
                        { "a": "b" })
        assert self.cmp(tools.convert_configini_values( { "a": "\"b\"" } ),
                        { "a": "b" })
        assert self.cmp(tools.convert_configini_values( { "a": "   \"b\" " } ),
                        { "a": "b" })

    def test_lists(self):
        assert self.cmp(tools.convert_configini_values( { "a": "[]" } ),
                        { "a": [ ] })
        assert self.cmp(tools.convert_configini_values( { "a": "[1]" } ),
                        { "a": [ 1 ] })
        assert self.cmp(tools.convert_configini_values( { "a": "[1, 2]" } ),
                        { "a": [ 1, 2 ] })
        assert self.cmp(tools.convert_configini_values( { "a": "  [1 ,2 , 3]  " } ),
                        { "a": [ 1, 2, 3 ] })
        assert self.cmp(tools.convert_configini_values( { "a": "['1' ,\"2\" , 3]" } ),
                        { "a": [ "1", "2", 3 ] })

    def test_syntax_exceptions(self):
        def checkbadsyntax(d):
            try:
                tools.convert_configini_values( d )
            except tools.ConfigSyntaxErrorException, csee:
                assert True
            except Exception, e:
                print repr(e)
                assert False

        checkbadsyntax( { "a": "'b" } )
        checkbadsyntax( { "a": "b'" } )
        checkbadsyntax( { "a": "\"b" } )
        checkbadsyntax( { "a": "b\"" } )
        checkbadsyntax( { "a": "[b" } )
        checkbadsyntax( { "a": "b]" } )
