# Proyek Pyramid (Langkah 2: Package)

Ini adalah langkah kedua dalam tutorial Pyramid, mengubah aplikasi "Hello World" dari satu file menjadi **Paket Python** (Python Package) yang terstruktur.

Proyek ini didasarkan pada [Quick Tutorial: Python Packages](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/package.html) dari dokumentasi resmi Pyramid.

## Tujuan

Tujuan dari proyek ini adalah untuk menstrukturkan ulang aplikasi agar sesuai standar Python, menggunakan `setup.py` agar bisa diinstal oleh `pip`.

## Persyaratan

* Python 3.6+
* `pip` dan `venv` (biasanya sudah termasuk dalam Python)

## Instalasi

1.  **Buat Struktur Proyek:**
    Buat direktori baru `package` di `D:\Figo\projects\quick_tutorial\`. Di dalamnya, buat struktur file berikut dan isi dengan kode dari tutorial:
    * `setup.py`
    * `tutorial/` (folder)
    * `tutorial/__init__.py` (file kosong)
    * `tutorial/app.py` (file kode Anda)

2.  **Buat dan Aktifkan Virtual Environment:**
    Sangat disarankan untuk menggunakan *virtual environment* untuk langkah ini.

    ```bash
    # Pindah ke direktori proyek BARU Anda
    cd D:\Figo\projects\quick_tutorial\package
    
    # Buat venv
    python -m venv venv

    # Aktifkan venv (Windows PowerShell)
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instal Proyek dan Dependensi:**
    Perintah ini membaca `setup.py` dan menginstal `pyramid`, `waitress`, dan proyek `tutorial` Anda ke dalam `venv`.

    ```bash
    # Pastikan (venv) aktif
    pip install -e .
    ```

## Menjalankan Aplikasi

1.  Pastikan *virtual environment* Anda aktif (prompt diawali dengan `(venv)`) dan Anda berada di direktori `D:\Figo\projects\quick_tutorial\package`.

2.  Jalankan server (file `app.py` sekarang ada di dalam `tutorial`):
    ```powershell
    python tutorial/app.py
    ```

3.  Server akan berjalan di `http://0.0.0.0:6543`.

## Cara Mengakses

Buka browser web Anda dan kunjungi alamat berikut:

[**http://localhost:6543/**](http://localhost:6543/)

Anda akan melihat pesan `Hello World!` di browser.

## Menghentikan Server

Untuk menghentikan server, kembali ke terminal tempat Anda menjalankan `python tutorial/app.py` dan tekan **Ctrl+C**.