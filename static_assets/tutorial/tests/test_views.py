import unittest
from pyramid import testing

# ... (def _make_config dan def _make_app tetap sama) ...

def _make_config():
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    config = testing.setUp(settings=settings)
    config.include('pyramid_jinja2')
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

    def test_hello_world(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    # ----------------------------------------------------------
    # ↓↓↓ TES BARU DITAMBAHKAN DI SINI ↓↓↓
    # ----------------------------------------------------------
    def test_css_file(self):
        test_app = self._get_test_app()
        res = test_app.get('/static/app.css', status=200)
        # Periksa apakah konten CSS kita ada di file
        self.assertIn(b'body {', res.body)