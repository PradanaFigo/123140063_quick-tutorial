# Proyek Pyramid (Langkah 10: Request dan Response)

Ini adalah langkah kesebelas dalam tutorial Pyramid. Di langkah ini, kita akan membuat aplikasi kita menjadi **dinamis**. Kita akan belajar cara membaca data dari URL (misalnya, nama Anda dari `/hello/Figo`) dan menggunakannya di dalam *view* dan *template* kita.

Kita akan membuat *view* "home" baru di `/` dan *view* "hello" dinamis di `/hello/{name}`.

Proyek ini didasarkan pada [Quick Tutorial: Request and Response](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/request_response.html) dari dokumentasi resmi Pyramid.

## 🎯 Tujuan

* Membuat rute dinamis yang menerima parameter dari URL (misalnya, `/hello/{name}`).
* Belajar cara mengakses parameter tersebut di dalam *view* menggunakan `request.matchdict`.
* Mengelola beberapa *view* dan rute di dalam satu *View Class*.
* Membuat template baru untuk *view* "home".

## 🚀 Instalasi dan Langkah-Langkah

### 1. Persiapan Proyek (Salin dari Langkah 9)

Pertama, salin seluruh proyek `view_classes` Anda ke folder baru bernama `request_response`.

```bash
# Pastikan Anda di D:\Figo\projects\quick_tutorial
cd D:\Figo\projects\quick_tutorial

# Salin 'view_classes' ke 'request_response'
Copy-Item -Path view_classes -Destination request_response -Recurse
2. Buat Ulang dan Aktifkan venv
venv tidak bisa disalin. Anda harus membuatnya ulang di dalam folder request_response.

Bash

# Pindah ke direktori 'request_response' yang baru
cd D:\Figo\projects\quick_tutorial\request_response

# HAPUS venv lama yang rusak (PENTING)
Remove-Item -Path venv -Recurse -Force

# Buat venv baru yang bersih
python -m venv venv

# Aktifkan venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1
3. Instal Proyek dan Dependensi
Tidak ada yang berubah di setup.py, tetapi venv baru Anda kosong, jadi kita perlu menginstal ulang semuanya.

Bash

# Pastikan (venv) aktif
pip install -e ".[dev,testing]"
📜 Perubahan Kode Utama
1. Perubahan Template
Kita mengubah nama template lama dan membuat yang baru.

Ubah Nama: tutorial\templates\hello_world.jinja2 diubah namanya menjadi tutorial\templates\hello.jinja2. Isinya tetap sama:

HTML

{% extends "tutorial:templates/layout.jinja2" %}

{% block content %}
<h1>Hello {{ name }}! Welcome to the {{ project }}!</h1>
{% endblock %}
File Baru: Buat tutorial\templates\home.jinja2:

PowerShell

New-Item tutorial\templates\home.jinja2
Isi home.jinja2:

HTML

{% extends "tutorial:templates/layout.jinja2" %}

{% block content %}
<p>This is the home view. <a href="/hello/Pyramid">Say Hello!</a></p>
{% endblock %}
2. Edit tutorial/app.py (Perubahan Besar)
Ganti seluruh isi tutorial/app.py dengan kode baru ini. Sekarang kita memiliki dua rute dan dua view method.

Python

from pyramid.config import Configurator
from pyramid.view import view_config

# ------------------------------------------------------------------
# ↓↓↓ PERUBAHAN UTAMA ADA DI SINI ↓↓↓
# ------------------------------------------------------------------

class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.project = 'tutorial'

    @view_config(route_name='home', renderer='home.jinja2')
    def home_view(self):
        print('Incoming request (home)')
        return {'name': 'Home', 'project': self.project}

    @view_config(route_name='hello', renderer='hello.jinja2')
    def hello_view(self):
        print('Incoming request (hello)')
        # Ambil 'name' dari URL (matchdict)
        name = self.request.matchdict['name']
        return {'name': name, 'project': self.project}

# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        # Rute lama (/) sekarang bernama 'home'
        config.add_route('home', '/')
        # Rute baru dinamis: /hello/{name}
        config.add_route('hello', '/hello/{name}')
        
        # 'config.scan' akan menemukan kedua @view_config
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
3. Perbarui Tes (Wajib)
Kedua file tes kita harus diubah total untuk menguji rute dan tampilan baru.

1. Edit tutorial/tests/test_views.py: Ganti seluruh isinya dengan ini:

Python

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

    def test_home_view(self):
        # Impor 'app' untuk tes unit
        from tutorial.app import app
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        test_app = app({}, **settings)
        
        from webtest import TestApp
        test_app.testapp = TestApp(test_app)
        
        # Tes rute '/'
        res = test_app.testapp.get('/', status=200)
        self.assertIn(b'<p>This is the home view.</p>', res.body)

    def test_hello_view(self):
        # Impor 'app' untuk tes unit
        from tutorial.app import app
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        test_app = app({}, **settings)
        
        from webtest import TestApp
        test_app.testapp = TestApp(test_app)
        
        # Tes rute '/hello/Pyramid'
        res = test_app.testapp.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
2. Edit tutorial/tests/test_functional.py: Ganti seluruh isinya dengan ini:

Python

import unittest
from webtest import TestApp

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        # Impor 'main' untuk tes fungsional
        from tutorial.app import main
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        app = main({}, **settings)
        self.testapp = TestApp(app)

    def test_home_view(self):
        # Tes rute '/'
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<p>This is the home view.</p>', res.body)

    def test_hello_view(self):
        # Tes rute '/hello/Pyramid'
        res = self.testapp.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
🏁 Menjalankan dan Memverifikasi
1. Menjalankan Tes
Pastikan semua perubahan Anda benar dengan menjalankan tes:

PowerShell

# Pastikan (venv) aktif
python -m pytest
Hasil: Anda akan melihat ================= 2 passed ... ==================.

2. Menjalankan Server
Setelah tes lulus, jalankan server:

PowerShell

pserve development.ini --reload
3. Cara Mengakses
Buka browser web Anda dan coba dua URL ini:

http://localhost:6543/

Ini akan menjalankan home_view dan menampilkan: "This is the home view."

http://localhost:6543/hello/Figo (atau ganti "Figo" dengan nama Anda)

Ini akan menjalankan hello_view dan menampilkan: "Hello Figo! Welcome to the tutorial!"