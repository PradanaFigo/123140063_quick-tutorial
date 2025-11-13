# Proyek Pyramid (Langkah 13: Aset Statis)

Ini adalah langkah kesepuluh dalam tutorial Pyramid. Di langkah ini, kita akan belajar cara menyertakan file statis (seperti CSS, JavaScript, dan gambar) ke dalam aplikasi kita. Kita akan menambahkan file CSS sederhana untuk memberi *style* pada halaman kita.

Proyek ini didasarkan pada [Quick Tutorial: Static Assets](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/static_assets.html) dari dokumentasi resmi Pyramid.

## 🎯 Tujuan

* Membuat direktori `static` untuk menyimpan file CSS.
* Belajar cara mendaftarkan direktori statis di Pyramid menggunakan `config.add_static_view()`.
* Menghubungkan file CSS di template layout (`layout.jinja2`) menggunakan `request.static_url()`.
* Memperbarui tes untuk memverifikasi bahwa file CSS berhasil dimuat.

## 🚀 Instalasi dan Langkah-Langkah

### 1. Persiapan Proyek 

Pertama, salin seluruh proyek `view_classes` Anda ke folder baru bernama `static_assets`.

```bash
# Pastikan Anda di D:\Figo\projects\quick_tutorial
cd D:\Figo\projects\quick_tutorial

# Salin 'view_classes' ke 'static_assets'
Copy-Item -Path view_classes -Destination static_assets -Recurse
2. Buat Ulang dan Aktifkan venv
venv tidak bisa disalin. Anda harus membuatnya ulang di dalam folder static_assets.

Bash

# Pindah ke direktori 'static_assets' yang baru
cd D:\Figo\projects\quick_tutorial\static_assets

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
1. Buat File CSS Baru
Kita perlu membuat folder static dan file app.css di dalamnya.

Buat Folder static:

PowerShell

mkdir tutorial\static
Buat File app.css:

PowerShell

New-Item tutorial\static\app.css
Isi tutorial\static\app.css: Tempelkan kode CSS ini ke dalam file app.css yang baru Anda buat:

CSS

body {
    margin: 2em;
    font-family: sans-serif;
    background: #eee;
}

h1 {
    color: #333;
}
2. Edit tutorial/app.py (Tambahkan Static View)
Buka tutorial/app.py. Tambahkan satu baris baru di fungsi app() untuk mendaftarkan folder static kita.

Python

from pyramid.config import Configurator
from pyramid.view import view_config

class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.project = 'tutorial'

    @view_config(route_name='hello', renderer='hello_world.jinja2')
    def hello_world(self):
        print('Incoming request')
        return {'name': 'Pyramid', 'project': 'tutorial'}

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        config.add_route('hello', '/')
        
        # ----------------------------------------------------------
        # ↓↓↓ BARIS BARU DITAMBAHKAN DI SINI ↓↓↓
        # ----------------------------------------------------------
        config.add_static_view(name='static', path='tutorial:static')
        
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    settings['pyramid.includes'] = 'pyramid_jinja2'
    return app(global_config, **settings)
3. Edit tutorial/templates/layout.jinja2
Buka layout.jinja2 dan tambahkan tag <link> di dalam <head> untuk memuat file CSS baru kita.

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
</body>
</html>
4. Perbarui Tes (Wajib)
Kita perlu menambahkan tes baru untuk memverifikasi bahwa file CSS dapat diakses.

Edit tutorial/tests/test_views.py: Ganti seluruh isinya dengan ini:

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

    def test_hello_world(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    # ----------------------------------------------------------
    # ↓↓↓ TES BARU DITAMBAHKAN DI SINI ↓↓↓
    # ----------------------------------------------------------
    def test_css_file(self):
        test_app = self._get_test_app()
        res = test_app.get('/static/app.css', status=200)
        # Periksa apakah konten CSS kita ada di file
        self.assertIn(b'body {', res.body)
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

    def test_hello_world(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    # ----------------------------------------------------------
    # ↓↓↓ TES BARU DITAMBAHKAN DI SINI ↓↓↓
    # ----------------------------------------------------------
    def test_css_file(self):
        res = self.testapp.get('/static/app.css', status=200)
        # Periksa apakah konten CSS kita ada di file
        self.assertIn(b'body {', res.body)
🏁 Menjalankan dan Memverifikasi
1. Menjalankan Tes
Pastikan semua perubahan Anda benar dengan menjalankan tes:

PowerShell

# Pastikan (venv) aktif
python -m pytest
Hasil: Anda akan melihat ================= 2 passed ... ================== (1 tes lama + 1 tes CSS baru).

2. Menjalankan Server
Setelah tes lulus, jalankan server:

PowerShell

pserve development.ini --reload
3. Cara Mengakses
Buka http://localhost:6543/.

Anda akan melihat halaman yang sama, tetapi sekarang memiliki style CSS:

Latar belakang akan menjadi abu-abu (#eee).

Teks <h1> akan menjadi abu-abu gelap (#333).

Akan ada margin di sekitar konten.