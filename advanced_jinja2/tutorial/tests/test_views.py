import unittest
from pyramid import testing

# --------------------------------------------------------------
# FUNGSI SETUP TES (DIPERBARUI)
# --------------------------------------------------------------
def _make_config():
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    config = testing.setUp(settings=settings)
    config.include('pyramid_jinja2')
    # Kembali menggunakan add_jinja2_search_path
    config.add_jinja2_search_path('tutorial:templates')
    return config

def _make_app():
    from tutorial.app import app
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    return app({}, **settings)


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = _make_config()

    def tearDown(self):
        testing.tearDown()

    def _get_test_app(self):
        from webtest import TestApp
        return TestApp(_make_app())

    def test_home_view(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        self.assertIn(b'<p>This is the home view.', res.body)
        # Tes navigasi baru dari layout
        self.assertIn(b'<li><a href="/">Home</a></li>', res.body)

    def test_hello_view(self):
        test_app = self._get_test_app()
        res = test_app.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
        # Tes navigasi baru dari layout
        self.assertIn(b'<li><a href="/hello/Pyramid">Hello</a></li>', res.body)

    def test_hello_json(self):
        test_app = self._get_test_app()
        res = test_app.get('/hello/Pyramid.json', status=200)
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})

    def test_css_file(self):
        test_app = self._get_test_app()
        res = test_app.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)