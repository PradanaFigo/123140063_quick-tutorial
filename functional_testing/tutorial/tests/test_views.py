import unittest

from pyramid import testing


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        # Impor fungsi 'app' yang kita buat dari app.py
        from tutorial.app import app
        
        # Buat aplikasi 'dummy' untuk pengujian
        test_app = app({}, pyramid_includes=True)
        
        # Gunakan 'webtest' untuk membuat permintaan 'GET /' palsu
        from webtest import TestApp
        test_app.testapp = TestApp(test_app)
        
        # Lakukan permintaan ke '/'
        res = test_app.testapp.get('/', status=200)
        
        # Periksa apakah bodinya mengandung 'Hello World!'
        self.assertIn(b'<h1>Hello World!</h1>', res.body)