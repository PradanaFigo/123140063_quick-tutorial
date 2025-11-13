import unittest
from webtest import TestApp

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial.app import main
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        app = main({}, **settings)
        self.testapp = TestApp(app)

    def test_home_view(self):
        res = self.testapp.get('/', status=200)
        # PERBAIKAN: Dibuat tidak kaku (brittle) dengan menghapus </p>
        self.assertIn(b'<p>This is the home view.', res.body)

    def test_hello_view(self):
        res = self.testapp.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    def test_hello_json(self):
        # Tes rute '/hello/Pyramid.json'
        res = self.testapp.get('/hello/Pyramid.json', status=200)
        # Periksa apakah bodinya adalah JSON yang benar
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})