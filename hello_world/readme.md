# Proyek Pyramid (Langkah 6: Functional Testing)

Ini adalah langkah keenam dalam tutorial Pyramid. Kita akan menambahkan **Pengujian Fungsional** (Functional Testing). Berbeda dengan *Unit Test* (Langkah 5) yang menguji fungsi `app()` secara terisolasi, *Functional Test* akan menguji seluruh tumpukan aplikasi, termasuk *entry point* `main()` dan file konfigurasi `.ini`.

Proyek ini didasarkan pada [Quick Tutorial: Functional Testing](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/functional_testing.html) dari dokumentasi resmi Pyramid.

## Tujuan

Tujuan dari proyek ini adalah untuk membuat tes yang mensimulasikan pemanggilan aplikasi secara penuh, persis seperti yang dilakukan server `pserve`. Ini memvalidasi bahwa semua bagian (entry point, konfigurasi, dan kode aplikasi) bekerja sama dengan benar.

## Persyaratan
* Python 3.6+
* `pip` dan `venv` (biasanya sudah termasuk dalam Python)

## Instalasi
1.  **Persiapan Proyek (Salin dari Langkah 5):**
    Pertama, salin seluruh proyek `testing` Anda ke folder baru bernama `functional_testing`.
    ```bash
    # Pastikan Anda di D:\Figo\projects\quick_tutorial
    cd D:\Figo\projects\quick_tutorial
    
    # Salin 'testing' ke 'functional_testing'
    Copy-Item -Path testing -Destination functional_testing -Recurse
    ```
    *Tidak ada perubahan pada `setup.py` atau `tutorial/app.py` di langkah ini.*

2.  **Buat Ulang dan Aktifkan Virtual Environment (PENTING):**
    `venv` tidak bisa disalin. Anda harus membuatnya ulang di dalam folder `functional_testing`.
    ```bash
    # Pindah ke direktori 'functional_testing' yang baru
    cd D:\Figo\projects\quick_tutorial\functional_testing
    
    # HAPUS venv lama yang rusak (PENTING)
    Remove-Item -Path venv -Recurse -Force
    
    # Buat venv baru yang bersih
    python -m venv venv
    
    # Aktifkan venv (Windows PowerShell)
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instal Proyek dan Dependensi (Termasuk Testing):**
    Perintah ini sama seperti di Langkah 5. Ini akan menginstal semua dependensi dari `setup.py` (termasuk `pytest` dan `webtest`).
    ```bash
    # Pastikan (venv) aktif
    pip install -e ".[dev,testing]"
    ```

## Kode Tes Fungsional Baru

Anda tidak mengubah file lama. Anda hanya **membuat satu file baru** di dalam `tutorial/tests/`.

**File Baru:** `tutorial/tests/test_functional.py`
```powershell
New-Item tutorial\tests\test_functional.py

Buka file baru tersebut dan tempelkan kode ini ke dalamnya:

Python

import unittest
from webtest import TestApp

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        # Impor fungsi 'main' dari app.py
        from tutorial.app import main
        
        # Siapkan pengaturan untuk file .ini
        # Kita gunakan 'development.ini' sebagai dasar
        # dan menimpa 'pyramid.includes' agar tidak memuat toolbar
        settings = {
            'pyramid.includes': [], # Kosongkan agar tidak ada debugtoolbar
        }
        
        # Buat aplikasi WSGI menggunakan 'main' (entry point)
        # dan pengaturan .ini kita
        app = main({}, **settings)
        
        # Buat 'TestApp' yang membungkus aplikasi WSGI kita
        self.testapp = TestApp(app)

    def test_hello_world(self):
        # Lakukan permintaan GET ke rute '/'
        res = self.testapp.get('/', status=200)
        
        # Periksa apakah bodinya mengandung 'Hello World!'
        self.assertIn(b'<h1>Hello World!</h1>', res.body)
Menjalankan Tes
Pastikan virtual environment Anda aktif (prompt diawali dengan (venv)) dan Anda berada di D:\Figo\projects\quick_tutorial\functional_testing.

Jalankan pytest:

PowerShell

python -m pytest
Hasil yang Diharapkan
Kali ini, pytest akan menemukan 2 file tes dan menjalankan keduanya. Hasil Anda akan terlihat seperti ini, menunjukkan 2 tes lulus:

============================= test session starts ==============================
platform win32 -- Python 3.x.x, pytest-x.x.x, ...
rootdir: D:\Figo\projects\quick_tutorial\functional_testing
plugins: ...
collected 2 items

tutorial\tests\test_functional.py .                                     [ 50%]
tutorial\tests\test_views.py .                                          [100%]

============================== 2 passed ... in ...s ===============================
