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
        
        # Periksa teks H1
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
        # Periksa teks dari layout.jinja2
        self.assertIn(b'<title>Pyramid Quick Tutorial</title>', res.body)