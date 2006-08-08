import string
from Pyblosxom import tools

def compare_unordered_lists(lista, listb):
    lista.sort()
    listb.sort()
    for mem in lista:
        print "comparing '" + mem + "' and '" + listb[0] + "'"
        assert len(listb) > 0
        assert listb[0] == mem
        listb.pop(0)
    assert len(listb) == 0

def test_is_year():
    assert tools.is_year(None) == 0
    assert tools.is_year("") == 0
    assert tools.is_year("ab") == 0
    assert tools.is_year("97") == 0
    assert tools.is_year("1997") == 1
    assert tools.is_year("2097") == 1

def _gen_checker(s, minlen, maxlen):
    assert len(s) >= minlen and len(s) <= maxlen
    for c in s:
        assert c in string.letters or c in string.digits

def test_generateRandStr():
    # this is a mediocre test because generateRandStr produces
    # a string that's of random length and random content.
    # it's possible for this test to pass even when the code
    # is bad.
    _gen_checker(tools.generateRandStr(), 5, 10)
    _gen_checker(tools.generateRandStr(), 5, 10)
    _gen_checker(tools.generateRandStr(), 5, 10)
    _gen_checker(tools.generateRandStr(), 5, 10)
    _gen_checker(tools.generateRandStr(), 5, 10)
    _gen_checker(tools.generateRandStr(4, 10), 4, 10)
    _gen_checker(tools.generateRandStr(4, 10), 4, 10)
    _gen_checker(tools.generateRandStr(4, 10), 4, 10)
    _gen_checker(tools.generateRandStr(4, 10), 4, 10)
    _gen_checker(tools.generateRandStr(4, 10), 4, 10)
    _gen_checker(tools.generateRandStr(3, 12), 3, 12)
    _gen_checker(tools.generateRandStr(3, 12), 3, 12)
    _gen_checker(tools.generateRandStr(3, 12), 3, 12)
    _gen_checker(tools.generateRandStr(3, 12), 3, 12)
    _gen_checker(tools.generateRandStr(3, 12), 3, 12)

def test_escape_text():
    assert tools.escape_text(None) == None
    assert tools.escape_text("") == ""
    assert tools.escape_text("abc") == "abc"
    assert tools.escape_text("a'b") == "a&apos;b"
    assert tools.escape_text("a\"b") == "a&quot;b"

def test_urlencode_text():
    assert tools.urlencode_text(None) == None
    assert tools.urlencode_text("") == ""
    assert tools.urlencode_text("abc") == "abc"
    assert tools.urlencode_text("a=c") == "a%3Dc"
    assert tools.urlencode_text("a&c") == "a%26c"

def test_variable_dict():
    vd = tools.VariableDict()
    vd.update( { "a": "b", \
                 "title": "This is my story", \
                 "title2": "Story: \"aha!\"", \
                 "filename": "joe.txt" } )
    assert vd.get("a") == "b"
    assert vd.get("a_escaped") == "b"
    assert vd.get("a_urlencoded") == "b"

    assert vd.get("title") == "This is my story"
    assert vd.get("title_escaped") == "This is my story"
    assert vd.get("title_urlencoded") == "This%20is%20my%20story"

    assert vd.get("title2") == "Story: \"aha!\""
    assert vd.get("title2_escaped") == "Story: &quot;aha!&quot;"
    assert vd.get("title2_urlencoded") == "Story%3A%20%22aha%21%22"

    assert vd.get("badkey", "novalue") == "novalue"
    assert vd.get("badkey_escaped", "novalue") == "novalue"
    assert vd.get("badkey_escaped", "no value") == "no value"
    assert vd.get("badkey_urlencoded", "novalue") == "novalue"
    assert vd.get("badkey_urlencoded", "no value") == "no%20value"

    compare_unordered_lists(vd.keys(), ["a", "title", "title2", "filename"])
    compare_unordered_lists(vd.values(), ["b", "This is my story", "Story: \"aha!\"", "joe.txt"])
