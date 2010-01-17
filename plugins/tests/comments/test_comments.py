"""
Tests for the comments plugin, contrib/plugins/comments/plugins/comments.py.
"""

__author__ = 'Ryan Barrett <pyblosxom@ryanb.org>'
__url__ = 'http://pyblosxom.sourceforge.net/wiki/index.php/Framework_for_testing_plugins'

from plugins.tests.test_base import PluginTest
from plugins.comments.plugins import comments

from nose.tools import eq_
import cgi, cPickle, os, cStringIO, sys

class TestComments(PluginTest):
    """Test class for the comments plugin.
    """
    def setUp(self):
        PluginTest.setUp(self, comments)

        # add comment templates
        self.renderer.flavour.update({'comment-story': 'comment-story',
                                      'comment': 'comment'})

        # inject the frozen time module
        comments.time = self.frozen_time

        # populate with default config vars
        comments.cb_start(self.args)

    def tearDown(self):
        PluginTest.tearDown(self)

    def comment_path(self):
        """Returns the comment path that would currently be created."""
        filename = '%s-%0.1f.%s' % (self.entry_name, self.timestamp,
                                    self.config['comment_draft_ext'])
        return os.path.join(self.config['comment_dir'], filename)

    def comment(self, title='title', author='author', body='body', url=None,
                email=None, ipaddress=None, encoding=None, preview=None,
                **kwargs):
        """Posts a comment with the given contents."""
        # set the encoding in the config. it should default to iso-8859-1.
        if encoding:
            self.config['blog_encoding'] = encoding

        # build up the form data and post the comment
        args = [(arg, vars()[arg])
                for arg in ('title', 'author', 'body', 'url', 'email', 'preview')
                if vars()[arg] is not None]
        self.set_form_data(dict(args))
        comments.cb_prepare(self.args)

    def check_comment_file(self, title='title', author='author', body='body',
                           url='', email='', encoding=None, ipaddress='',
                           expected_title=None, expected_author=None,
                           expected_body=None, expected_url=None, preview=None,
                           delete_datadir=True):
        """Posts a comment and checks its contents on disk."""
        self.comment(title, author, body, url, email, ipaddress, encoding,
                     preview)

        if encoding is None:
            encoding = 'iso-8859-1'
        if expected_title is None:
            expected_title = title
        if expected_author is None:
            expected_author = author
        if expected_body is None:
            expected_body = body
        if expected_url is None:
            expected_url = url

        # check the files in the comments directory
        files = os.listdir(self.config['comment_dir'])
        assert os.path.basename(self.comment_path()) in files
        assert comments.LATEST_PICKLE_FILE in files

        # check the coment file's contents
        expected_lines = [
            '<?xml version="1.0" encoding="%s"?>\n' % encoding,
            '<item>\n',
            '<description>%s</description>\n' % cgi.escape(expected_body),
            '<pubDate>%0.1f</pubDate>\n' % self.timestamp,
            '<author>%s</author>\n' % cgi.escape(expected_author),
            '<title>%s</title>\n' % cgi.escape(expected_title),
            '<source></source>\n',
            '<link>%s</link>\n' % cgi.escape(expected_url),
            '<w3cdate>%s</w3cdate>\n' % self.timestamp_w3c,
            '<cmt_date>%s</cmt_date>\n' % self.timestamp_date,
            '<ipaddress>%s</ipaddress>\n' % ipaddress,
            '</item>\n',
            ]
        if email:
            expected_lines.insert(-1, '<email>%s</email>\n' % email)

        file = open(self.comment_path())
        for expected, actual in zip(expected_lines, file.readlines()):
            eq_(expected, actual)

        if delete_datadir:
            self.delete_datadir()

    def check_comment_output(self, expected, delete_datadir=True, **kwargs):
        """Posts a comment and checks its rendered output.

        Note that this deletes the datadir before it posts the comment!
        """
        self.data['display_comment_default'] = True

        self.comment(**kwargs)
        self.args['template'] = ''
        comments.cb_story_end(self.args)
        eq_(expected, self.args['template'])

        if delete_datadir:
            self.delete_datadir()

    def test_cb_start(self):
        """cb_start() should set defaults for some config variables."""
        self.config = self.config_base
        comments.cb_start(self.args)

        eq_(os.path.join(self.datadir, 'comments'), self.config['comment_dir'])
        eq_('cmt', self.config['comment_ext'])
        eq_('cmt', self.config['comment_draft_ext'])
        eq_(0, self.config['comment_nofollow'])

    def test_verify_installation(self):
        """verify_installation should check the comment dir and smtp config."""
        # comment_dir must exist
        assert not os.path.exists('/not/a/directory')
        self.config['comment_dir'] = '/not/a/directory'
        eq_(0, comments.verify_installation(self.request))
        del self.config['comment_dir']

        # either all smtp config variables must be defined, or none
        smtp_vars = ['comment_smtp_server', 'comment_smtp_from',
                     'comment_smtp_to']
        for smtp_var in smtp_vars:
            [self.config.pop(var, '') for var in smtp_vars]
            self.config[smtp_var] = 'abc'
            eq_(0, comments.verify_installation(self.request))

        del self.config[smtp_vars[-1]]

        eq_(1, comments.verify_installation(self.request))

    def test_cb_handle(self):
        """cb_handle() should intercept requests for /comments.js."""
        eq_(None, comments.cb_handle(self.args))

        self.request.addHttp({'PATH_INFO': '/not_comments.js'})
        eq_(None, comments.cb_handle(self.args))

        self.request.addHttp({'PATH_INFO': '/comments.js'})
        eq_(True, comments.cb_handle(self.args))

        response = self.request.getResponse()
        eq_('text/javascript', response.getHeaders()['Content-Type'])

        out = cStringIO.StringIO()
        if hasattr(response, "send_body"):
            response.send_body(out)
        elif hasattr(response, "sendBody"):
            response.sendBody(out)
        else:
            raise Exception("response doesn't have sendBody or send_body.")
        assert out.getvalue().startswith('/* AJAX comment support for pyblosxom')

    def test_cb_prepare_showcomments(self):
        """cb_prepare() should set display_comment_default to show comments."""
        # default is to not show comments
        del self.data['bl_type']
        comments.cb_prepare(self.args)
        eq_(False, self.data['display_comment_default'])

        # show them if the bl_type config var is 'file'
        self.data['bl_type'] = 'db'
        comments.cb_prepare(self.args)
        eq_(False, self.data['display_comment_default'])

        self.data['bl_type'] = 'file'
        comments.cb_prepare(self.args)
        eq_(True, self.data['display_comment_default'])

        # or if the query string has showcomments=yes
        del self.data['bl_type']
        self.request.addHttp({'QUERY_STRING': 'x=yes&showcomments=no7&y=no'})
        comments.cb_prepare(self.args)
        eq_(False, self.data['display_comment_default'])

        self.request.addHttp({'QUERY_STRING': 'x=yes&showcomments=yes&y=no'})
        comments.cb_prepare(self.args)
        eq_(True, self.data['display_comment_default'])

    def test_cb_prepare_new_comment(self):
        """A new comment should be packaged in XML and stored in a new file."""
        self.check_comment_file(title='title', author='author', body='body')

        # url is optional. try setting it.
        self.check_comment_file(url='http://home/')

        # previewed comments shouldn't be stored
        self.comment(preview='yes')
        assert not os.path.exists(self.comment_path())

    def test_cb_prepare_encoding(self):
        """If the blog_encoding config var is set, it should be used."""
        self.check_comment_file(encoding='us-ascii')

    def test_cb_prepare_massage_link(self):
        """User-provided URLs should be scrubbed and linkified if necessary."""
        # html control characters should be stripped
        self.check_comment_file(url='<script arg=\'val"ue"\'>',
                                expected_url='http://script arg=value')

        # http:// should only be added if there isn't already a protocol
        self.check_comment_file(url='xmpp:me@jabber.org')

    def test_cb_prepare_nofollow(self):
        """Nofollow support should add rel="nofollow" to links in the body."""
        body = '<a href="/dest">x</a>'

        # default is off
        assert self.config['comment_nofollow'] == False
        self.check_comment_file(body=body)

        # turned on
        self.config['comment_nofollow'] = True
        nofollow_body = '<a rel="nofollow" href="/dest">x</a>'
        self.check_comment_file(body=body, expected_body=nofollow_body)

    def test_cb_prepare_email(self):
        """User-provided URLs should be scrubbed and linkified if necessary."""
        self.check_comment_file(email='a@b.c')

    def test_cb_prepare_ipaddress(self):
        """If provided, IP address should be recorded."""
        ipaddress = '12.34.56.78'
        self.request.addHttp({'REMOTE_ADDR': ipaddress})
        self.check_comment_file(ipaddress=ipaddress)

    def test_cb_reject(self):
        """Comments should be filtered with cb_comment_reject()."""
        # try rejecting the comment, with and without a message
        for return_value, msg in {True: 'Comment rejected.',
                                  (True, 'bad!'): 'bad!'
                                  }.items():
            self.inject_callback('comment_reject', lambda: return_value)
            self.comment()
            assert not os.path.exists(self.comment_path())
            eq_(True, self.data['rejected'])
            eq_(msg, self.data['comment_message'])

        del self.data['rejected']

        # try accepting the comment, with and without a message
        for return_value in [False, (False, 'ok')]:
            self.inject_callback('comment_reject', lambda: return_value)
            self.check_comment_file()

            assert 'rejected' not in self.data
            eq_('Comment submitted.  Thanks!', self.data['comment_message'])

    def test_cb_prepare_latest_pickle(self):
        """The "latest" file should contain the last comment's timestamp."""
        self.comment()
        latest_path = os.path.join(self.config['comment_dir'],
                                   comments.LATEST_PICKLE_FILE)
        timestamp = cPickle.load(open(latest_path))
        eq_(self.timestamp, timestamp)

    def test_cb_prepare_draft(self):
        """For draft support, comment_draft_ext should override comment_ext."""
        self.config['comment_draft_ext'] = 'draft'
        self.check_comment_file()

    def test_cb_head(self):
        """cb_head() should expand template variables in single-entry lists."""
        template = self.args['template']

        # only expand if we have a comment-head template
        assert 'comment-head' not in self.renderer.flavour
        eq_(template, comments.cb_head(self.args))
        assert not self.entry.has_key('title')

        # don't expand if we're displaying more than one entry
        self.renderer.flavour['comment-head'] = ''
        self.renderer.setContent([self.entry, self.entry])
        eq_(template, comments.cb_head(self.args))
        assert not self.entry.has_key('title')

        # we have comment-head and only one entry. expand!
        class MockEntry(dict):
            """Intercepts __getitem__ and records the key."""
            def __getitem__(self, key):
                self.key = key

        mock_entry = MockEntry()

        self.renderer.setContent([self.entry])
        self.args['entry'] = {'entry_list': [mock_entry]}
        eq_(template, comments.cb_head(self.args))
        eq_('title', mock_entry.key)

    def test_cb_renderer(self):
        """cb_renderer() should return an AjaxRenderer for ajax requests."""
        assert not isinstance(comments.cb_renderer(self.args),
                              comments.AjaxRenderer)

        self.set_form_data({'ajax': 'true'})
        assert isinstance(comments.cb_renderer(self.args),
                          comments.AjaxRenderer)

    def test_ajax_renderer(self):
        """AjaxRenderer should only output previewed and posted comments."""
        def should_output(template_name):
            renderer = comments.AjaxRenderer(self.request, self.data)
            return renderer._AjaxRenderer__shouldOutput(self.entry,
                                                        template_name)

        # a comment preview
        self.set_form_data({'ajax': 'preview'})
        eq_(True, should_output('comment-preview'))
        eq_(False, should_output('story'))

        # a comment that was just posted
        self.set_form_data({'ajax': 'post'})
        eq_(False, should_output('story'))

        self.entry['cmt_time'] = self.timestamp
        assert 'cmt_time' not in self.data
        eq_(False, should_output('comment'))

        self.data['cmt_time'] = self.timestamp
        eq_(True, should_output('comment'))

    def test_num_comments(self):
        """cb_story[_end]() should count the number of comments."""
        self.data['display_comment_default'] = True

        def check_num_comments(expected):
            for method in (comments.cb_story, comments.cb_story_end):
                if self.entry.has_key('num_comments'):
                    del self.entry['num_comments']
                method(self.args)
                eq_(expected, self.entry['num_comments'])

        check_num_comments(0)
        self.comment()
        check_num_comments(1)

        self.frozen_time.timestamp += 1
        self.comment()
        check_num_comments(2)

    def test_when_to_render_comments(self):
        """cb_story[_end]() should only render comments when appropriate."""
        def check_no_comments():
            comments.cb_story(self.args)
            eq_('template starts:', self.args['template'])
            comments.cb_story_end(self.args)
            eq_('template starts:', self.args['template'])

        del self.renderer.flavour['comment-story']
        check_no_comments()

        self.renderer.flavour['comment-story'] = 'comment-story'
        self.renderer.setContent([self.entry, self.entry])
        check_no_comments()

        self.renderer.setContent([self.entry])
        self.data['display_comment_default'] = False
        check_no_comments()

        self.data['display_comment_default'] = True
        self.entry['nocomments'] = True
        check_no_comments()

    def test_cb_story_comment_story_template(self):
        """Check that cb_story() appends the comment-story template.."""
        self.data['display_comment_default'] = True
        assert self.renderer.flavour['comment-story'] == 'comment-story'
        comments.cb_story(self.args)
        eq_('template starts:comment-story', self.args['template'])

    def test_cb_story_end_renders_comments(self):
        """Check that cb_story_end() renders comments."""
        self.data['display_comment_default'] = True

        # no comments. check both cb_story_end's return value and
        # args['template'].
        self.args['template'] = 'foo'
        eq_('foo', comments.cb_story_end(self.args))
        eq_('foo', self.args['template'])

        # one comment
        self.renderer.flavour['comment'] = '$cmt_time '
        expected = '%s ' % self.timestamp
        self.check_comment_output(expected, delete_datadir=False)

        # two comments
        self.frozen_time.timestamp += 1
        expected += '%s ' % self.frozen_time.timestamp
        self.check_comment_output(expected)

    def test_template_variables(self):
        """Check the comment template variables."""
        self.data['display_comment_default'] = True

        # these will sent in the form data
        args = {
            'body': 'body=with"chars',
            'author': 'author',
            'title': 'title',
            'url': 'http://snarfed.org/',
            'email': 'pyblosxom@ryanb.org',
            }

        # these will be used as template variables, prefixed with $cmt_
        vars = dict(args)

        for old, new in [('body', 'description'), ('url', 'link')]:
            vars[new] = vars[old]
            del vars[old]

        vars.update({
            # these are generated by pyblosxom
            'time': str(self.timestamp),
            'w3cdate': self.timestamp_w3c,
            'date': self.timestamp_date,
            'pubDate': self.timestamp_asc,
            'description': 'body=with"chars',
            })

        # these depends on the fact that dict.keys() and dict.values() return
        # items in the same order. so far, python guarantees this.
        def make_template():
            return '\n'.join('$cmt_%s' % name for name in vars.keys())

        def make_expected():
            return '\n'.join(vars.values())

        # a normal comment
        self.renderer.flavour['comment'] = 'comment:\n' + make_template()
        self.check_comment_output('comment:\n' + make_expected(), **args)

        # a previewed comment
        self.renderer.flavour['comment-preview'] = 'preview:\n' + make_template()
        args['preview'] = 'yes'
        self.check_comment_output('preview:\n' + make_expected(), **args)

        # a rejected comment
        del args['preview']
        self.inject_callback('comment_reject', lambda: (True, 'foo'))
        vars['description'] = '<span class="error">foo</span>'
        self.renderer.flavour['comment'] = 'comment:\n' + make_template()
        self.check_comment_output('comment:\n' + make_expected(), **args)

    def test_optionally_linked_author(self):
        """Test the cmt_optionally_linked_author template variable."""
        self.renderer.flavour['comment'] = '$cmt_optionally_linked_author'

        assert self.config['comment_nofollow'] == False
        self.check_comment_output('me', author='me', url='')
        self.check_comment_output('<a href="http://home">me</a>',
                                  author='me', url='home')

        self.config['comment_nofollow'] = True
        self.check_comment_output('me', author='me', url='')
        self.check_comment_output('<a rel="nofollow" href="http://home">me</a>',
                                  author='me', url='home')
