import unittest
from webtest import TestApp

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial.app import main
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        app = main({}, **settings)
        self.testapp = TestApp(app)

    def test_hello_world(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    def test_css_file(self):
        res = self.testapp.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)

    # ----------------------------------------------------------
    # ↓↓↓ TES BARU DITAMBAHKAN DI SINI ↓↓↓
    # ----------------------------------------------------------
    def test_hello_json(self):
        res = self.testapp.get('/hello.json', status=200)
        # Periksa apakah bodinya adalah JSON yang benar
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})