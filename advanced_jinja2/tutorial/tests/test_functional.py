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
        self.assertIn(b'<p>This is the home view.', res.body)
        # Tes navigasi baru dari layout
        self.assertIn(b'<li><a href="/">Home</a></li>', res.body)

    def test_hello_view(self):
        res = self.testapp.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
        # Tes navigasi baru dari layout
        self.assertIn(b'<li><a href="/hello/Pyramid">Hello</a></li>', res.body)

    def test_hello_json(self):
        res = self.testapp.get('/hello/Pyramid.json', status=200)
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})

    def test_css_file(self):
        res = self.testapp.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)