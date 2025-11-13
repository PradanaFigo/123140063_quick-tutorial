# Proyek Pyramid (Langkah 5: Unit Testing)

Ini adalah langkah kelima dalam tutorial Pyramid. Kita akan menambahkan kemampuan *unit testing* (pengujian unit) ke proyek kita menggunakan `pytest` dan `webtest` untuk memverifikasi bahwa aplikasi kita berfungsi seperti yang diharapkan.

Proyek ini didasarkan pada [Quick Tutorial: Unit Testing](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/unit_testing.html) dari dokumentasi resmi Pyramid.

## Tujuan

Tujuan dari proyek ini adalah untuk menambahkan *framework testing* ke proyek kita. Kita akan:
* Menambahkan `pytest`, `pytest-cov`, dan `webtest` sebagai dependensi *testing*.
* Membagi `tutorial/app.py` agar bisa diuji.
* Menulis dan menjalankan *unit test* pertama kita untuk memverifikasi tampilan "Hello World".

## Persyaratan

* Python 3.6+
* `pip` dan `venv` (biasanya sudah termasuk dalam Python)

## Instalasi

1.  **Persiapan Proyek (Salin dari Langkah 4):**
    Pertama, salin seluruh proyek `debugtoolbar` Anda ke folder baru bernama `testing`.

    ```bash
    # Pastikan Anda di D:\Figo\projects\quick_tutorial
    cd D:\Figo\projects\quick_tutorial
    
    # Salin 'debugtoolbar' ke 'testing' (ini akan membuat folder 'testing')
    Copy-Item -Path debugtoolbar -Destination testing -Recurse
    ```
    Setelah itu, **edit file-file di dalam folder `testing`** sesuai tutorial:
    * **`setup.py`**: Tambahkan `testing_requires` baru dan perbarui `extras_require`.
    * **`tutorial/app.py`**: Lakukan refactor (pemecahan kode) menjadi fungsi `app()` dan `main()`.
    * **Buat File Tes Baru**: Buat `tutorial/tests/test_views.py`.

2.  **Buat Ulang dan Aktifkan Virtual Environment (PENTING):**
    `venv` tidak bisa disalin. Anda harus membuatnya ulang di dalam folder `testing`.

    ```bash
    # Pindah ke direktori 'testing' yang baru
    cd D:\Figo\projects\quick_tutorial\testing
    
    # HAPUS venv lama yang rusak (PENTING)
    Remove-Item -Path venv -Recurse -Force
    
    # Buat venv baru yang bersih
    python -m venv venv
    
    # Aktifkan venv (Windows PowerShell)
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instal Proyek dan Dependensi (Termasuk Testing):**
    Perintah ini akan membaca `setup.py` Anda dan menginstal dependensi "dev" **DAN** "testing" (`pytest`, `webtest`, dll.).

    ```bash
    # Pastikan (venv) aktif
    pip install -e ".[dev,testing]"
    ```

## Menjalankan Tes

1.  Pastikan *virtual environment* Anda aktif (prompt diawali dengan `(venv)`) dan Anda berada di direktori `D:\Figa\projects\quick_tutorial\testing`.

2.  Jalankan `pytest`. Cara terbaik untuk menjalankannya adalah melalui modul Python untuk menghindari error `command not found`:
    ```powershell
    python -m pytest
    ```

## Hasil yang Diharapkan

Anda **tidak** menjalankan server (`pserve`). Sebagai gantinya, Anda akan melihat hasil tes di terminal Anda yang mirip seperti ini:

============================= test session starts ============================== platform win32 -- Python 3.x.x, pytest-x.x.x, ... rootdir: D:\Figo\projects\quick_tutorial\testing plugins: ... collected 1 item

tutorial\tests\test_views.py . [100%]

============================== 1 passed ... in ...s ===============================

Tanda `1 passed` menunjukkan bahwa tes Anda berhasil dan aplikasi "Hello World" Anda berfungsi!