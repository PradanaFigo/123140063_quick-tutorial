import unittest

from pyramid import testing


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        self.config = testing.setUp(settings=settings)
        # Kita juga perlu memuat konfigurasi Jinja2 di tes
        self.config.include('pyramid_jinja2')
        self.config.add_jinja2_search_path('tutorial:templates')

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        from tutorial.app import app
        
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        test_app = app({}, **settings)
        
        from webtest import TestApp
        test_app.testapp = TestApp(test_app)
        
        res = test_app.testapp.get('/', status=200)
        
        # Periksa teks H1
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
        # Periksa teks dari layout.jinja2
        self.assertIn(b'<title>Pyramid Quick Tutorial</title>', res.body)