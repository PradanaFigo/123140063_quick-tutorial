# Proyek Pyramid (Langkah 12: Advanced Jinja2)

Ini adalah langkah ketigabelas dalam tutorial Pyramid. Di langkah ini, kita akan belajar cara menggunakan *helper* (pembantu) Pyramid, seperti `request.route_url`, langsung di dalam template Jinja2 kita untuk membuat navigasi yang dinamis.

Proyek ini didasarkan pada [Quick Tutorial: Advanced Jinja2](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/jinja2.html) dari dokumentasi resmi Pyramid.

## 🎯 Tujuan

* Memperkenalkan `request.route_url` sebagai cara untuk menghasilkan URL dari nama rute di dalam template.
* Menggunakan `route_url` untuk membangun menu navigasi di file layout utama (`layout.jinja2`).
* Memperbarui tes untuk memverifikasi bahwa navigasi baru muncul di semua halaman.

## 🚀 Instalasi dan Langkah-Langkah

### 1. Persiapan Proyek (Salin dari Langkah 11)

Pertama, salin seluruh proyek `routing` Anda ke folder baru bernama `advanced_jinja2`.

```bash
# Pastikan Anda di D:\Figo\projects\quick_tutorial
cd D:\Figo\projects\quick_tutorial

# Salin 'routing' ke 'advanced_jinja2'
Copy-Item -Path routing -Destination advanced_jinja2 -Recurse
2. Buat Ulang dan Aktifkan venv
venv tidak bisa disalin. Anda harus membuatnya ulang di dalam folder advanced_jinja2.

Bash

# Pindah ke direktori 'advanced_jinja2' yang baru
cd D:\Figo\projects\quick_tutorial\advanced_jinja2

# HAPUS venv lama yang rusak (PENTING)
Remove-Item -Path venv -Recurse -Force

# Buat venv baru yang bersih
python -m venv venv

# Aktifkan venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1
3. Instal Proyek dan Dependensi
venv baru Anda kosong, jadi kita perlu menginstal ulang semua dependensi.

Bash

# Pastikan (venv) aktif
pip install -e ".[dev,testing]"
📜 Kode Proyek
1. tutorial/app.py
File app.py kita tetap stabil. File ini mendaftarkan jinja2, static_view, rute-rute, dan memindai view class kita.

Python

from pyramid.config import Configurator
from pyramid.view import view_config

class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.project = 'tutorial'

    @view_config(route_name='home', renderer='home.jinja2')
    def home_view(self):
        return {'name': 'Home', 'project': self.project}

    @view_config(route_name='hello', renderer='hello.jinja2')
    def hello_view(self):
        name = self.request.matchdict['name']
        return {'name': name, 'project': self.project}

    @view_config(route_name='hello_json', renderer='json')
    def hello_json(self):
        name = self.request.matchdict['name']
        return {'name': name, 'project': self.project}
    
    # Method ini ditambahkan untuk tutorial
    @view_config(route_name='change_name')
    def change_name(self):
        print('Change name view called')
        return self.request.response

# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        config.add_route('home', '/')
        config.add_route('hello_json', '/hello/{name}.json')
        config.add_route('hello', '/hello/{name}')
        
        # Tambahkan rute baru dari tutorial
        config.add_route('change_name', '/change/{name}')
        
        # Daftarkan folder 'static'
        config.add_static_view(name='static', path='tutorial:static')
        
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
2. tutorial/templates/layout.jinja2 (Perubahan Utama)
Ini adalah inti dari langkah ini. Kita menambahkan navigasi di bagian bawah menggunakan request.route_url() (sebagai fungsi).

HTML

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pyramid Quick Tutorial</title>
    <link rel="stylesheet"
          href="{{ request.static_url('tutorial:static/app.css') }}">
</head>
<body>
    {% block content %}
    {% endblock %}

    <hr>
    
    <p>Navigasi:</p>
    <ul>
        <li><a href="{{ request.route_url('home') }}">Home</a></li>
        <li><a href="{{ request.route_url('hello', name='Pyramid') }}">Hello</a></li>
    </ul>

</body>
</html>
3. tutorial/tests/test_views.py (Diperbarui)
Tes diperbarui untuk memverifikasi bahwa link navigasi baru dari layout.jinja2 muncul di halaman.

Python

import unittest
from pyramid import testing

def _make_config():
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    config = testing.setUp(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('tutorial:templates')
    return config

def _make_app():
    from tutorial.app import app
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    return app({}, **settings)


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = _make_config()

    def tearDown(self):
        testing.tearDown()

    def _get_test_app(self):
        from webtest import TestApp
        return TestApp(_make_app())

    def test_home_view(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        self.assertIn(b'<p>This is the home view.', res.body)
        # Tes navigasi baru dari layout
        self.assertIn(b'<li><a href="/">Home</a></li>', res.body)

    def test_hello_view(self):
        test_app = self._get_test_app()
        res = test_app.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
        # Tes navigasi baru dari layout
        self.assertIn(b'<li><a href="/hello/Pyramid">Hello</a></li>', res.body)

    def test_hello_json(self):
        test_app = self._get_test_app()
        res = test_app.get('/hello/Pyramid.json', status=200)
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})

    def test_css_file(self):
        test_app = self._get_test_app()
        res = test_app.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)
4. tutorial/tests/test_functional.py (Diperbarui)
Tes fungsional juga diperbarui untuk memverifikasi link navigasi baru.

Python

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
🏁 Menjalankan dan Memverifikasi
1. Menjalankan Tes
Pastikan semua perubahan Anda benar dengan menjalankan tes:

PowerShell

# Pastikan (venv) aktif
python -m pytest
Hasil: Anda akan melihat ================= 4 passed ... ==================.

2. Menjalankan Server
Setelah tes lulus, jalankan server:

PowerShell

pserve development.ini --reload
3. Cara Mengakses
Buka http://localhost:6543/.

Anda akan melihat halaman yang sama seperti sebelumnya, tetapi sekarang di bagian bawah ada dua link navigasi baru ("Home" dan "Hello") yang dibuat oleh request.route_url().