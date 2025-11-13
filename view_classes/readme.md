# Proyek Pyramid (Langkah 8: Templating dengan Layouts)

Ini adalah langkah kedelapan dalam tutorial Pyramid. Kita akan menyempurnakan penggunaan template Jinja2 dengan mengenalkan **template layout** (tata letak). Ini memungkinkan kita memiliki satu file HTML utama (seperti `layout.jinja2`) dan file konten yang lebih kecil (`hello_world.jinja2`) yang "mengisi" bagian-bagian dari layout tersebut.

Proyek ini didasarkan pada [Quick Tutorial: Changing the Renderer](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/templating.html) dari dokumentasi resmi Pyramid.

## 🎯 Tujuan

* Memperkenalkan konsep *template inheritance* (pewarisan template) di Jinja2.
* Membuat file `layout.jinja2` sebagai template dasar.
* Mengubah `hello_world.jinja2` agar *extends* (menggunakan) layout dasar.
* Mengatur agar template Jinja2 otomatis di-reload saat diubah (tanpa perlu restart server).

## 🚀 Instalasi dan Langkah-Langkah

### 1. Persiapan Proyek (Salin dari Langkah 7)

Pertama, salin seluruh proyek `views` Anda ke folder baru bernama `templating`.

```bash
# Pastikan Anda di D:\Figo\projects\quick_tutorial
cd D:\Figo\projects\quick_tutorial

# Salin 'views' ke 'templating'
Copy-Item -Path views -Destination templating -Recurse
2. Buat Ulang dan Aktifkan venv
venv tidak bisa disalin. Anda harus membuatnya ulang di dalam folder templating.

Bash

# Pindah ke direktori 'templating' yang baru
cd D:\Figo\projects\quick_tutorial\templating

# HAPUS venv lama yang rusak (PENTING)
Remove-Item -Path venv -Recurse -Force

# Buat venv baru yang bersih
python -m venv venv

# Aktifkan venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1
3. Instal Proyek dan Dependensi
Tidak ada perubahan pada setup.py, tetapi kita perlu menginstal semua dependensi ke dalam venv baru kita.

Bash

# Pastikan (venv) aktif
pip install -e ".[dev,testing]"
4. Edit development.ini (Perbaikan Error & Reload)
Buka development.ini. Ganti seluruh isinya dengan versi yang benar dan sederhana ini, yang juga menambahkan jinja2.reload_all = true. Ini memperbaiki RecursionError sebelumnya.

Ini, TOML

[app:main]
use = egg:tutorial

pyramid.includes =
    pyramid_debugtoolbar

# Baris baru untuk auto-reload template
jinja2.reload_all = true

[server:main]
use = egg:waitress#main
host = 0.0.0.0
port = 6543
5. Edit production.ini (Perbaikan Error)
Buka production.ini. Ganti seluruh isinya dengan versi produksi yang benar dan sederhana.

Ini, TOML

[app:main]
use = egg:tutorial

[server:main]
use = egg:waitress#main
host = 0.0.0.0
port = 6543
6. Buat Template Layout (layout.jinja2)
Buat file baru di tutorial/templates/layout.jinja2.

PowerShell

New-Item tutorial\templates\layout.jinja2
Buka file baru tersebut dan tempelkan kode ini. Ini adalah kerangka HTML utama kita.

HTML

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pyramid Quick Tutorial</title>
</head>
<body>
    {# 'block content' adalah tempat konten halaman kita akan disisipkan #}
    {% block content %}
    {% endblock %}
</body>
</html>
7. Edit Template Halaman (hello_world.jinja2)
Sekarang, edit file tutorial/templates/hello_world.jinja2 yang sudah ada. Ganti seluruh isinya agar "menggunakan" layout baru kita:

Cuplikan kode

{# Beri tahu Jinja2 untuk menggunakan 'layout.jinja2' sebagai dasarnya #}
{% extends "tutorial:templates/layout.jinja2" %}

{# Definisikan konten untuk 'block content' yang ada di layout #}
{% block content %}
<h1>Hello {{ name }}! Welcome to the {{ project }}!</h1>
{% endblock %}
8. Edit tutorial/app.py (Perbarui Renderer)
Buka tutorial/app.py. Kita perlu memberi tahu Jinja2 di mana harus mencari template (add_jinja2_search_path) dan menyederhanakan nama renderer.

Ganti seluruh isi tutorial/app.py dengan kode baru ini:

Python

from pyramid.config import Configurator

def hello_world(request):
    print('Incoming request')
    return {'name': 'Pyramid', 'project': 'tutorial'}

# ------------------------------------------------------------------
# ↓↓↓ PERUBAHAN UTAMA ADA DI SINI ↓↓↓
# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        
        # 1. Tambahkan setingan untuk Jinja2
        # Ini memberi tahu jinja2 untuk mencari template
        # di folder 'tutorial:templates'
        config.add_jinja2_search_path('tutorial:templates')
        
        config.add_route('hello', '/')
        
        # 2. Perbarui renderer
        # Kita hanya perlu nama file, karena search path sudah diatur
        config.add_view(
            hello_world,
            route_name='hello',
            renderer='hello_world.jinja2' # <-- Lebih sederhana
        )
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    # Pastikan 'main' juga memuat Jinja2 dari settings
    # (Meskipun 'app' sudah memuatnya, ini praktik yang baik)
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
9. Perbarui Tes (Wajib)
Output HTML kita sekarang berbeda (karena menyertakan <title> dari layout). Tes kita harus diperbarui untuk memeriksanya.

1. Edit tutorial/tests/test_views.py: Ganti seluruh isinya dengan ini:

Python

import unittest

from pyramid import testing


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        self.config = testing.setUp(settings=settings)
        # Kita juga perlu memuat konfigurasi Jinja2 di tes
        self.config.include('pyramid_jinja2')
        self.config.add_jinja2_search_path('tutorial:templates')

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        from tutorial.app import app
        
        settings = {'pyramid.includes': 'pyramid_jinja2'}
        test_app = app({}, **settings)
        
        from webtest import TestApp
        test_app.testapp = TestApp(test_app)
        
        res = test_app.testapp.get('/', status=200)
        
        # Periksa teks H1
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
        # Periksa teks dari layout.jinja2
        self.assertIn(b'<title>Pyramid Quick Tutorial</title>', res.body)
2. Edit tutorial/tests/test_functional.py: Ganti seluruh isinya dengan ini:

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
        
        # Periksa teks H1
        self.assertIn(b'<h1>Hello Pyramid!', res.body)
        # Periksa teks dari layout.jinja2
        self.assertIn(b'<title>Pyramid Quick Tutorial</title>', res.body)
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
Buka http://localhost:6543/. Anda akan melihat halaman yang sama persis (Hello Pyramid! Welcome to the tutorial!), tetapi sekarang halaman itu dibangun dari dua file template (layout.jinja2 + hello_world.jinja2).