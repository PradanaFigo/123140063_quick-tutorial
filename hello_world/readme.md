# Proyek Hello World Pyramid

Ini adalah aplikasi web "Hello World" minimalis yang dibuat menggunakan [Pyramid Web Framework](https://trypyramid.com/).

Proyek ini didasarkan pada [Quick Tutorial: Hello World](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/hello_world.html) dari dokumentasi resmi Pyramid.

## Tujuan

Tujuan dari proyek ini adalah untuk menunjukkan cara paling sederhana membuat aplikasi web Pyramid yang berfungsi hanya dengan satu file Python dan server WSGI `waitress`.

## Persyaratan

* Python 3.6+
* `pip` (manajer paket Python)

## Instalasi

1.  **Buat Direktori Proyek:**
    Buat direktori untuk proyek Anda (misalnya: `D:\Figo\projects\quick_tutorial\hello_world`) dan buat file `app.py` di dalamnya.

2.  **Instal Dependensi:**
    Proyek ini memerlukan `pyramid` dan `waitress`. Karena Anda tidak menggunakan venv, paket-paket ini akan diinstal secara global.

    Buat file `requirements.txt` dengan isi berikut:

    ```text
    pyramid
    waitress
    ```

    Lalu instal menggunakan pip:
    ```bash
    pip install -r requirements.txt
    ```
    *Atau, instal secara manual:*
    ```bash
    pip install pyramid waitress
    ```

## Menjalankan Aplikasi

1.  Buka terminal (PowerShell atau Command Prompt) dan pindah ke direktori proyek Anda:
    ```powershell
    cd D:\Figo\projects\quick_tutorial\hello_world
    ```

2.  Jalankan server:
    ```powershell
    python app.py
    ```

3.  Server akan berjalan di `http://0.0.0.0:6543`.

## Cara Mengakses

Buka browser web Anda dan kunjungi alamat berikut:

[**http://localhost:6543/**](http://localhost:6543/)

Anda akan melihat pesan `Hello World!` di browser.

## Menghentikan Server

Untuk menghentikan server, kembali ke terminal tempat Anda menjalankan `python app.py` dan tekan **Ctrl+C**.