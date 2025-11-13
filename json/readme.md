# Proyek Pyramid (Langkah 14: AJAX dan Render JSON)

Ini adalah langkah keempatbelas dalam tutorial Pyramid. Di langkah ini, kita akan membuat aplikasi kita lebih interaktif dengan menggunakan **AJAX** (via JavaScript/jQuery) untuk mengambil data dari *endpoint* **JSON** baru dan memperbarui halaman secara dinamis.

Proyek ini didasarkan pada [Quick Tutorial: AJAX/JSON](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/json.html) dari dokumentasi resmi Pyramid.

## 🎯 Tujuan

* Membuat *view* baru yang menggunakan `renderer='json'` untuk mengembalikan data sebagai JSON.
* Menambahkan rute baru (`/hello.json`) untuk *endpoint* JSON tersebut.
* Menggunakan jQuery (AJAX) di template untuk mengambil data dari *endpoint* JSON.
* Memperbarui halaman HTML secara dinamis menggunakan data yang diambil.
* Menambahkan tes untuk memvalidasi *endpoint* JSON yang baru.

## 🚀 Instalasi dan Langkah-Langkah

### 1. Persiapan Proyek (Salin dari Langkah 10)

Pertama, salin seluruh proyek `static_assets` Anda ke folder baru bernama `json`.

```bash
# Pastikan Anda di D:\Figo\projects\quick_tutorial
cd D:\Figo\projects\quick_tutorial

# Salin 'static_assets' ke 'json'
Copy-Item -Path static_assets -Destination json -Recurse
2. Buat Ulang dan Aktifkan venv
venv tidak bisa disalin. Anda harus membuatnya ulang di dalam folder json.

Bash

# Pindah ke direktori 'json' yang baru
cd D:\Figo\projects\quick_tutorial\json

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
1. tutorial/app.py (Tambahkan View & Rute JSON)
Kita menambahkan view hello_json baru dengan renderer='json' dan rute /hello.json.

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

    # ----------------------------------------------------------
    # ↓↓↓ VIEW BARU UNTUK JSON ↓↓↓
    # ----------------------------------------------------------
    @view_config(route_name='hello_json', renderer='json')
    def hello_json(self):
        print('Incoming request (JSON)')
        return {'name': 'Pyramid', 'project': 'tutorial'}


def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        config.add_route('hello', '/')
        
        # ----------------------------------------------------------
        # ↓↓↓ RUTE BARU DITAMBAHKAN DI SINI ↓↓↓
        # ----------------------------------------------------------
        config.add_route('hello_json', '/hello.json')
        
        config.add_static_view(name='static', path='tutorial:static')
        
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    settings['pyramid.includes'] = 'pyramid_jinja2'
    return app(global_config, **settings)
2. tutorial/templates/layout.jinja2 (Tambahkan jQuery)
Kita menambahkan link ke library jQuery di <head>.

HTML

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pyramid Quick Tutorial</title>
    
    <link rel="stylesheet"
          href="{{ request.static_url('tutorial:static/app.css') }}">
          
    <script src="//[code.jquery.com/jquery-2.1.1.min.js](https://code.jquery.com/jquery-2.1.1.min.js)"></script>
          
</head>
<body>
    {# 'block content' akan diisi oleh hello_world.jinja2 #}
    {% block content %}
    {% endblock %}
    
    {# 'block scripts' adalah blok baru untuk skrip kita #}
    {% block scripts %}
    {% endblock %}
</body>
</html>
3. tutorial/templates/hello_world.jinja2 (Tambahkan Skrip AJAX)
Kita menambahkan {% block scripts %} yang berisi kode JavaScript untuk memanggil endpoint JSON kita.

Cuplikan kode

{% extends "tutorial:templates/layout.jinja2" %}

{% block content %}
{# Judul h1 ini awalnya 'Hello Pyramid!' #}
<h1>Hello {{ name }}! Welcome to the {{ project }}!</h1>
{% endblock %}


{# ↓↓↓ TAMBAHKAN BLOK SKRIP INI ↓↓↓ #}
{% block scripts %}
<script>
$(document).ready(function() {
    // Jalankan kode ini saat halaman selesai dimuat
    
    // 1. Minta data JSON dari '/hello.json'
    $.getJSON('/hello.json', function(data) {
        
        // 2. Jika berhasil, ambil data 'name' dan 'project'
        var name = data.name;
        var project = data.project;
        
        // 3. Temukan <h1> dan ganti HTML-nya
        $('h1').html('Hello ' + name + '! Welcome to the ' + project + '!');
    });
});
</script>
{% endblock %}
4. tutorial/tests/test_views.py (Diperbarui)
Kita menambahkan test_hello_json dan memperbaiki setUp / _make_config untuk mendaftarkan rute-rute selama tes unit.

Python

import unittest
from pyramid import testing

def _make_config():
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    config = testing.setUp(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('tutorial:templates')
    
    # --- TAMBAHKAN RUTE YANG HILANG DI SINI ---
    # Kita harus mendaftarkan rute agar 'scan' dapat menemukannya
    config.add_route('hello', '/')
    config.add_route('hello_json', '/hello.json')
    config.add_static_view(name='static', path='tutorial:static')
    # ----------------------------------------
    
    return config

def _make_app():
    from tutorial.app import app
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    return app({}, **settings)


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = _make_config()
        # Sekarang 'scan' akan menemukan rute yang sudah didaftarkan
        self.config.scan('tutorial.app') 

    def tearDown(self):
        testing.tearDown()

    def _get_test_app(self):
        from webtest import TestApp
        return TestApp(_make_app())

    def test_hello_world(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    def test_css_file(self):
        test_app = self._get_test_app()
        res = test_app.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)

    # ----------------------------------------------------------
    # ↓↓↓ TES BARU DITAMBAHKAN DI SINI ↓↓↓
    # ----------------------------------------------------------
    def test_hello_json(self):
        test_app = self._get_test_app()
        res = test_app.get('/hello.json', status=200)
        # Periksa apakah bodinya adalah JSON yang benar
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})
5. tutorial/tests/test_functional.py (Diperbarui)
Kita juga menambahkan test_hello_json ke tes fungsional.

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

    def test_css_file(self):
        res = self.testapp.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)

    # ----------------------------------------------------------
    # ↓↓↓ TES BARU DITAMBAHKAN DI SINI ↓↓↓
    # ----------------------------------------------------------
    def test_hello_json(self):
        res = self.testapp.get('/hello.json', status=200)
        # Periksa apakah bodinya adalah JSON yang benar
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})
🏁 Menjalankan dan Memverifikasi
1. Menjalankan Tes
Pastikan semua perubahan Anda benar dengan menjalankan tes:

PowerShell

# Pastikan (venv) aktif
python -m pytest
Hasil: Anda akan melihat ================= 3 passed ... ================== (2 tes lama + 1 tes JSON baru).

2. Menjalankan Server
Setelah tes lulus, jalankan server:

PowerShell

pserve development.ini --reload
3. Cara Mengakses
Halaman Utama: Buka http://localhost:6543/. Halaman akan dimuat dan (sangat cepat) diperbarui oleh JavaScript.

Endpoint JSON: Buka http://localhost:6543/hello.json untuk melihat output JSON mentah yang digunakan oleh skrip AJAX.