import unittest

from pyramid import testing


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        # Sertakan jinja2 saat melakukan setup testing
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        self.config = testing.setUp(settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        # Impor fungsi 'app' yang kita buat dari app.py
        from tutorial.app import app
        
        # Sertakan jinja2 saat membuat aplikasi tes
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        test_app = app({}, **settings)
        
        from webtest import TestApp
        test_app.testapp = TestApp(test_app)
        
        # Lakukan permintaan ke '/'
        res = test_app.testapp.get('/', status=200)
        
        # Periksa apakah bodinya mengandung HTML yang baru
        self.assertIn(b'<h1>Hello Pyramid!', res.body)