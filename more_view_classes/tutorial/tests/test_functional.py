import unittest
from webtest import TestApp

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial.app import main
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        app = main({}, **settings)
        self.testapp = TestApp(app)

    # Ganti nama dari 'test_hello_world'
    def test_home_get(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    # Tes baru untuk form POST
    def test_home_post(self):
        res = self.testapp.post('/', {'project': 'Proyek Fungsional'}, status=200)
        self.assertIn(b'<h1>Hello Pyramid! Welcome to the Proyek Fungsional!</h1>', res.body)

    def test_css_file(self):
        res = self.testapp.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)

    # Ganti nama dari 'test_hello_json'
    def test_home_json(self):
        res = self.testapp.get('/home.json', status=200)
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})