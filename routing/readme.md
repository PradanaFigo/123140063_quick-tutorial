# Proyek Pyramid (Langkah 11: Routing)

Ini adalah langkah keduabelas dalam tutorial Pyramid. Di langkah ini, kita akan belajar cara menambahkan lebih banyak rute ke aplikasi kita. Secara spesifik, kita akan membuat *endpoint* API baru yang mengembalikan data **JSON** sebagai ganti HTML.

Proyek ini didasarkan pada [Quick Tutorial: More Routing](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/routing.html) dari dokumentasi resmi Pyramid.

## 🎯 Tujuan

* Menambahkan rute baru (`/hello/{name}.json`) yang merespons secara berbeda dari rute `/hello/{name}`.
* Membuat *view* baru yang menggunakan `renderer='json'` untuk secara otomatis mengubah *dictionary* Python menjadi respons JSON.
* Memperbaiki bug urutan rute (rute yang lebih spesifik harus didaftarkan terlebih dahulu).
* Menambahkan tes baru untuk memvalidasi *endpoint* JSON kita.

## 🚀 Instalasi dan Langkah-Langkah

### 1. Persiapan Proyek (Salin dari Langkah 11)

Pertama, salin seluruh proyek `request_response` Anda ke folder baru bernama `routing`.

```bash
# Pastikan Anda di D:\Figo\projects\quick_tutorial
cd D:\Figo\projects\quick_tutorial

# Salin 'request_response' ke 'routing'
Copy-Item -Path request_response -Destination routing -Recurse
2. Buat Ulang dan Aktifkan venv
venv tidak bisa disalin. Anda harus membuatnya ulang di dalam folder routing.

Bash

# Pindah ke direktori 'routing' yang baru
cd D:\Figo\projects\quick_tutorial\routing

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
1. Edit tutorial/app.py (Tambahkan View JSON & Perbaiki Urutan)
Ganti seluruh isi tutorial/app.py dengan kode baru ini. Perubahan terpenting adalah penambahan hello_json dan memperbaiki urutan add_route untuk menghindari error.

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
        name = self.request.matchdict['name']
        return {'name': name, 'project': self.project}

    # --------------------------------------------------------------
    # VIEW BARU UNTUK JSON
    # --------------------------------------------------------------
    @view_config(route_name='hello_json', renderer='json')
    def hello_json(self):
        print('Incoming request (hello_json)')
        name = self.request.matchdict['name']
        # Mengembalikan dictionary, renderer 'json' akan
        # mengubahnya menjadi data JSON
        return {'name': name, 'project': self.project}

# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        config.add_route('home', '/')
        
        # ----------------------------------------------------------
        # PERBAIKAN: Rute yang lebih spesifik (.json) harus 
        # didaftarkan SEBELUM rute yang lebih umum.
        # ----------------------------------------------------------
        config.add_route('hello_json', '/hello/{name}.json')
        config.add_route('hello', '/hello/{name}')
        
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
2. Perbarui Tes (Tambahkan Tes JSON & Perbaiki Tes Home)
Tes home_view kita dari langkah sebelumnya terlalu kaku (brittle). Kita akan memperbaikinya dan menambahkan tes untuk JSON.

Edit tutorial/tests/test_views.py: Ganti seluruh isinya dengan ini:

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
Edit tutorial/tests/test_functional.py: Ganti seluruh isinya dengan ini:

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
        # PERBAIKAN: Dibuat tidak kaku (brittle) dengan menghapus </p>
        self.assertIn(b'<p>This is the home view.', res.body)

    def test_hello_view(self):
        res = self.testapp.get('/hello/Pyramid', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    def test_hello_json(self):
        # Tes rute '/hello/Pyramid.json'
        res = self.testapp.get('/hello/Pyramid.json', status=200)
        # Periksa apakah bodinya adalah JSON yang benar
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})
🏁 Menjalankan dan Memverifikasi
1. Menjalankan Tes
Pastikan semua perubahan Anda benar dengan menjalankan tes:

PowerShell

# Pastikan (venv) aktif
python -m pytest
Hasil: Anda akan melihat ================= 3 passed ... ================== (1 home, 1 hello HTML, 1 hello JSON).

2. Menjalankan Server
Setelah tes lulus, jalankan server:

PowerShell

pserve development.ini --reload
3. Cara Mengakses
Buka browser web Anda dan coba URL BARU ini:

http://localhost:6543/hello/Figo.json

Anda tidak akan melihat halaman HTML. Sebaliknya, browser Anda akan menampilkan data JSON mentah:

JSON

{"name": "Figo", "project": "tutorial"}