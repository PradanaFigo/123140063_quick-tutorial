import unittest
from webtest import TestApp

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        # Impor 'main' untuk tes fungsional
        from tutorial.app import main
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        app = main({}, **settings)
        self.testapp = TestApp(app)

    def test_home_view(self):
        # Tes rute '/'
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<p>This is the home view.</p>', res.body)

    def test_hello_view(self):
        # Tes rute '/hello/Pyramid'
        res = self.testapp.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)