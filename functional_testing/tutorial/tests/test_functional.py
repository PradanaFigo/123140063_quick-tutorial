import unittest

from webtest import TestApp


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        # Impor fungsi 'main' dari app.py
        from tutorial.app import main
        
        # Siapkan pengaturan untuk file .ini
        # Kita gunakan 'development.ini' sebagai dasar
        # dan menimpa 'pyramid.includes' agar tidak memuat toolbar
        settings = {
            'pyramid.includes': [], # Kosongkan agar tidak ada debugtoolbar
        }
        
        # Buat aplikasi WSGI menggunakan 'main' (entry point)
        # dan pengaturan .ini kita
        app = main({}, **settings)
        
        # Buat 'TestApp' yang membungkus aplikasi WSGI kita
        self.testapp = TestApp(app)

    def test_hello_world(self):
        # Lakukan permintaan GET ke rute '/'
        res = self.testapp.get('/', status=200)
        
        # Periksa apakah bodinya mengandung 'Hello World!'
        self.assertIn(b'<h1>Hello World!</h1>', res.body)