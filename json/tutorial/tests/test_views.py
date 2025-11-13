import unittest
from pyramid import testing

# ------------------------------------------------------------------
# ↓↓↓ PERUBAHAN UTAMA ADA DI FUNGSI INI ↓↓↓
# ------------------------------------------------------------------
def _make_config():
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    config = testing.setUp(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('tutorial:templates')
    
    # --- TAMBAHKAN RUTE YANG HILANG DI SINI ---
    # Kita harus mendaftarkan rute agar 'scan' dapat menemukannya
    config.add_route('hello', '/')
    config.add_route('hello_json', '/hello.json')
    config.add_static_view(name='static', path='tutorial:static')
    # ----------------------------------------
    
    return config

def _make_app():
    from tutorial.app import app
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    return app({}, **settings)


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = _make_config()
        # Sekarang 'scan' akan menemukan rute yang sudah didaftarkan
        self.config.scan('tutorial.app') 

    def tearDown(self):
        testing.tearDown()

    def _get_test_app(self):
        from webtest import TestApp
        return TestApp(_make_app())

    def test_hello_world(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    def test_css_file(self):
        test_app = self._get_test_app()
        res = test_app.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)

    def test_hello_json(self):
        test_app = self._get_test_app()
        res = test_app.get('/hello.json', status=200)
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})