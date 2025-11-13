# Proyek Pyramid (Langkah 15: More View Classes)

Ini adalah langkah kelimabelas dalam tutorial Pyramid. Di langkah ini, kita akan belajar cara mengarahkan *request* yang berbeda (seperti `GET` dan `POST`) ke *method* yang berbeda di dalam **satu *view class*** yang sama. Ini adalah cara standar untuk menangani *form submission* (pengiriman formulir).

Proyek ini didasarkan pada [Quick Tutorial: More View Classes](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/more_view_classes.html) dari dokumentasi resmi Pyramid.

## 🎯 Tujuan

* Menggunakan argumen `request_method` di `@view_config` untuk memisahkan logika `GET` dan `POST`.
* Membuat *view method* `home_get` untuk menangani permintaan halaman.
* Membuat *view method* `home_post` untuk menangani data yang dikirim dari formulir.
* Mengganti nama rute dan *template* agar lebih sesuai (`hello` -> `home`).

## 🚀 Instalasi dan Langkah-Langkah

### 1. Persiapan Proyek (Salin dari Langkah 14)

Pertama, salin seluruh proyek `json` Anda ke folder baru bernama `more_view_classes`.

```bash
# Pastikan Anda di D:\Figo\projects\quick_tutorial
cd D:\Figo\projects\quick_tutorial

# Salin 'json' ke 'more_view_classes'
Copy-Item -Path json -Destination more_view_classes -Recurse
2. Buat Ulang dan Aktifkan venv
venv tidak bisa disalin. Anda harus membuatnya ulang di dalam folder more_view_classes.

Bash

# Pindah ke direktori 'more_view_classes' yang baru
cd D:\Figo\projects\quick_tutorial\more_view_classes

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
4. Ubah Nama Template
Kita mengubah nama hello_world.jinja2 menjadi home.jinja2 agar lebih sesuai.

PowerShell

Rename-Item -Path tutorial\templates\hello_world.jinja2 -NewName home.jinja2
📜 Kode Proyek
1. tutorial/app.py
View hello_world dipecah menjadi home_get (untuk GET) dan home_post (untuk POST), dan rute-rute diperbarui.

Python

from pyramid.config import Configurator
from pyramid.view import view_config

class TutorialViews:
    def __init__(self, request):
        self.request = request

    # ----------------------------------------------------------
    # VIEW UNTUK GET
    # ----------------------------------------------------------
    @view_config(
        route_name='home',
        renderer='home.jinja2',
        request_method='GET'  # <-- Hanya merespons GET
    )
    def home_get(self):
        print('Incoming GET request')
        return {'name': 'Pyramid', 'project': 'tutorial'}

    # ----------------------------------------------------------
    # VIEW BARU UNTUK POST (FORM)
    # ----------------------------------------------------------
    @view_config(
        route_name='home',
        renderer='home.jinja2',
        request_method='POST' # <-- Hanya merespons POST
    )
    def home_post(self):
        print('Incoming POST request')
        # Ambil 'project' dari data form yang di-POST
        project_name = self.request.params['project']
        # Kembalikan nama proyek baru ke template
        return {'name': 'Pyramid', 'project': project_name}

    # ----------------------------------------------------------
    # VIEW JSON
    # ----------------------------------------------------------
    @view_config(route_name='home_json', renderer='json')
    def home_json(self):
        print('Incoming request (JSON)')
        return {'name': 'Pyramid', 'project': 'tutorial'}


def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        # ----------------------------------------------------------
        # NAMA RUTE DIPERBARUI
        # ----------------------------------------------------------
        config.add_route('home', '/')
        config.add_route('home_json', '/home.json')
        
        config.add_static_view(name='static', path='tutorial:static')
        
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    settings['pyramid.includes'] = 'pyramid_jinja2'
    return app(global_config, **settings)
2. tutorial/templates/home.jinja2
Template ini (sebelumnya hello_world.jinja2) sekarang berisi <form> dan URL AJAX-nya diperbarui.

Cuplikan kode

{% extends "tutorial:templates/layout.jinja2" %}

{% block content %}
{# <h1> akan diisi oleh AJAX atau oleh 'project' dari POST #}
<h1>Hello {{ name }}! Welcome to the {{ project }}!</h1>

{# TAMBAHKAN FORM INI #}
<form method="POST"
      action="{{ request.route_url('home') }}">
    <label>Ganti Nama Proyek:</label>
    <input type="text" name="project" value="{{ project }}">
    <input type="submit" value="Simpan">
</form>

{% endblock %}


{% block scripts %}
<script>
$(document).ready(function() {
    
    // 1. Minta data JSON dari '/home.json' (URL BARU)
    $.getJSON('{{ request.route_url("home_json") }}', function(data) {
        
        // 2. Jika berhasil, ambil data 'name' dan 'project'
        var name = data.name;
        var project = data.project;
        
        // 3. Temukan <h1> dan ganti HTML-nya
        $('h1').html('Hello ' + name + '! Welcome to the ' + project + '!');
    });
});
</script>
{% endblock %}
3. tutorial/tests/test_views.py (Diperbarui)
Tes diperbarui untuk mencerminkan rute baru dan menambahkan tes untuk POST.

Python

import unittest
from pyramid import testing

def _make_config():
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    config = testing.setUp(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('tutorial:templates')
    
    # --- PERBARUI NAMA RUTE DI SINI ---
    config.add_route('home', '/')
    config.add_route('home_json', '/home.json')
    config.add_static_view(name='static', path='tutorial:static')
    # ----------------------------------
    
    return config

def _make_app():
    from tutorial.app import app
    settings = {'pyramid.includes': 'pyramid_jinja2'}
    return app({}, **settings)


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = _make_config()
        self.config.scan('tutorial.app') 

    def tearDown(self):
        testing.tearDown()

    def _get_test_app(self):
        from webtest import TestApp
        return TestApp(_make_app())

    # Ganti nama dari 'test_hello_world'
    def test_home_get(self):
        test_app = self._get_test_app()
        res = test_app.get('/', status=200)
        self.assertIn(b'<h1>Hello Pyramid!', res.body)

    # Tes baru untuk form POST
    def test_home_post(self):
        test_app = self._get_test_app()
        # Kirim data form
        res = test_app.post('/', {'project': 'Proyek Baru'}, status=200)
        # Pastikan halaman merespons dengan nama proyek baru
        self.assertIn(b'<h1>Hello Pyramid! Welcome to the Proyek Baru!</h1>', res.body)

    def test_css_file(self):
        test_app = self._get_test_app()
        res = test_app.get('/static/app.css', status=200)
        self.assertIn(b'body {', res.body)

    # Ganti nama dari 'test_hello_json'
    def test_home_json(self):
        test_app = self._get_test_app()
        res = test_app.get('/home.json', status=200)
        self.assertEqual(res.json_body, {'name': 'Pyramid', 'project': 'tutorial'})
4. tutorial/tests/test_functional.py (Diperbarui)
Tes fungsional juga diperbarui untuk mencerminkan perubahan.

Python

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

Halaman akan dimuat dan judulnya akan diatur oleh AJAX (...Welcome to the tutorial!).

Ubah teks di dalam kotak (misalnya, "Proyek Keren") dan tekan "Simpan".

Halaman akan dimuat ulang (melalui POST) dan judulnya akan berubah menjadi ...Welcome to the Proyek Keren!.