import unittest
from pyramid import testing

def _make_config():
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    config = testing.setUp(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('tutorial:templates')
    
    # --- PERBARUI NAMA RUTE DI SINI ---
    config.add_route('home', '/')
    config.add_route('home_json', '/home.json')
    config.add_static_view(name='static', path='tutorial:static')
    # ----------------------------------
    
    return config

def _make_app():
    from tutorial.app import app
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    return app({}, **settings)


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = _make_config()
        self.config.scan('tutorial.app') 

    def tearDown(self):
        testing.tearDown()

    def _get_test_app(self):
        from webtest import TestApp
        return TestApp(_make_app())

    # Ganti nama dari 'test_hello_world'
    def test_home_get(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    # Tes baru untuk form POST
    def test_home_post(self):
        test_app = self._get_test_app()
        # Kirim data form
        res = test_app.post('/', {'project': 'Proyek Baru'}, status=200)
        # Pastikan halaman merespons dengan nama proyek baru
        self.assertIn(b'<h1>Hello Pyramid! Welcome to the Proyek Baru!</h1>', res.body)

    def test_css_file(self):
        test_app = self._get_test_app()
        res = test_app.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)

    # Ganti nama dari 'test_hello_json'
    def test_home_json(self):
        test_app = self._get_test_app()
        res = test_app.get('/home.json', status=200)
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})