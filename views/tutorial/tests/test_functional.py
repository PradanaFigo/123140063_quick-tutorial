import unittest

from webtest import TestApp


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        # Impor fungsi 'main' dari app.py
        from tutorial.app import main
        
        # Sertakan jinja2 saat memanggil 'main'
        settings = {
            'pyramid.includes': 'pyramid_jinja2',
        }
        
        # Buat aplikasi WSGI menggunakan 'main' (entry point)
        app = main({}, **settings)
        
        # Buat 'TestApp' yang membungkus aplikasi WSGI kita
        self.testapp = TestApp(app)

    def test_hello_world(self):
        # Lakukan permintaan GET ke rute '/'
        res = self.testapp.get('/', status=200)
        
        # Periksa apakah bodinya mengandung HTML yang baru
        self.assertIn(b'<h1>Hello Pyramid!', res.body)