from StringIO import StringIO

from Pyblosxom.tests.helpers import UnitTestBase
from Pyblosxom.pyblosxom import Request
from Pyblosxom.renderers import blosxom

req = Request({}, {}, {})

class TestBlosxomRenderer(UnitTestBase):
    def test_dollar_parse_problem(self):
        output = StringIO()
        renderer = blosxom.BlosxomRenderer(req, output)
        renderer.flavour = {"story": "$(body)"}

        # mocking out _run_callback to just return the args dict
        renderer._run_callback = lambda c, args: args

        entry = {"body": r'PS1="\u@\h \[\$foo \]\W\[$RST\] \$"'}

        # the rendered template should be exactly the same as the body
        # in the entry--no \$ -> $ silliness.
        self.eq_(renderer.render_template(entry, "story"),
                 entry["body"])
