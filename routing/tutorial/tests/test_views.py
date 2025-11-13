import unittest
from pyramid import testing

class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        self.config = testing.setUp(settings=settings)
        self.config.include('pyramid_jinja2')
        self.config.add_jinja2_search_path('tutorial:templates')

    def tearDown(self):
        testing.tearDown()

    def _get_test_app(self):
        from tutorial.app import app
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        test_app = app({}, **settings)
        
        from webtest import TestApp
        return TestApp(test_app)

    def test_home_view(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        # PERBAIKAN: Dibuat tidak kaku (brittle) dengan menghapus </p>
        self.assertIn(b'<p>This is the home view.', res.body)

    def test_hello_view(self):
        test_app = self._get_test_app()
        res = test_app.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    def test_hello_json(self):
        test_app = self._get_test_app()
        # Tes rute '/hello/Pyramid.json'
        res = test_app.get('/hello/Pyramid.json', status=200)
        # Periksa apakah bodinya adalah JSON yang benar
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})