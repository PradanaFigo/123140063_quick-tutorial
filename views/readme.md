# Proyek Pyramid (Langkah 9: View Classes)

Ini adalah langkah kesembilan dalam tutorial Pyramid. Di langkah ini, kita akan melakukan *refactor* (penataan ulang kode) pada *view* kita. Kita akan beralih dari menggunakan **fungsi view** sederhana menjadi menggunakan **Python class** sebagai *view*.

Ini adalah cara yang lebih terorganisir untuk mengelola *view* yang kompleks, karena Anda dapat mengelompokkan beberapa *view* terkait (misalnya, `view_homepage`, `view_edit`, `view_save`) di dalam satu *class* yang sama.

Proyek ini didasarkan pada [Quick Tutorial: Using View Classes](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/view_classes.html) dari dokumentasi resmi Pyramid.

## 🎯 Tujuan

* Melakukan *refactor* dari *view* berbasis fungsi ke *view* berbasis *class*.
* Memperkenalkan *class* `TutorialViews` untuk menampung *method view* kita.
* Belajar menggunakan dekorator `@view_config` untuk menghubungkan *method class* ke rute dan *renderer*.
* Belajar menggunakan `config.scan()` untuk secara otomatis menemukan *view* yang didekorasi.

## 🚀 Instalasi dan Langkah-Langkah

### 1. Persiapan Proyek (Salin dari Langkah 8)

Pertama, salin seluruh proyek `templating` Anda ke folder baru bernama `view_classes`.

```bash
# Pastikan Anda di D:\Figo\projects\quick_tutorial
cd D:\Figo\projects\quick_tutorial

# Salin 'templating' ke 'view_classes'
Copy-Item -Path templating -Destination view_classes -Recurse
2. Buat Ulang dan Aktifkan venv
venv tidak bisa disalin. Anda harus membuatnya ulang di dalam folder view_classes.

Bash

# Pindah ke direktori 'view_classes' yang baru
cd D:\Figo\projects\quick_tutorial\view_classes

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
Inti dari langkah ini adalah perubahan pada tutorial/app.py.

Edit tutorial/app.py (Perubahan Besar)
Ganti seluruh isi tutorial/app.py dengan kode baru ini. Perhatikan penggunaan @view_config dan config.scan().

Python

from pyramid.config import Configurator
from pyramid.view import view_config

# ------------------------------------------------------------------
# ↓↓↓ PERUBAHAN UTAMA ADA DI SINI ↓↓↓
# ------------------------------------------------------------------

class TutorialViews:
    def __init__(self, request):
        # Simpan 'request' agar bisa diakses di method lain
        # sebagai self.request
        self.request = request

    # Dekorator ini menggantikan config.add_view()
    @view_config(route_name='hello', renderer='hello_world.jinja2')
    def hello_world(self):
        print('Incoming request')
        return {'name': 'Pyramid', 'project': 'tutorial'}

# ------------------------------------------------------------------

def app(global_config, **settings):
    """ Fungsi ini berisi logika aplikasi.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tutorial:templates')
        
        # Rute tetap ditambahkan di sini
        config.add_route('hello', '/')
        
        # 'config.scan' akan mencari @view_config di file .py ini
        # Ini menggantikan config.add_view() lama
        config.scan('.app')
    return config.make_wsgi_app()

def main(global_config, **settings):
    """ Fungsi 'main' ini tetap menjadi entry point dari setup.py.
    """
    settings['pyramid.includes'] = 'pyramid_jinja2'
    
    return app(global_config, **settings)
Tidak ada perubahan pada file tes (test_views.py dan test_functional.py). Perilaku eksternal aplikasi tetap sama.

🏁 Menjalankan dan Memverifikasi
1. Menjalankan Tes
Meskipun file tes tidak diubah, kita jalankan tes untuk membuktikan bahwa refactor (penataan ulang kode) kita tidak merusak fungsionalitas apa pun.

PowerShell

# Pastikan (venv) aktif
python -m pytest
Hasil: Anda akan melihat ================= 2 passed ... ==================.

2. Menjalankan Server
Setelah tes lulus, jalankan server:

PowerShell

pserve development.ini --reload
3. Cara Mengakses
Buka http://localhost:6543/.

Anda akan melihat hasil yang sama persis seperti sebelumnya: Hello Pyramid! Welcome to the tutorial!

Meskipun tampilannya sama, kode Anda sekarang jauh lebih rapi dan terorganisir dalam sebuah class.